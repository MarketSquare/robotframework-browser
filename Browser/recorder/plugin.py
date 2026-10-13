# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""``Record Keyword`` / ``Record Keywords`` - a recorder plugin for Browser.

Drives Playwright's programmatic recorder through the bundled ``recorder.js``
JS extension and turns the recorded, *semantic* action stream into Robot
Framework User Keywords, written live into a ``.robot`` / ``.resource`` file.

Load it with::

    Library    Browser    plugins=Browser.recorder.plugin.RecorderPlugin
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.running.arguments.embedded import EmbeddedArgumentParser, EmbeddedArguments
from robot.variables import VariableMatches

from Browser.base.librarycomponent import LibraryComponent
from Browser.generated.playwright_pb2 import Request

from .keyword_writer import normalize_keyword_name
from .session import RecorderSession

_JS_EXTENSION = Path(__file__).parent.resolve() / "recorder.js"
_POLL_KEYWORD = "rfbRecorderPoll"
_STOP_KEYWORD = "rfbRecorderStop"
_POLL_INTERVAL = 0.2


@dataclass(frozen=True)
class KnownKeywords:
    """What the running suite can already resolve, as the session needs it.

    ``names`` are plain keyword names, ``embedded`` pairs a keyword name that
    declares embedded arguments with a predicate that says whether a candidate
    name would be *matched* by it, and ``bdd_prefixes`` are the suite's own
    ``Given``/``When``/... markers in its configured languages.

    Both ``names`` and ``embedded`` also carry the ``Owner.Keyword`` forms of
    every keyword that can be called owner-qualified, because those names are
    shadowable in exactly the same way as the bare ones - see
    `collect_known_keywords`.

    Everything is plain data plus callables, so `RecorderSession` can consume it
    without ever touching a Robot runtime context.
    """

    names: frozenset[str] = frozenset()
    embedded: tuple[tuple[str, Callable[[str], bool]], ...] = ()
    bdd_prefixes: tuple[str, ...] = ()


def collect_known_keywords(target: Path | None = None) -> KnownKeywords:
    """Every keyword the *running* Robot suite can currently resolve.

    A recorded keyword is written into a resource file, and resource keywords
    outrank library keywords in Robot's resolution order. So a recording named
    after an existing keyword silently takes its place on the next suite run -
    and the ``new`` command is reachable from the page under test. The only
    reliable defence is to ask Robot itself what names are already taken.

    RF 7.4.2 exposes the imported libraries publicly as
    ``Namespace.libraries``; imported resource files and the suite file's own
    keywords have no public accessor and are read from the namespace's keyword
    store. Both give ``ResourceFile``/``TestLibrary`` owners with a ``keywords``
    collection, and the resource cache is flat - resources imported by other
    resources are in it too.

    Owner-qualified names are collected too. ``KeywordStore._get_runner`` asks
    the *suite file* for a keyword before it resolves an explicit
    ``Owner.Keyword`` call, so a keyword literally named ``BuiltIn.Log`` in the
    suite file wins over the call ``BuiltIn.Log`` - and the suite file is the
    recorder's default target. Verified against a real `robot` run. The owner
    name used is the one a call must use, i.e. the ``WITH NAME`` alias when
    there is one. The suite file itself is skipped: ``_get_explicit_runner``
    searches libraries and resources only, so its keywords have no callable
    qualified form to hijack.

    ``target`` is the recording target. Only its *literal, unqualified* names
    are dropped - those are the keywords the writer may legitimately reuse, and
    they are checked separately against the file on disk. Its BDD variants,
    qualified forms and embedded-argument patterns are kept: none of them can
    be "reused" by a literal recorded name, they can only be shadowed by one.

    Returns an empty result when no suite is running, so the recorder still
    works from plain Python.
    """
    try:
        namespace = BuiltIn()._get_context().namespace
    except (RobotNotRunningError, AttributeError) as error:
        logger.debug(f"recorder: no running suite to read keyword names from: {error}")
        return KnownKeywords()
    owners = list(namespace.libraries)
    store = getattr(namespace, "_kw_store", None)
    suite_file = None
    if store is not None:
        owners.extend(store.resources.values())
        suite_file = store.suite_file
        if suite_file is not None:
            owners.append(suite_file)
    else:
        # `_kw_store` is a private Robot attribute. If a future RF version
        # renames or removes it this branch silently falls back to only
        # `namespace.libraries`, dropping every resource, resource-of-resource
        # and suite-file keyword from the collision set with no other signal -
        # quietly weakening the name-collision defence. Failing loudly here
        # (without raising, which would break recording outright on an RF
        # version bump) at least puts the gap in front of the user.
        logger.warn(
            "recorder: could not read Robot's internal keyword store "
            "(Namespace._kw_store is missing or was renamed); resource and "
            "suite-file keywords will not be checked for name collisions "
            "this session."
        )
    languages = getattr(namespace, "languages", None)
    prefixes = tuple(getattr(languages, "bdd_prefixes", None) or ())
    names: set[str] = set()
    embedded: list[tuple[str, Callable[[str], bool]]] = []
    for owner in owners:
        source = getattr(owner, "source", None)
        is_target = bool(
            target is not None and source and Path(source).resolve() == target
        )
        owner_name = getattr(owner, "name", None) if owner is not suite_file else None
        for kw in getattr(owner, "keywords", ()):
            if not kw.name:
                continue
            for candidate, reusable in _shadowable_forms(
                kw.name, owner_name, prefixes, is_target
            ):
                matches = _embedded_matcher(candidate)
                if matches is not None:
                    embedded.append((candidate, matches))
                elif not reusable:
                    names.add(candidate)
    return KnownKeywords(frozenset(names), tuple(embedded), prefixes)


