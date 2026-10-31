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
"""Naming rules for recorded User Keywords and Keyword Arguments.

Keyword and argument names arrive over the page-callable command channel and
are untrusted (ADR 0010); everything that decides whether a name may be
recorded lives here.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

from robot.api import get_model, logger
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.parsing.model.blocks import Keyword, KeywordSection
from robot.running.arguments.embedded import EmbeddedArgumentParser, EmbeddedArguments
from robot.utils import normalize
from robot.variables import VariableMatches

from .cells import VARIABLE_START

# Anything Robot cannot carry inside a single keyword-name cell. A newline in
# particular would end the row and let the rest of the "name" be parsed as
# further Robot source.
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f]")
# Two adjacent whitespace characters of *any* kind. Robot's own tokenizer uses
# `re.compile(r"(\s{2,}|\t)", re.UNICODE)` to split cells, so `\s` here has to
# have exactly the same unicode semantics - matching only ASCII spaces would
# let U+00A0, U+3000 and friends through as a separator Robot still honours.
_ANY_DOUBLE_WHITESPACE = re.compile(r"\s\s")
# A pipe surrounded by whitespace separates cells in Robot's pipe-separated
# format.
_PIPE_SEPARATOR = re.compile(r"\s\|\s")


def _surrogates(name: str) -> bool:
    """True if ``name`` cannot be written to a UTF-8 file.

    A lone surrogate (``\\ud800``) survives every structural check above and
    only blows up inside ``model.save()`` with a ``UnicodeEncodeError``, which
    used to abort the whole recording session.
    """
    try:
        name.encode("utf-8")
    except UnicodeEncodeError:
        return True
    return False


#: Keyword and argument names are typed by a person; a longer one is a mistake,
#: or a page under test filling the user's file through the command binding.
NAME_LIMIT = 200

#: Shapes Robot's lexer would read as something other than one plain name cell,
#: in the order they are reported. Checked after `_exotic_whitespace_error`,
#: which needs the offending character for its message.
_NAME_RULES: tuple[tuple[Callable[[str], object], str], ...] = (
    (lambda name: not name, "Keyword name must not be empty."),
    (
        lambda name: len(name) > NAME_LIMIT,
        f"Keyword name must not be longer than {NAME_LIMIT} characters.",
    ),
    (_surrogates, "Keyword name must not contain unpaired surrogate characters."),
    (
        _CONTROL_CHARS.search,
        "Keyword name must not contain control characters such as newlines or tabs.",
    ),
    (
        lambda name: name != name.strip(),
        "Keyword name must not start or end with whitespace.",
    ),
    (
        _ANY_DOUBLE_WHITESPACE.search,
        "Keyword name must not contain two or more consecutive spaces.",
    ),
    (
        lambda name: name.startswith(("#", "*", "|")),
        "Keyword name must not start with '#', '*' or '|'.",
    ),
    (
        _PIPE_SEPARATOR.search,
        "Keyword name must not contain a '|' surrounded by spaces.",
    ),
    # `...` is Robot's continuation marker: the row folds into the section
    # header instead of defining a keyword, and the recorded steps become an
    # unnamed keyword that makes the whole file unimportable.
    (
        lambda name: name == "...",
        "Keyword name must not be Robot's continuation marker '...'.",
    ),
    # `${...}` in a *name* declares embedded arguments, so `${a} ${b}` matches
    # every two-word keyword call in the suite - `No Operation` included - and
    # silently runs the recorded body instead. An *unclosed* `${` is the other
    # half of the same hole: Robot refuses to create the keyword and the
    # recorded steps are lost. Neither shape has any legitimate use in a
    # recorded name, so all of Robot's variable openers are rejected.
    (
        VARIABLE_START.search,
        (
            "Keyword name must not contain Robot Framework variable syntax "
            "such as '${...}'."
        ),
    ),
)


def _exotic_whitespace_error(name: str) -> str | None:
    """Reject every whitespace character except a plain ASCII space.

    ``str.isspace()`` is exactly the set Robot's unicode-aware ``\\s`` and
    ``str.splitlines()`` react to, so this one check covers U+0085, U+00A0,
    U+2028, U+2029, U+3000, the C0/C1 separators and the rest at once.
    """
    for char in name:
        if char.isspace() and char != " ":
            return (
                "Keyword name must not contain whitespace other than a plain "
                f"space (found U+{ord(char):04X})."
            )
    return None


def keyword_name_error(name: str) -> str | None:
    """Why ``name`` is unusable as a User Keyword name, or ``None`` if it is fine.

    A keyword name is written into the file verbatim - it cannot be escaped the
    way an argument cell can, because escapes would become part of the name a
    caller has to type. So the shapes that would change the *structure* of the
    written file are rejected outright instead. This matters beyond typos: the
    ``new`` command arrives over a page-callable binding, so a hostile page
    could otherwise smuggle whole Robot statements into the user's source file
    through a keyword name.

    The rules mirror what the Robot lexer actually does, not what looks
    dangerous: it splits cells on ``\\s{2,}`` with *unicode* semantics, splits
    lines with ``str.splitlines()`` (which breaks on U+0085, U+2028, U+2029 and
    the C1 separators as well as ``\\n``), and switches a line to the
    pipe-separated format when it starts with ``|``. Every whitespace character
    other than a plain ASCII space is therefore rejected outright - a name is
    the one place where nothing can be escaped.
    """
    if not isinstance(name, str):
        return "Keyword name must be a string."
    exotic = _exotic_whitespace_error(name)
    if exotic:
        return exotic
    for is_unusable, message in _NAME_RULES:
        if is_unusable(name):
            return message
    return None


def normalize_keyword_name(name: str) -> str:
    """The form Robot itself compares keyword names in.

    Robot resolves a keyword call case-insensitively and ignoring spaces and
    underscores, so ``l_ogin as admin`` and ``Login As Admin`` are the *same*
    keyword to it. Any duplicate or collision check that compares raw strings
    therefore lets through names that Robot will later reject as duplicates -
    breaking the user's pre-existing keyword.
    """
    return normalize(name, ignore="_", caseless=True, spaceless=True)


def existing_keyword_names(target: Path) -> set[str]:
    """Names of the User Keywords already defined in ``target``."""
    target = Path(target)
    if not target.exists():
        return set()
    names: set[str] = set()
    for section in get_model(str(target)).sections:
        if isinstance(section, KeywordSection):
            names.update(
                item.name
                for item in section.body
                if isinstance(item, Keyword) and item.name
            )
    return names


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


def collect_known_keywords() -> KnownKeywords:
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
        # `_kw_store` is private to Robot. Without it only library keywords are
        # known, which weakens the collision defence; warn rather than fail.
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
        owner_name = getattr(owner, "name", None) if owner is not suite_file else None
        for kw in getattr(owner, "keywords", ()):
            if not kw.name:
                continue
            for candidate in _shadowable_forms(kw.name, owner_name, prefixes):
                matches = _embedded_matcher(candidate)
                if matches is not None:
                    embedded.append((candidate, matches))
                else:
                    names.add(candidate)
    return KnownKeywords(frozenset(names), tuple(embedded), prefixes)


def _shadowable_forms(
    name: str, owner_name: str | None, prefixes: tuple[str, ...]
) -> list[str]:
    """Every name a call can reach ``name`` by.

    That is the name itself, every form a BDD-prefixed call also reaches, and -
    for an owner a call may qualify with - each of those prefixed by the owner
    name.
    """
    forms = []
    for form in (name, *_bdd_variants(name, prefixes)):
        forms.append(form)
        if owner_name:
            forms.append(f"{owner_name}.{form}")
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
    ``EmbeddedArguments`` says no. Verified against a real `robot` run:
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
    literal_match = _literal_matcher(embedded)
    pattern = _normalized_embedded_pattern(name)
    if pattern is None:
        return literal_match

    def matches(candidate: str) -> bool:
        return literal_match(candidate) or bool(
            pattern.fullmatch(normalize_keyword_name(candidate))
        )

    return matches


def _literal_matcher(embedded: EmbeddedArguments) -> Callable[[str], bool]:
    """``EmbeddedArguments.matches`` (Robot 7.3+), or its older ``match``."""
    matches = getattr(embedded, "matches", None)
    if matches is not None:
        return matches
    return lambda candidate: embedded.match(candidate) is not None


def _custom_pattern(parser: EmbeddedArgumentParser, base: str) -> str | None:
    """The custom pattern of an embedded argument (``n:\\d+``), or ``None``.

    Robot keeps this split private and renamed it in 7.3 (``_parse_arg``, which
    also reads a type) from ``_get_name_and_pattern``.
    """
    parse_arg = getattr(parser, "_parse_arg", None)
    if parse_arg is not None:
        return parse_arg(base)[2]
    get_name_and_pattern = getattr(parser, "_get_name_and_pattern")  # noqa: B009
    _name, pattern, custom = get_name_and_pattern(base)
    return pattern if custom else None


_warned_without_normalized_check = False


def _warn_without_normalized_check(error: Exception) -> None:
    global _warned_without_normalized_check  # noqa: PLW0603 - warn once per run
    if _warned_without_normalized_check:
        return
    _warned_without_normalized_check = True
    logger.warn(
        "recorder: this Robot Framework version does not offer the embedded-argument "
        f"parser the recorder reuses ({error}); a recorded name such as "
        "'Open_Login_Page' is not checked against an embedded 'Open ${page} Page'. "
        "Exact embedded-argument matches are still rejected."
    )


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
            custom = _custom_pattern(parser, match.base)
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
    except AttributeError as error:
        # Robot's private parser changed again; see `_custom_pattern`.
        _warn_without_normalized_check(error)
        return None
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


# A Keyword Argument becomes `${name}` in `[Arguments]` and in every Keyword
# Call that uses it. The name arrives over the page-callable command channel
# (ADR 0010), so only the plainest shape Robot accepts is allowed: anything
# else could close the variable early or smuggle in extended variable syntax.
_ARGUMENT_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


#: Robot's built-in variables. An argument of that name would shadow them in
#: the recorded keyword - `cell()` itself writes `${EMPTY}`.
_BUILTIN_VARIABLES = frozenset(
    normalize_keyword_name(variable)
    for variable in [
        "SPACE",
        "EMPTY",
        "TRUE",
        "FALSE",
        "NONE",
        "NULL",
        "TEMPDIR",
        "EXECDIR",
        "CURDIR",
        "OPTIONS",
        "TEST_NAME",
        "TEST_TAGS",
        "TEST_DOCUMENTATION",
        "TEST_STATUS",
        "TEST_MESSAGE",
        "PREV_TEST_NAME",
        "PREV_TEST_STATUS",
        "PREV_TEST_MESSAGE",
        "SUITE_NAME",
        "SUITE_SOURCE",
        "SUITE_DOCUMENTATION",
        "SUITE_METADATA",
        "SUITE_STATUS",
        "SUITE_MESSAGE",
        "KEYWORD_STATUS",
        "KEYWORD_MESSAGE",
        "LOG_LEVEL",
        "OUTPUT_DIR",
        "OUTPUT_FILE",
        "REPORT_FILE",
        "LOG_FILE",
        "DEBUG_FILE",
    ]
)


_VARIABLE_FORM = re.compile(r"\$\{(.*)\}", re.DOTALL)


def plain_argument_name(name: str) -> str:
    """``email`` for ``${email}``: an argument may be written as a variable."""
    match = _VARIABLE_FORM.fullmatch(name)
    return match.group(1) if match else name


_ARGUMENT_RULES: tuple[tuple[Callable[[str], object], str], ...] = (
    (lambda name: not name, "Argument name must not be empty."),
    (
        lambda name: len(name) > NAME_LIMIT,
        f"Argument name must not be longer than {NAME_LIMIT} characters.",
    ),
    (
        lambda name: not _ARGUMENT_NAME.fullmatch(name),
        (
            "Argument name must start with a letter or '_' and contain only "
            "letters, digits and '_'."
        ),
    ),
)


def argument_name_error(name: object) -> str | None:
    """Why ``name`` is unusable as a Keyword Argument name, or ``None``.

    ``name`` is the plain name or the same written as a variable, ``${name}``.
    """
    if not isinstance(name, str):
        return "Argument name must be a string."
    if name.startswith("${"):
        plain = plain_argument_name(name)
        if plain == name or not _ARGUMENT_NAME.fullmatch(plain):
            return "Write the argument as a variable like ${email}, or just email."
        name = plain
    for is_unusable, message in _ARGUMENT_RULES:
        if is_unusable(name):
            return message
    if normalize_keyword_name(name) in _BUILTIN_VARIABLES:
        return f"Argument name '{name}' is a Robot Framework built-in variable."
    return None


class NameGuard:
    """Decide whether a keyword name may be recorded (ADR 0010).

    ``taken`` names - keywords already in the target file and keywords recorded
    earlier in this session - are collisions too, since a Keyword Recording never
    extends an existing keyword.
    """

    def __init__(self, known: KnownKeywords) -> None:
        self._known = {normalize_keyword_name(n): n for n in known.names}
        self._embedded = known.embedded
        self._prefixes = known.bdd_prefixes

    def error(self, name: str, taken: Iterable[str] = ()) -> str | None:
        """Why ``name`` must not be recorded, or ``None``.

        Names are compared the way Robot compares them - caseless, ignoring
        spaces and underscores - so a re-spelled existing name is a collision.
        """
        invalid = keyword_name_error(name)
        if invalid:
            return invalid
        taken_map = {normalize_keyword_name(t): t for t in taken}
        if normalize_keyword_name(name) in taken_map:
            return (
                f"Keyword '{taken_map[normalize_keyword_name(name)]}' already exists."
            )
        for form in self._name_forms(name):
            normalized = normalize_keyword_name(form)
            existing = (
                self._known.get(normalized)
                or taken_map.get(normalized)
                or self._embedded_shadow(form)
            )
            if existing is not None:
                return (
                    f"Keyword '{existing}' already exists in this suite and would be "
                    f"shadowed by '{name}'. Please choose another name."
                )
        return None

    def _name_forms(self, name: str) -> list[str]:
        """``name`` and every form Robot would resolve a call to it as."""
        return [name, *sorted(_bdd_variants(name, self._prefixes))]

    def _embedded_shadow(self, name: str) -> str | None:
        """The embedded-argument keyword ``name`` would instantiate, if any."""
        for declared, matches in self._embedded:
            try:
                matched = matches(name)
            except Exception as error:
                logger.debug(
                    f"recorder: could not match '{name}' against '{declared}': {error!r}"
                )
                continue
            if matched:
                return declared
        return None
