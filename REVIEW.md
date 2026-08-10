# Review guide — `fix/bugs-from-doc-audit`

Eight defects found while auditing the Browser library documentation against its
implementation. Each is written up below as it would be filed, followed by the
technical fix, the functional change a user would notice, and an assessment of
whether anyone could have depended on the old behaviour.

**Affected versions:** 20.3.0 and earlier, unless stated otherwise.

**Branch:** `fix/bugs-from-doc-audit`, three commits on top of `main`.
11 files, +266 / −30.

**How this was reviewed.** Every fix below was then re-reviewed on the opposite
assumption — one agent per change, each told to start from "this is wrong" and
to find the argument for reverting. Two changes did not survive that and were
dropped: a `str()` removal in `crawling.py` that fixed nothing reachable and
removed the only guard on a union-typed value, and a stray `uv.lock` that this
project does not track. Four more were corrected rather than kept as written;
those corrections are folded into the write-ups below.

**Verification.** 115/115 jest, `tsc --noEmit` at the same nine pre-existing
errors as the baseline, 169 Python unit tests, `ruff format` clean and `ruff
check` three findings below baseline.

| # | Area | Severity | Backwards-incompatible? |
|---|---|---|---|
| 1 | Storage keywords build JavaScript by raw interpolation | **Critical** | Low — see §1.5 |
| 2 | `Get Credential` writes the private key to disk | **High** | Low, and intended |
| 3 | JS extension keywords always require an open browser | High | No — strictly more permissive |
| 4 | `Add Locator Handler Custom` destroys the caller's spec | High | No |
| 5 | `Merge Coverage Reports` discards `name=` when `config_file=` is given | Medium | **Yes — medium** |
| 6 | `Emulate Media` documented as returning nothing | Low | No (docs only) |
| 7 | `Get Page Errors` documented as returning a dict | Low | No (docs only) |
| 8 | Stale comments describing a mechanism removed in 17.0.0 | Trivial | No |

Plus a `sessionStorage` assertion message fix, described in §1.4 — that one has
its own small compatibility note.

Three of these defects survived for years by not being tested, so each ships
with the test that closes that gap; see **Test additions** at the end.

---

## 1. Storage keywords build JavaScript by raw string interpolation

### 1.1 Issue

> **Title:** `LocalStorage Get Item` executes arbitrary JavaScript when the key contains a double quote
>
> **Labels:** bug, security
>
> The six local/session storage keywords embed the key — and for `Set Item`, the
> value — directly into a JavaScript expression that is then evaluated in the
> page. Three of them interpolate into a quoted literal with no escaping at all,
> and three use Python's `repr()`.
>
> Neither produces a JavaScript string literal reliably.
>
> **Reproduction — code execution:**
>
> ```robotframework
> LocalStorage Get Item    x"), (window.pwned = 42), window.localStorage.getItem("y
> ```
>
> The generated script is
>
> ```js
> window.localStorage.getItem("x"), (window.pwned = 42), window.localStorage.getItem("y")
> ```
>
> `window.pwned = 42` runs in the page under test. Any key that reaches the
> keyword from test data, a fixture, a CSV, or the application itself is an
> injection point. A key containing only a plain `"` fails with a JavaScript
> `SyntaxError` that names neither the keyword nor the key.
>
> **Reproduction — silent wrong key:**
>
> ```robotframework
> LocalStorage Set Item    tag\U000e0001char    value
> ${v}=    LocalStorage Get Item    tag\U000e0001char       # -> None
> ```
>
> For any non-printable code point above U+FFFF, `repr()` emits `\U000e0001`.
> JavaScript treats `\U` as an *identity escape*: the backslash is dropped and
> the literal text `U000e0001` becomes part of the string. The page reads or
> deletes a different key than the one asked for, with no syntax error and no
> exception — the keyword simply returns `None`.
>
> Because `LocalStorage Set Item` used `repr()` while `LocalStorage Get Item`
> used raw interpolation, a write and a read of the same key did not even agree
> with each other.
>
> **Affected keywords:** `LocalStorage Get Item`, `LocalStorage Set Item`,
> `LocalStorage Remove Item`, `SessionStorage Get Item`,
> `SessionStorage Set Item`, `SessionStorage Remove Item`.

