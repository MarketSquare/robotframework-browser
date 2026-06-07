# Browser library 20.0.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.0.0 is a new release with enhancements and bug fixes. There are
enhancements to Wait For Request and Get Text keywords, both keywords contains
backward incompatible changes. There is bug fix for the Stop Coverage keyword and
bug fixes to the library documentation. All issues targeted for Browser library
v20.0.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.0.0).
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
install it manually. Browser library 20.0.0 was released on Sunday June 7, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.60.0



## Most important enhancements

### Implement keyword for allTextContents ([#4763](https://github.com/MarketSquare/robotframework-browser/issues/4763))
Get Text keyword has been enhanced to support different Playwright method to get text
from the element. Now user can force how text is returned by keyword by using
`text_type` argument with `allInnerTexts`, `allTextContents`, `inputValue`,
and `innerHTML` values. If argument is not defined or value `None` is used, keyword
should work as before. It will try get the text by two different ways from the element.

## Backwards incompatible changes

### easy to use between logic to Get Text ([#4608](https://github.com/MarketSquare/robotframework-browser/issues/4608))

With the enhancement done to the [AssertionEngine](https://github.com/MarketSquare/AssertionEngine)
in the [5.0 release](https://github.com/MarketSquare/AssertionEngine/releases/tag/v5.0.0),
Browser library supports regex [groups](https://docs.python.org/3/howto/regex.html#grouping)
in the `matches` operator. Example if
[Get Text](https://marketsquare.github.io/robotframework-browser/Browser.html#Get%20Text)
`${selector}` returns text: `Your order number is 123456 and total price is 98.76€.`

```robotframework
*** Test Cases ***
No Group String As Return Value
    ${result} =    Get Text    ${selector}    matches    order number is
    Should Be Equal    ${result}    Your order number is 123456 and total price is 98.76€.

Single Group Tuple As Return Value
    ${result} =    Get Text    ${selector}    matches    order number is (\\d+)
    Length Should Be    ${result}    1
    Should Be Equal    ${result}[0]    123456

Multiple Groups Tuple As Return Value
    ${result} =    Get Text    ${selector}    matches    (\\d+) .* (\\d+\\.\\d+)
    Length Should Be    ${result}    2
    Should Be Equal    ${result}[0]    123456
    Should Be Equal    ${result}[1]    98.76

Groups With Names Dictionary As Return Value
    ${result} =    Get Text    ${selector}    matches    (?P<order_number>\\d+) .* (?P<total_price>\\d+\\.\\d+)
    Length Should Be    ${result}    2
    Should Be Equal    ${result['order_number']}    123456
    Should Be Equal    ${result['total_price']}    98.76

Mixed With Group And Group Names
    ${result} =    Get Text    ${selector}    matches    (\\d+) .* (?P<total_price>\\d+\\.\\d+)
    Length Should Be    ${result}    2
    Should Be Equal    ${result}[0]    123456
    Should Be Equal    ${result}[1]    98.76
```
This change is backwards incompatible if you have used `matches` operator with regex groups
and you expect keyword to return full text.

### Remove deprecated functionality ([#4945](https://github.com/MarketSquare/robotframework-browser/issues/4945))
We have removed the following deprecate functionality:
1. Wait Until Network Is Idle
2. Internal, but not public, code which where not used has been cleaned.


### Wait For Request to return post data ([#4656](https://github.com/MarketSquare/robotframework-browser/issues/4656))
Wait For Request keyword used to return only the URL as string. Now keyword Robot Framework
dotdict which contains following keys: url, method, headers and postData.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4608](https://github.com/MarketSquare/robotframework-browser/issues/4608) | feature | high | easy to use between logic to Get Text |
| [#4763](https://github.com/MarketSquare/robotframework-browser/issues/4763) | feature | high | Implement keyword for allTextContents |
| [#4945](https://github.com/MarketSquare/robotframework-browser/issues/4945) | feature | high | Remove depracated functionality |
| [#3991](https://github.com/MarketSquare/robotframework-browser/issues/3991) | bug | medium | If calling Stop Coverage for a page where Start Coverage is not called, logging of the keyword is wrong |
| [#4741](https://github.com/MarketSquare/robotframework-browser/issues/4741) | bug | medium | Document why screenshot is missing from in log file when using Browser library from custom python library |
| [#4656](https://github.com/MarketSquare/robotframework-browser/issues/4656) | feature | medium | Wait For Request to return post data |
| [#4698](https://github.com/MarketSquare/robotframework-browser/issues/4698) | feature | low | Support listener interface in python plugins |

Altogether 7 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av20.0.0).