def _shadowable_forms(
    name: str, owner_name: str | None, prefixes: tuple[str, ...], is_target: bool
) -> list[tuple[str, bool]]:
    """Every name a call can reach ``name`` by, and whether it is reusable.

    That is the name itself, every form a BDD-prefixed call also reaches, and -
    for an owner a call may qualify with - each of those prefixed by the owner
    name. Only the plain, unqualified name of a keyword in the recording target
    is *reusable*, i.e. may be recorded again.
    """
    forms = []
    for form in (name, *_bdd_variants(name, prefixes)):
        forms.append((form, is_target and form == name))
        if owner_name:
            forms.append((f"{owner_name}.{form}", False))
    return forms


def _embedded_matcher(name: str) -> Callable[[str], bool] | None:
    """A predicate for the names ``name`` matches, or ``None`` if it is literal.

    A keyword such as ``Open ${page} Page`` is *instantiated* by a call, so the
    literal name ``Open Login Page`` resolves to it and a recording under that
    name shadows it just as surely as a name-for-name collision - verified
    against a real `robot` run. Robot decides that match with the keyword's own
    ``EmbeddedArguments``, so the same object decides it here.

    That check alone is not enough, though. ``EmbeddedArguments`` compiles the
    *raw* literal parts of the name, so its pattern for ``Open ${page} Page`` is
    case-insensitive but otherwise literal - a single space, no underscores.
    Robot's *normal* keyword matching is caseless, spaceless **and** ignores
    underscores, and ``KeywordStore._select_best_matches`` prefers such a normal
    match over an embedded one. So a recorded ``Open_Login_Page`` is a normal
    match for the call ``Open Login Page`` and beats the embedded owner, while
    ``EmbeddedArguments.matches`` says no. Verified against a real `robot` run:
    the call ran the recorded body, rc=0. `_normalized_embedded_pattern` closes
    that by matching the *normalized* candidate, and both checks are kept.
    """
    try:
        embedded = EmbeddedArguments.from_name(name)
    except Exception as error:  # a custom pattern Robot itself cannot compile
        logger.debug(f"recorder: ignoring unparsable keyword name {name!r}: {error}")
        return None
    if embedded is None:
        return None
    pattern = _normalized_embedded_pattern(name)
    if pattern is None:
        return embedded.matches

    def matches(candidate: str) -> bool:
        return embedded.matches(candidate) or bool(
            pattern.fullmatch(normalize_keyword_name(candidate))
        )

    return matches


def _normalized_embedded_pattern(name: str) -> re.Pattern | None:
    """``name`` as a pattern over *normalized* candidate names.

    Built the way Robot builds its own embedded pattern - split on
    `VariableMatches`, custom patterns such as ``${n:\\d+}`` preserved verbatim -
    except that the literal parts around the variables are normalized the way
    Robot compares keyword names. The candidate is normalized the same way
    before matching, so ``Open_Login_Page``, ``OpenLoginPage`` and
    ``open login page`` are all recognised as claims on ``Open ${page} Page``.

    Plain variables use ``(.+?)`` rather than Robot's ``(.*?)``: an embedded
    argument that swallowed nothing would make ``Open Page`` look like a claim
    on ``Open ${page} Page``, which Robot itself does not resolve there.

    A custom pattern is matched against the normalized candidate, so one that
    depends on spaces or underscores can be missed here; the raw
    ``EmbeddedArguments`` check in `_embedded_matcher` still covers those names
    in their exact form. Returns ``None`` when the name has no embedded
    arguments or Robot's parser cannot be reused.
    """
    parser = EmbeddedArgumentParser()
    parts: list[str] = []
    found = False
    try:
        after = string = " ".join(name.split())
        for match in VariableMatches(string, identifiers="$"):
            _arg, _type, custom = parser._parse_arg(match.base)
            group = ".+?" if custom is None else parser._format_custom_regexp(custom)
            parts.extend(
                [re.escape(normalize_keyword_name(match.before)), "(", group, ")"]
            )
            after = match.after
            found = True
        if not found:
            return None
        parts.append(re.escape(normalize_keyword_name(after)))
        return re.compile("".join(parts), re.IGNORECASE)
    except Exception as error:
        logger.debug(f"recorder: no normalized matcher for {name!r}: {error}")
        return None