### 1.2 Technical fix

`Browser/keywords/webapp_state.py` — all six call sites now embed with
`json.dumps()`:

```python
response = self.eval_js(
    f"window.localStorage.getItem({json.dumps(key)})", frame_selector
)
```

`json.dumps` is the right tool for three specific reasons:

- Its output is a **strict subset of JavaScript string-literal syntax**. Every
  escape it emits (`\"`, `\\`, `\n`, `\uXXXX`) means the same thing in JS as in
  JSON.
- With the default `ensure_ascii=True` the output is **pure ASCII for every code
  point** in the Unicode range. Astral characters become surrogate-pair escapes
  (`"\ud83d\ude00"`), which JavaScript reassembles correctly. This also means
  U+2028 LINE SEPARATOR and U+2029 PARAGRAPH SEPARATOR — legal in JSON, but
  illegal inside a JavaScript string literal before ES2019 — never reach the
  page as raw characters.
- Being ASCII, the script survives the protobuf hop to the Node process without
  any encoding question.

`repr()` was rejected because of the `\U` case above. Manual escaping was
rejected because it is the thing that just failed.

**Verification.** Differential fuzz over 601 generated keys, each expression
executed against a `getItem` spy:

| implementation | ok | syntax error | wrong key | injection |
|---|---|---|---|---|
| old, raw interpolation | 452 | 109 | 40 | reproduced |
| old, `repr()` | 528 | 0 | 73 | 0 |
| **new, `json.dumps()`** | **601** | **0** | **0** | **0** |

### 1.3 Functional change

