# Browser library 20.4.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.4.0 is a new release with to Python usage, enhancing Set Presenter Mode
keyword. Also this release drop support for Robot Framework 6x and not minimum
version is raised to 7.1.1. There are also several other bug fixes and smaller
enhancements. Also would like to high light our redesigned
https://robotframework-browser.org/ webpage and it has lots of new content.
Go checkout the webpage and provide feedback in Slack or issue tracker. All
issues targeted for Browser library v20.4.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.4.0).
For first time installation with [pip](https://pip.pypa.io/en/stable/) and
[BrowserBatteries](https://pypi.org/project/robotframework-browser-batteries/)
just run
```bash
   pip install robotframework-browser robotframework-browser-batteries
   rfbrowser install
```
to install the latest available release. If you upgrading
from previous release with [pip](http://pip-installer.org), run
```bash
   pip install --upgrade robotframework-browser robotframework-browser-batteries
   rfbrowser clean-node
   rfbrowser install
```
For first time installation with [pip](http://pip-installer.org) with Browser
library only, just run
```bash
   pip install robotframework-browser
   rfbrowser init
```
If you upgrading from previous release with [pip](http://pip-installer.org), run
```bash
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
```
Alternatively you can download the source distribution from
[PyPI](https://pypi.org/project/robotframework-browser/) and
install it manually. Browser library 20.4.0 was released on Wednesday August 19, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright 1.62.1. BrowserBatteries package was
released with NodeJS 24.19.0.



## Most important enhancements

### Several small issues found while auditing the docs against the code ([#5135](https://github.com/MarketSquare/robotframework-browser/issues/5135))
This issue covers several fixes:

**Security**

* Storage keywords built JavaScript by string interpolation. The six
local/session storage keywords embedded the key straight into the expression
evaluated in the page, so a key containing " did not merely break the
syntax, it executed: x"), (window.pwned = 42), window.localStorage.getItem("y
runs that assignment. The three sites using repr() instead had a quieter
failure — for any non-printable code point above U+FFFF, repr() emits
\U000e0001, which JavaScript reads as an identity escape, so the page
silently addressed a different key. All six now use json.dumps.
* Get Credential wrote the WebAuthn private key to playwright-log.txt.
The Node side logged the whole credential object, and that log is written
under default configuration. The Python side already wraps the key material in
Secret() to keep it out of the RF log; the Node line defeated that. It logs
the id only.

**Bugs**

* JavaScript extension keywords always required an open browser.
getActiveBrowser() throws when nothing is open, so the optional chaining
guarding it never ran — including for a keyword whose only argument is
playwright. atest/.../funky.js's createRemoteBrowser is exactly that
shape, and only passes today because an earlier test leaves a browser open.
The browser is now resolved only when the keyword asks for page, context
or browser.
* Add Locator Handler Custom emptied the spec it was given. It popped keys
out of the caller's dictionary, so a &{dict} variable could be used once;
the second call failed with Action must be defined in the handler
specification, and the variable stayed broken for the rest of the suite.
Listing the same dictionary twice in one call failed the same way. It works on
a copy now.
* Merge Coverage Reports discarded name= when config_file= was also
given. ⚠️ The one change that can alter a passing suite — see below.

**Documentation**

* Emulate Media was annotated -> None but returns a dict, and RF drops a
None return type from the spec entirely, so the keyword reference said it
returned nothing. Get Page Errors was annotated -> dict but returns a
list. Both now declare what they return; no runtime change.
* getElement and findLocator still documented the element=<uuid> selector
syntax, removed in 17.0.0. Comments only.

**One behavior change**

Merge Coverage Reports now honours an explicit name when a config_file is
also supplied. Previously the name was overwritten with the default report
title, so name= worked without a config file and was silently ignored with
one — contradicting the function's own merge order, where keyword arguments
override the config file for every other option.

### Raise minimum needed Robot Framework version to 7.1.1 ([#5133](https://github.com/MarketSquare/robotframework-browser/issues/5133))
To be able to ease the work needed for making Python support easier, it was
decided to drop support for Robot Framework 6.1.x. This also allowed us to clean
some internal conversion logic and architecture of the library better. I understand
if someone sees this a backwards incompatible change, but the 6.1.1 was released
28. July 2023, which is over three years ago. If you have not been able to update
your Robot Framework version, you can still use the older version of Browser
library, but we strongly encourage you to update.


### `Set Presenter Mode` silently fall back to defaults, when invalid dict given ([#5143](https://github.com/MarketSquare/robotframework-browser/issues/5143))
The keyword Set Presenter Mode and the init arg enable_presenter_mode just silently ignored everything that is not 100% correct.

Any Strings were just True and therefore 100% default. Any actual dict,
must be correct, otherwise it failed.

```
*** Test Cases ***
All following calls will end up in full default config.
  Set Presenter Mode    {"color": "red"}   #does not have all keys, therefore full defaults
  Set Presenter Mode    {"duration": "5 seconds", "width": "6px", "style": "dotted", "color": "red"    #missing closing {
  Set Presenter Mode    What ever you put in here, except of an invalid dict.    #will also be a string... and therefore Truthy
```

The documentation however was talking about default which did actually only exist in case of a Truthy non-dict given.


### Keywords called from Python convert plain values, like they do in Robot Framework ([#5145](https://github.com/MarketSquare/robotframework-browser/issues/5145))
The Browser library keyword have been part of the public API for the start, but using keyword that example takes
[Enums](https://docs.python.org/3/library/enum.html) or
[timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects)
are unnecessary hard from Python side. But they are excellent when used
Robot Framework test data, because Robot Framework does automatic conversion
and IDE have good support for Enum types. So all that makes the usage great
from Robot Framework side, makes it harder from Python side. With this change
when keyword methods are called from Python, we now accept string, like the
usage from Robot Framework side. Example

```
browser.click("//button", "middle")                    # was: MouseButton.middle
browser.click_with_options("//button", delay="1.5s")   # was: timedelta(seconds=1.5)
browser.get_text("h1", "==", "Login Page")             # was: AssertionOperator["=="]
```

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#5135](https://github.com/MarketSquare/robotframework-browser/issues/5135) | bug | critical | Several small issues found while auditing the docs against the code |
| [#5133](https://github.com/MarketSquare/robotframework-browser/issues/5133) | feature | critical | Raise minimum needed Robot Framework version to 7.1.1 |
| [#5143](https://github.com/MarketSquare/robotframework-browser/issues/5143) | bug | high | `Set Presenter Mode` silently fall back to defaults, when invalid dict given |
| [#5145](https://github.com/MarketSquare/robotframework-browser/issues/5145) | feature | high | Keywords called from Python convert plain values, like they do in Robot Framework |
| [#1037](https://github.com/MarketSquare/robotframework-browser/issues/1037) | bug | medium | Playwright process connection in container fails when proxy is set ..   client_channel/lb_policy/pick_first/pick_first.cc","file_line":397,"grpc_status":14 |
| [#3367](https://github.com/MarketSquare/robotframework-browser/issues/3367) | bug | medium | "Stream removed" issue happens once "Handle Future Dialogs" is used more than once |
| [#4095](https://github.com/MarketSquare/robotframework-browser/issues/4095) | enhancement | medium | Screenshots in portrait mode (phone) too big in the test report (hardcoded 800px) |
| [#5142](https://github.com/MarketSquare/robotframework-browser/issues/5142) | bug | --- | Review and Fix typos and formatting issues in library documentation (Libdoc) |
| [#5154](https://github.com/MarketSquare/robotframework-browser/issues/5154) | bug | --- | Keyword call banner is silently disabled when Browser is imported with AS alias or subclassed |
| [#5169](https://github.com/MarketSquare/robotframework-browser/issues/5169) | bug | --- | Keyword call banner muting and secret log suppression are disabled when keyword names are translated |
| [#5170](https://github.com/MarketSquare/robotframework-browser/issues/5170) | bug | --- | Keyword call banner paints a resolved secret into the page before Fill Secret rejects it |
| [#5172](https://github.com/MarketSquare/robotframework-browser/issues/5172) | bug | --- | Create Credential paints privateKey and publicKey into the keyword call banner in clear text |
| [#5101](https://github.com/MarketSquare/robotframework-browser/issues/5101) | feature | --- | Add `mode`, `depth` and `boxes` arguments to `Get Aria Snapshot` |
| [#5110](https://github.com/MarketSquare/robotframework-browser/issues/5110) | feature | --- | Add `delay=` argument to `Keyboard Key` for the `press` action |
| [#5117](https://github.com/MarketSquare/robotframework-browser/issues/5117) | feature | --- | Add `Set Storage State` keyword and `indexedDB=`/`credentials=` arguments on `Save Storage State` |

Altogether 15 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av20.4.0).