def _bdd_variants(name: str, prefixes: tuple[str, ...]) -> set[str]:
    """The names a BDD-prefixed call to ``name`` would also resolve.

    Robot strips ``Given``/``When``/``Then``/``And``/``But`` *before* looking a
    keyword up, so a suite keyword called ``Given User Is Logged In`` is reached
    by resolving ``User Is Logged In``. Recording a keyword under that bare name
    therefore hijacks the BDD call without ever colliding with the full name -
    verified against a real `robot` run. The prefixes come from the suite's own
    configured languages, so translated suites are covered too.
    """
    variants = set()
    for prefix in prefixes:
        marker = f"{prefix} "
        if name.lower().startswith(marker.lower()) and name[len(marker) :].strip():
            variants.add(name[len(marker) :])
    return variants


class RecorderPlugin(LibraryComponent):
    """Record interactions in the live browser and emit Browser User Keywords."""

    # -- keywords ---------------------------------------------------------- #

    @keyword(name="Record Keyword", tags=("Recorder",))
    def record_keyword(
        self, name: str, file: Path | None = None, timeout: timedelta | None = None
    ) -> str:
        """Record browser interactions into a User Keyword named ``name``.

        Opens the Playwright recorder in the *currently active* browser context
        and shows the Robot Framework recorder toolbar on the page. Each action
        is converted to a Browser keyword and written **live** as you go; the
        toolbar's *Undo* and *Discard* buttons correct mistakes without leaving
        the browser.

        To finish, press *Stop* in the header of the Robot Framework toolbar, or
        the red *Record* button in the Playwright toolbar. The keyword text is
        returned.

        | =Arguments= | =Description= |
        | ``name`` | Name of the User Keyword to create. Mandatory. |
        | ``file`` | Target ``.robot`` / ``.resource`` file. Defaults to the source file of the running suite. |
        | ``timeout`` | Safety net that ends the recording unattended. Defaults to no timeout, i.e. the keyword blocks until you stop the recording. |

        The name must not collide with a keyword the suite already knows -
        libraries, imported resources and the suite's own keywords - because a
        recorded keyword would silently take the existing one's place.

        Example:
        | ${keyword_text}=    Record Keyword    Login As Admin
        | Record Keyword    Search For Product    ${CURDIR}/resources/shop.resource

        See also `Record Keywords` to record several keywords in one session.
        """
        session = self._run_session(file, timeout, fixed_name=name)
        return session.text()

    @keyword(name="Record Keywords", tags=("Recorder",))
    def record_keywords(
        self, file: Path | None = None, timeout: timedelta | None = None
    ) -> list[str]:
        """Record several User Keywords in one browser session.

        Opens the Playwright recorder and shows the Robot Framework recorder
        toolbar on the page. Use *+ New Keyword* to name and start a keyword,
        record it, then *Finish* it and start the next one. Actions performed
        while no keyword is being recorded are **not** captured, so navigating
        between keywords is free.

        *Undo* removes the last recorded step and *Discard* abandons the current
        keyword entirely. Press *Stop* in the header of the Robot Framework
        toolbar, or the red *Record* button in the Playwright toolbar, to end
        the session.

        Returns the list of keyword names recorded.

        Names that collide with a keyword the suite already knows are rejected
        in the toolbar: a recorded keyword would otherwise silently take the
        existing one's place. Unlike `Record Keyword`, a name already present
        in the target file is rejected too - a session started with
        *+ New Keyword* always creates a new keyword and can never append to
        one that already exists there.

        | =Arguments= | =Description= |
        | ``file`` | Target ``.robot`` / ``.resource`` file. Defaults to the source file of the running suite. |
        | ``timeout`` | Safety net that ends the session unattended. Defaults to no timeout. |

        Example:
        | @{names}=    Record Keywords
        | Record Keywords    ${CURDIR}/resources/shop.resource
        """
        session = self._run_session(file, timeout, fixed_name=None)
        return session.keywords

    # -- session driver ---------------------------------------------------- #

    def _run_session(
        self,
        file: Path | None,
        timeout: timedelta | None,
        fixed_name: str | None,
    ) -> RecorderSession:
        target = Path(file).resolve() if file else self._default_target()
        known = collect_known_keywords(target)
        session = RecorderSession(
            target,
            fixed_name=fixed_name,
            known_keywords=known.names,
            embedded_keywords=known.embedded,
            bdd_prefixes=known.bdd_prefixes,
        )
        logger.info(f"Recording into {target}")

        # Registered once per session rather than cached on the plugin: node's
        # extension list lives on a per-peer state that can be re-created, and a
        # stale "already registered" would then fail with an unknown keyword.
        # Registering again is harmless - node's `require` is cached.
        self.initialize_js_extension(_JS_EXTENSION)
        deadline = (
            None if timeout is None else time.monotonic() + timeout.total_seconds()
        )
        first = True
        try:
            while True:
                reply = self._poll(session.toolbar_state(), reset=first)
                first = False
                for entry in reply.get("events") or []:
                    self._safely(
                        lambda entry=entry: session.handle_event(
                            str(entry.get("event", "added")),
                            entry.get("action") or {},
                        ),
                        f"event {entry!r}",
                    )
                for command in reply.get("commands") or []:
                    self._safely(
                        lambda command=command: session.handle_command(command or {}),
                        f"command {command!r}",
                    )
                self._drain_log(session)
                if session.stopped:
                    break
                if reply.get("mode") == "stopped":
                    break
                if not reply.get("pages"):
                    logger.info("recorder: all pages closed, ending the session")
                    break
                if deadline is not None and time.monotonic() > deadline:
                    logger.info("recorder: timeout reached, ending the session")
                    break
                time.sleep(_POLL_INTERVAL)
        finally:
            # An aborted suite must still leave a well-formed keyword behind.
            # Both cleanup steps below must always be attempted, and neither
            # may replace an exception already propagating out of the loop.
            names: list[str] = []
            try:
                names = session.close()
            except Exception as error:
                logger.debug(f"recorder: close failed: {error}")
            self._drain_log(session)
            try:
                self._call(_STOP_KEYWORD, {})
            except Exception as error:
                # Never mask the real failure with a cleanup failure.
                logger.debug(f"recorder: stop failed: {error}")
            logger.info(f"Recorded {len(names)} keyword(s): {', '.join(names) or '-'}")
        return session

    def _poll(self, state: dict, reset: bool) -> dict:
        return self._call(_POLL_KEYWORD, {"state": json.dumps(state), "reset": reset})

    def _call(self, name: str, arguments: dict) -> dict:
        """One extension-keyword round trip.

        Uses the gRPC stub rather than `call_js_keyword` because the latter logs
        every response at INFO, which at this poll rate would flood the log.
        """
        payload = {"arguments": list(arguments.items())}
        with self.playwright.grpc_channel() as stub:
            request = Request().KeywordCall(name=name, arguments=json.dumps(payload))
            body = ""
            for response in stub.CallExtensionKeyword(request):
                if response.bodyPart:
                    body += response.bodyPart
                elif response.json:
                    body = response.json
        return json.loads(body) if body else {}

    @staticmethod
    def _safely(action: Callable[[], None], what: str) -> None:
        """Run one recorder step, surviving a malformed event or command.

        Events and commands arrive over a channel the page under test can call,
        so a single bogus payload must not tear down a recording the user has
        been building for minutes. The failure is reported and the loop goes on.
        """
        try:
            action()
        except Exception as error:
            logger.warn(f"recorder: ignoring {what}: {error!r}")

    @staticmethod
    def _drain_log(session: RecorderSession) -> None:
        for entry in session.log:
            logger.info(f"recorder: {entry}")
        session.log.clear()

    @staticmethod
    def _default_target() -> Path:
        try:
            source = BuiltIn().get_variable_value("${SUITE_SOURCE}")
        except RobotNotRunningError:
            source = None
        if not source:
            raise ValueError(
                "No 'file' argument given and no running suite source is available. "
                "Provide the target file explicitly, e.g. "
                "Record Keywords    ${CURDIR}/keywords.resource"
            )
        # `${SUITE_SOURCE}` is an abspath, not a realpath: a suite reached
        # through a symlink would otherwise never match its own entry in the
        # collected keywords, and the suite's own keywords - the ones the writer
        # may legitimately reuse - would be reported as collisions.
        return Path(source).resolve()