- Keys and values containing `"`, `\`, newlines, tabs, NUL, or any Unicode
  character now work. Previously they failed, or silently addressed a different
  key.
- A key can no longer inject JavaScript into the page.
- No change whatsoever for keys made of ordinary printable characters, which is
  the overwhelming majority of real usage.

### 1.4 Related: `SessionStorage Get Item` assertion message

The assertion message prefix was `"sessionStorage "` with a trailing space, but
`verify_assertion` supplies its own separator, so failures read:

```
sessionStorage  'None' (nonetype) should be 'Tidii' (str)
```

— with two spaces. The `localStorage` sibling never had the trailing space. The
prefix is now `"sessionStorage"`, and the two are consistent.

### 1.5 Backwards compatibility

**Low risk, with two named exceptions.**

- **Anyone exploiting the injection deliberately** — using a crafted storage key
  as a back door to run JavaScript — loses that. This is the fix working as
  intended; `Evaluate JavaScript` is the supported way to run JavaScript.
- **Anyone who worked around the mangling** by writing the corrupted key
  (`tagU000e0001char`) as a literal in their tests will now address the real key
  instead. This requires someone to have diagnosed the `\U` mangling and adapted
  to it, which the silent nature of the bug makes unlikely.
- **Error-message matching.** A test using `Run Keyword And Expect Error` on the
  double-spaced `sessionStorage  ...` text needs one space removed. Glob
  patterns with `*` are unaffected.

No supported usage changes behaviour.

---

## 2. `Get Credential` writes the WebAuthn private key to the log file

### 2.1 Issue

> **Title:** `Get Credential` logs the full credential, including `privateKey`, to `playwright-log.txt`
>
> **Labels:** bug, security
>
> The Node side logs the whole credential object returned by Playwright:
>
> ```ts
> logger.info(`Retrieved credential with id: ${JSON.stringify(credential)}`);
> ```
>
> Playwright's `context.credentials.get()` returns
> `{ id, rpId, userHandle, privateKey, publicKey }`, where `privateKey` is a
> base64url-encoded PKCS#8 private key and an ordinary own enumerable string
> property — so `JSON.stringify` includes it in full.
>
> This is not gated behind a debug setting. The Node logger defaults to level
> `info`, and `enable_playwright_debug` defaults to `library`, which routes the
> Node process's stdout to `playwright-log.txt` in the output directory. So under
> **default configuration**, every `Get Credential` call writes a private key in
> clear text to a file that is routinely archived as a CI artifact.
>
> The Python side already treats this material as sensitive — the keyword wraps
> the returned key in `Secret()` specifically so it does not reach the Robot
> Framework log. The Node-side log defeated that.

### 2.2 Technical fix

`node/playwright-wrapper/credential.ts`:

```ts
// Never stringify the whole credential: it carries privateKey, and this log
// goes to playwright-log.txt, which is written by default.
logger.info(`Retrieved credential with id: ${credential.id}`);
```

The log message always claimed to print the id; now it does.

An audit of the rest of the Node side found no second instance of this class:
`createCredential` logs only `rpId` and `id`, the gRPC wrappers log
`{event_kind, action, status}` and never stringify request bodies, and
`Fill Secret` / `Type Secret` route through `fillText` / `typeText`, which do no
Node-side logging of the value.

### 2.3 Functional change

`playwright-log.txt` no longer contains WebAuthn private keys. Nothing else
changes: the keyword still returns `id`, `rpId`, `userHandle`, `privateKey` and
`publicKey` to the caller, and the Python side still logs
`Retrieved credential with id: <id>, rpId: <rpId>`.

### 2.4 Backwards compatibility

**Low risk.** The only way to depend on the old behaviour is to have been
scraping the private key out of `playwright-log.txt`, which is precisely the
disclosure being closed. The key is still available from the keyword's return
value, which is the supported route.

---

## 3. JavaScript extension keywords always require an open browser

### 3.1 Issue

> **Title:** A JS extension keyword fails with "Browser has been closed." even when it does not use the browser
>
> **Labels:** bug
>
> `extensionKeywordCall` populates the arguments a JS extension keyword can
> declare:
>
> ```ts
> apiArguments.set('page', state.getActivePage());
> apiArguments.set('context', state.getActiveContext());
> apiArguments.set('browser', state.getActiveBrowser()?.browser);
> ```
>
> `getActiveBrowser()` **throws** `Browser has been closed.` when nothing is
> open. It never returns `undefined` — it has exactly two exits, a throw or a
> `BrowserState` — so the `?.` was dead code and could not protect anything.
>
> The three lines run unconditionally, before the keyword's own parameters are
> even inspected. Every extension keyword therefore requires an open browser,
> including keywords that use none of them:
>
> ```js
> // atest/test/05_JS_Tests/funky.js
> async function createRemoteBrowser(logger, playwright) { ... }
> ```
>
> This keyword's entire purpose is to *start* something, and it cannot be called
> until a browser is already open.

### 3.2 Technical fix

`node/playwright-wrapper/playwright-state.ts` — resolve the browser only when
the keyword asks for something that needs one:

```ts
const argNames = getArgumentNamesFromJavascriptKeyword(keyword);
if (argNames.some((name) => name === 'page' || name === 'context' || name === 'browser')) {
    apiArguments.set('browser', state.getActiveBrowser().browser);
}
apiArguments.set('page', state.getActivePage());
apiArguments.set('context', state.getActiveContext());
```

The guard covers `page` and `context` as well as `browser`, and this is
deliberate. Those two are optional-chained (`this.activeBrowser?.context?.c`)
and quietly return `undefined` rather than throwing. Guarding only `browser`
would leave a `page`-declaring keyword — by far the common case — failing deep
inside its own body with `Cannot read properties of undefined (reading
'locator')` instead of the clear `Browser has been closed.`

`argNames` is computed once and reused for the positional call, which also
removes a duplicate parse.

**Verification.** The real function was driven through jest against a copy of
the previous implementation. With no browser open, the old code failed all four
shapes tested — `playwright`-only, `(logger, playwright)`, a defaulted
parameter, and `(page)`. The new code runs the first three and gives the clear
error for the fourth. Repo suite: 115/115.

### 3.3 Functional change

An extension keyword that declares none of `page`, `context` or `browser` can
now be called with no browser open. Keywords that do declare one of them behave
exactly as before, including the error message.

### 3.4 Backwards compatibility

**No risk in practice — the change is strictly more permissive.** Calls that
worked continue to work identically; calls that failed may now succeed.

One edge case worth recording: `getArgumentNamesFromJavascriptKeyword` does not
parse destructured (`({browser})`) or rest (`...args`) parameters. A keyword
declaring `browser` that way previously threw `Browser has been closed.`
unconditionally — i.e. it never worked at all — and will now run and receive
`undefined`. Since neither behaviour is functional, no working test changes.
This parser limitation is pre-existing and untouched.

---

## 4. `Add Locator Handler Custom` destroys the caller's specification

### 4.1 Issue

> **Title:** A handler spec dictionary can only be passed to `Add Locator Handler Custom` once
>
> **Labels:** bug
>
> The keyword pops keys out of the spec dictionary it is given, mutating the
> caller's object. Robot Framework passes list-variable elements by reference, so
> the caller's `&{dict}` is emptied as a side effect of the call.
>
> **Reproduction:**
>
> ```robotframework
> *** Variables ***
> &{CLICK_SPEC}    action=click    selector=id=OverlayCloseButton
>
> *** Test Cases ***
> First Test
>     VAR    @{specs}    ${CLICK_SPEC}
>     Add Locator Handler Custom    id=overlay    ${specs}
>
> Second Test
>     VAR    @{specs}    ${CLICK_SPEC}
>     Add Locator Handler Custom    id=overlay    ${specs}
> ```
>
> ```
> First Test   | PASS |
> Second Test  | FAIL | ValueError: Action must be defined in the handler specification: {}
> ```
>
> The suite variable is permanently gutted, so every later test using it fails
> too. A second manifestation needs no reuse across tests at all — listing the
> same dictionary twice in one call fails on the second iteration of the loop.
>
> The `[${spec}]` inline form documented in the keyword is unaffected, because
> Robot Framework re-evaluates it into a fresh dictionary each time. That is why
> the existing acceptance tests, which all use that form, never caught it.

### 4.2 Technical fix

`Browser/keywords/locator_handler.py` — work on a copy, and use `pop` for its
return value rather than as a separate deletion step:

```python
options = dict(spec)
if action == "fill":
    handler_action.value = options.pop("value")
else:
    handler_action.value = ""
options.pop("action", None)
handler_action.selector = options.pop("selector")
handler_action.optionsAsJson = json.dumps(options)
```

The unconditional `pop("value")` and `pop("selector")` cannot raise a new
`KeyError`: validation earlier in the same loop already rejects a missing
`selector`, a `fill` action without `value`, and a non-`fill` action carrying a
`value`.

**Verification.** Differential fuzz over all 96 combinations of `action` ×
`selector` × `value` × `force` × `timeout`, comparing the emitted proto fields
or the raised exception: **0 differences**. The only observable change is that
the caller's dictionary survives.

### 4.3 Functional change

A handler-spec dictionary can be reused — across calls, across tests, and twice
within one call. The message sent to the Node side is byte-identical in every
input case.

### 4.4 Backwards compatibility

**No risk.** The wire format is unchanged, and the only behavioural difference
is that a dictionary the caller owns is no longer emptied. Depending on that
would mean depending on the keyword clearing your variable for you.

---

## 5. `Merge Coverage Reports` ignores `name=` when a config file is given

### 5.1 Issue

> **Title:** `Merge Coverage Reports` silently discards the `name` argument if `config_file` is also given
>
> **Labels:** bug
>
> ```ts
> if (mergedOptions.name === '' && configFileModule.name) {
>     mergedOptions.name = configFileModule.name;
> } else {
>     mergedOptions.name = defaultName;
> }
> ```
>
> When the user supplies a name, `mergedOptions.name` is non-empty, the condition
> is false, and the `else` overwrites the user's name with the hard-coded
> `Browser library Merged Coverage Report`.
>
> ```robotframework
> Merge Coverage Reports    ${in}    ${out}
> ...    config_file=${CURDIR}/coverageConfigMD.js
> ...    name=My Report          # report title: "Browser library Merged Coverage Report"
> ```
>
> Without `config_file=`, the same `name=` works — the no-config branch of the
> same function honours it. So `--name` on the CLI and `name=` on the keyword
> work until you add a config file, at which point they are silently ignored.
>
> This contradicts the function's own merge order, `{...configFileModule,
> ...options}`, which spreads keyword arguments last precisely so they override
> the config file, as they do for `inputDir` and `outputDir`.

### 5.2 Technical fix

`node/playwright-wrapper/playwright-state.ts`:

```ts
if (mergedOptions.name === '') {
    mergedOptions.name = configFileModule.name || defaultName;
}
```

Truth table — only one case changes:

| user `name` | config `name` | before | after |
|---|---|---|---|
| unset | set | config name | config name |
| unset | unset | default | default |
| unset | `''` | default | default |
| **set** | set or unset | **default** | **user's name** |

`||` rather than a strict `undefined` check is deliberate: an empty-string
config name must still fall through to the default, exactly as before, or the
report would be titled with an empty string.

Nothing downstream depends on the name: `mergedOptions` has one consumer,
`new CoverageReport(mergedOptions).generate()`, and no path, directory or
filename is derived from `.name`. It is the report title, asserted in the
acceptance tests by reading the `.mcr-title` element.

### 5.3 Functional change

`name=` (keyword) and `--name` (CLI) now take effect when a config file is also
supplied. Precedence is: explicit argument, then config file, then the built-in
default.

### 5.4 Backwards compatibility

**This is the one change that can break a passing test.**

A suite that passes both `config_file=` and `name=` *and* asserts the report
title will see the title change from `Browser library Merged Coverage Report` to
whatever it asked for. That is the requested behaviour, but a test pinned to the
old title fails.

Assessed as **medium** rather than high because the combination is narrow, the
old behaviour is not documented anywhere, and anyone who passed `name=` and got
the default title would reasonably have read it as a bug. Worth one line in the
release notes.

---

## 6. `Emulate Media` documented as returning nothing

### 6.1 Issue

> **Title:** `Emulate Media` is documented with return type `null` but returns a dictionary
>
> **Labels:** bug, documentation
>
> The keyword is annotated `-> None`. It has a single return path,
> `return json.loads(response.body)`, and the Node side always sends a JSON
> object.
>
> Robot Framework drops a `-> None` return type from the Libdoc spec entirely, so
> the published keyword reference shows `Emulate Media` returning `null` — for a
> keyword the library's own acceptance tests assign and compare as a dictionary:
>
> ```robotframework
> ${media} =    Emulate Media    colorScheme=dark
> Dictionaries Should Be Equal    ${media}    ${expected_media}
> ```
>
> Users reading the reference have no way to discover the return value exists.

### 6.2 Technical fix

`Browser/keywords/pdf.py`: `-> None` becomes `-> dict`.

### 6.3 Functional change

None at runtime. Robot Framework performs no conversion on return values; the
annotation's only consumer is Libdoc. The keyword reference will show the
correct return type after the next release build.

### 6.4 Backwards compatibility

**None.** The runtime value is unchanged. Static type checkers analysing test
code will stop reporting the value as `None`, which is a correction.

---

## 7. `Get Page Errors` documented as returning a dict

### 7.1 Issue

> **Title:** `Get Page Errors` is annotated `-> dict` but returns a list
>
> **Labels:** bug, documentation
>
> The Node side returns a JSON array, and `_slice_messages` returns a list on
> every path. The library's own acceptance tests index it positionally:
>
> ```robotframework
> ${errors}[0][name]
> ${errors}[-1][time]
> ```
>
> The sibling keyword `Get Console Log` is correctly annotated `-> list[dict]`.

### 7.2 Technical fix

`Browser/keywords/playwright_state.py`: `-> dict` becomes `-> list[dict]`,
matching `Get Console Log`.

### 7.3 Functional change

None at runtime.

A specific concern was checked and ruled out: the annotation does **not** select
an assertion handler. `Get Page Errors` calls the generic `verify_assertion`
directly, and the sorting behaviour of `list_verify_assertion` (which reorders
both sides for `==`) is never reached. Assertion semantics are unchanged.

### 7.4 Backwards compatibility

**None.** Documentation and static typing only.

---

## 8. Comments describing a mechanism removed in 17.0.0

### 8.1 Issue

> **Title:** `getElement` comments still describe the `element=<uuid>` selector engine
>
> **Labels:** documentation
>
> The doc comments on `getElement` / `getElements` state that they "create global
> UUID for it, and store the reference in global state. Enables using special
> selector syntax `element=<uuid>` in RF keywords."
>
> That mechanism was removed in commit `073097e5`, released in Browser 17.0.0
> (July 2023). `element=<uuid>` now fails with `Unknown engine "element"`, which
> the acceptance tests assert. The functions return
> `locator._selector` — the selector string Playwright built.
>
> The same stale description also appears in the `@param` documentation for
> `findLocator`, which is the function `getElement` calls.

### 8.2 Technical fix

Comments only, no executable change. `node/playwright-wrapper/evaluation.ts` and
`node/playwright-wrapper/playwright-invoke.ts` now describe what the functions
do: return a selector string usable as the **first** clause of another selector.

"First clause" is precise, not cautious: when a selector prefix is configured,
the returned selector is wrapped as `!prefix <selector>`, and that marker is only
honoured at the start of a selector.

### 8.3 Functional change

None.

### 8.4 Backwards compatibility

None.

---

## Test additions

Three of these defects survived because the existing tests could not have caught
them. Each fix ships with the test that closes that gap.

### `utest/test_webapp_storage_escaping.py` (new)

Calls all six storage keywords with `eval_js` mocked and asserts the exact
script handed to it, across fourteen awkward keys — quotes, backslashes,
newlines, NUL, U+2028/U+2029, bidi overrides, astral printables, astral
non-printables, and an injection payload.

Coverage of `Browser/keywords/webapp_state.py`: **0% → 88%**. Verified by
mutation: restoring the raw interpolation fails 24 of the 169 cases.

### `atest/.../locator_handler.robot` — spec reuse

Every existing case uses the `[${spec}]` inline form, which Robot Framework
re-evaluates into a fresh dictionary and which therefore cannot detect in-place
mutation. The new case passes a list variable — which aliases the caller's
dictionary — reuses the same spec across calls, and lists it twice within one
call.

### `atest/.../coverage.robot` — `config_file` with `name`

The only input combination whose behaviour changed was covered by nothing. The
new case supplies both and asserts the rendered `.mcr-title`.

---

## Verification summary

| check | result |
|---|---|
| `jest` (Node) | 115/115 pass |
| `tsc --noEmit` | same 9 pre-existing errors as the baseline; none in changed files |
| `pytest utest/` (storage) | 169 pass, 88% coverage of the changed module |
| mutation test | reverting the escaping fails 24 tests |
| `ruff format` | clean |
| `ruff check` | 3 fewer findings than baseline |
| behavioural fuzz | 96/96 identical protos (locator handler); 601/601 correct scripts (storage) |

## Suggested release-note lines

- **Fixed:** storage keywords now escape keys and values correctly. Keys
  containing quotes, backslashes, control characters or astral Unicode work, and
  a key can no longer inject JavaScript into the page.
- **Fixed:** `Get Credential` no longer writes the credential's private key to
  `playwright-log.txt`.
- **Fixed:** a JavaScript extension keyword that does not take `page`, `context`
  or `browser` can be called without an open browser.
- **Fixed:** `Add Locator Handler Custom` no longer empties the specification
  dictionary it is given, so it can be reused.
- **Changed:** `Merge Coverage Reports` now honours an explicit `name` when a
  `config_file` is also given. Previously the name was replaced with the default
  report title. *If you pass both and assert the report title, update the
  expected value.*
- **Fixed:** `Emulate Media` and `Get Page Errors` declare their real return
  types, so the keyword reference is correct.

## What is deliberately not in here

Two findings came out of the adversarial pass, were judged out of scope for a
bug-fix branch, and are left for whoever wants them:

- `Browser/base/librarycomponent.py:166` still branches on
  `selector.startswith("element=")`. That has been dead since `073097e5`
  removed the UUID-handle mechanism in 17.0.0; its old job — keeping an element
  reference clear of the selector prefix — moved to the `!prefix` marker in
  `getters.py`.
- `atest/test/01_Browser_Management/element_selector.robot` still titles itself
  after that removed syntax, though its assertions are correct.

Both are cosmetic. They are named here so the next reader does not have to
rediscover that the branch is dead rather than load-bearing.
