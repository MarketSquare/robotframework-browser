# robotframework-browser
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-46-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Version](https://img.shields.io/pypi/v/robotframework-browser.svg)](https://pypi.python.org/pypi/robotframework-browser)
[![Actions Status](https://github.com/MarketSquare/robotframework-browser/workflows/Continuous%20integration/badge.svg)](https://github.com/MarketSquare/robotframework-browser/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

----

[Robot Framework](https://robotframework.org) Browser library powered by [Playwright](https://playwright.dev/). Moving browser automation to year 2021!

Aiming for :rocket: speed, :white_check_mark: reliability and :microscope: visibility.

See [keyword documentation](https://marketsquare.github.io/robotframework-browser/Browser.html) and
[web page](https://robotframework-browser.org/) for more details.

# Installation instructions

Only Python 3.7 or newer is supported.

1. Install node.js e.g. from https://nodejs.org/en/download/ (only < v15 supported; if unsure, use 14.15.0 LTS)
2. Update pip `pip install -U pip` to ensure latest version is used
3. Install robotframework-browser from the commandline: `pip install robotframework-browser`
4. Install the node dependencies: run `rfbrowser init` in your shell
  - if `rfbrowser` is not found, try `python -m Browser.entry init`

Please note that by default Chromium, Firefox and WebKit browser are installed, even those would be already
installed in the system. The installation size depends on the operating system, but usually is +700Mb.
It is possible to skip browser binaries installation with `rfbrowser init --skip-browsers` command, but then user
is responsible for browser binary installation.

Or use the [docker images](https://github.com/MarketSquare/robotframework-browser/packages). Documented at [atest/docker/README.md](https://github.com/MarketSquare/robotframework-browser/blob/master/atest/docker/README.md).

## Update instructions

To upgrade your already installed robotframework-browser library

1. Update from commandline: `pip install -U robotframework-browser`
2. Install the node dependencies for the newly installed version: `rfbrowser init`

# Examples

### Testing with [Robot Framework](https://robotframework.org)
```RobotFramework
*** Settings ***
Library   Browser

*** Test Cases ***
Example Test
    New Page    https://playwright.dev
    Get Text    h1    contains    Playwright
```
### and testing with [Python](https://python.org).
```python
import Browser
browser = Browser.Browser()
browser.new_page("https://playwright.dev")
assert 'Playwright' in browser.get_text("h1")
browser.close_browser()
```

### and extending with JavaScript

```JavaScript
async function myGoToKeyword(page, args) {
  return await page.goto(args[0]);
}
exports.__esModule = true;
exports.myGoToKeyword = myGoToKeyword;
```

```RobotFramework
*** Settings ***
Library   Browser  jsextension=${CURDIR}/mymodule.js

*** Test Cases ***
Example Test
   New Page
   myGoToKeyword   https://www.robotframework.org
```
### Ergonomic selector syntax, supports chaining of `text`, `css`  and `xpath` selectors

```RobotFramework
# Select element containing text "Login" with text selector strategy 
# and select it's parent `input` element with xpath
Click    "Login" >> xpath=../input
# Select element with CSS strategy and select button in it with text strategy
Click    div.dialog >> "Ok"
```
### Evaluate in browser page
```RobotFramework
New Page   ${LOGIN_URL}
${ref}=    Get Element    h1
Get Property    ${ref}    innerText    ==    Login Page
Execute JavaScript    (elem) => elem.innerText = "abc"    ${ref}
Get Property    ${ref}    innerText    ==    abc
```
### Asynchronously waiting for HTTP requests and responses
```RobotFramework
# The button with id `delayed_request` fires a delayed request. We use a promise to capture it.
${promise}=    Promise To    Wait For Response    matcher=    timeout=3s
Click    \#delayed_request
${body}=    Wait For    ${promise}
```
### Device Descriptors
```RobotFramework
${device}=  Get Device  iPhone X
New Context  &{device}
New Page
Get Viewport Size  # returns { "width": 375, "height": 812 }
```
### Sending HTTP requests and parsing their responses
```RobotFramework
&{response}=    HTTP    /api/post    POST    {"name": "John"}
Should Be Equal    ${response.status}    ${200}
```
# Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development instructions.

## Core team

In order of appearance.

  * Mikko Korpela
  * Tatu Aalto
  * Janne Härkönen (Alumnus)
  * Kerkko Pelttari
  * René Rohner

## Contributors

This project is community driven and becomes a reality only through the work of all the people who contribute.
Supported by [Robocorp](https://robocorp.com/) through [Robot Framework Foundation](https://robotframework.org/foundation/).
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/mkorpela"><img src="https://avatars1.githubusercontent.com/u/136885?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Mikko Korpela</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=mkorpela" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/aaltat"><img src="https://avatars0.githubusercontent.com/u/2665023?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Tatu Aalto</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=aaltat" title="Code">💻</a></td>
    <td align="center"><a href="https://robocorp.com"><img src="https://avatars1.githubusercontent.com/u/8512727?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Antti Karjalainen</b></sub></a><br /><a href="#fundingFinding-aikarjal" title="Funding Finding">🔍</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/ismoaro/"><img src="https://avatars2.githubusercontent.com/u/1047173?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ismo Aro</b></sub></a><br /><a href="#fundingFinding-IsNoGood" title="Funding Finding">🔍</a></td>
    <td align="center"><a href="https://twitter.com/janneharkonen"><img src="https://avatars3.githubusercontent.com/u/159146?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Janne Härkönen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=yanne" title="Code">💻</a></td>
    <td align="center"><a href="http://xylix.fi"><img src="https://avatars1.githubusercontent.com/u/13387304?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Kerkko Pelttari</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=xylix" title="Code">💻</a></td>
    <td align="center"><a href="https://robocorp.com"><img src="https://avatars3.githubusercontent.com/u/54288445?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Robocorp</b></sub></a><br /><a href="#financial-robocorp" title="Financial">💵</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Snooz82"><img src="https://avatars0.githubusercontent.com/u/41592183?v=4?s=100" width="100px;" alt=""/><br /><sub><b>René</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Snooz82" title="Code">💻</a></td>
    <td align="center"><a href="https://wordpress.com/read/feeds/39696435"><img src="https://avatars0.githubusercontent.com/u/1123938?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Bryan Oakley</b></sub></a><br /><a href="#ideas-boakley" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/idxn"><img src="https://avatars3.githubusercontent.com/u/2438992?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Tanakiat Srisaranyakul</b></sub></a><br /><a href="#ideas-idxn" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://visible-quality.blogspot.com"><img src="https://avatars1.githubusercontent.com/u/5338157?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Maaret Pyhäjärvi</b></sub></a><br /><a href="#userTesting-maaretp" title="User Testing">📓</a></td>
    <td align="center"><a href="http://www.tentamen.eu"><img src="https://avatars2.githubusercontent.com/u/777520?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Karlo Smid</b></sub></a><br /><a href="#userTesting-karlosmid" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/aspargillus"><img src="https://avatars0.githubusercontent.com/u/4592889?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Frank Schimmel</b></sub></a><br /><a href="#userTesting-Aspargillus" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/tuxmux28"><img src="https://avatars3.githubusercontent.com/u/2794048?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Christoph</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=tuxmux28" title="Tests">⚠️</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/mikahanninen"><img src="https://avatars2.githubusercontent.com/u/1019528?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Mika Hänninen</b></sub></a><br /><a href="#question-mikahanninen" title="Answering Questions">💬</a></td>
    <td align="center"><a href="https://www.imbus.de"><img src="https://avatars0.githubusercontent.com/u/67375753?v=4?s=100" width="100px;" alt=""/><br /><sub><b>imbus</b></sub></a><br /><a href="#financial-imbus" title="Financial">💵</a></td>
    <td align="center"><a href="https://github.com/Finalrykku"><img src="https://avatars0.githubusercontent.com/u/19802569?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Niklas</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Finalrykku" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/gdroes"><img src="https://avatars1.githubusercontent.com/u/6716450?v=4?s=100" width="100px;" alt=""/><br /><sub><b>gdroes</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=gdroes" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://reaktor.com"><img src="https://avatars2.githubusercontent.com/u/71799?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Reaktor</b></sub></a><br /><a href="#financial-reaktor" title="Financial">💵</a></td>
    <td align="center"><a href="https://github.com/adrianyorke"><img src="https://avatars1.githubusercontent.com/u/30093433?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Adrian Yorke</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=adrianyorke" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/pulls?q=is%3Apr+reviewed-by%3Aadrianyorke" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/wangzimeiyingtao"><img src="https://avatars0.githubusercontent.com/u/70925596?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nanakawa</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=wangzimeiyingtao" title="Tests">⚠️</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/emanlove"><img src="https://avatars1.githubusercontent.com/u/993527?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ed Manlove</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=emanlove" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/estimation"><img src="https://avatars1.githubusercontent.com/u/16793171?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Brian Tsao</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aestimation" title="Bug reports">🐛</a> <a href="#userTesting-estimation" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/mawentao119"><img src="https://avatars0.githubusercontent.com/u/26617186?v=4?s=100" width="100px;" alt=""/><br /><sub><b>charis</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=mawentao119" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/s-galante"><img src="https://avatars2.githubusercontent.com/u/4580052?v=4?s=100" width="100px;" alt=""/><br /><sub><b>s-galante</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3As-galante" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://www.elabit.de"><img src="https://avatars3.githubusercontent.com/u/1897410?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Simon Meggle</b></sub></a><br /><a href="#userTesting-simonmeggle" title="User Testing">📓</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Asimonmeggle" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/Anna-Gunda"><img src="https://avatars3.githubusercontent.com/u/13298792?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Anna-Gunda</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAnna-Gunda" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/anton264"><img src="https://avatars0.githubusercontent.com/u/10194266?v=4?s=100" width="100px;" alt=""/><br /><sub><b>anton264</b></sub></a><br /><a href="#userTesting-anton264" title="User Testing">📓</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/emakaay"><img src="https://avatars.githubusercontent.com/u/72747481?v=4?s=100" width="100px;" alt=""/><br /><sub><b>emakaay</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aemakaay" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://virvatuli.itch.io/"><img src="https://avatars.githubusercontent.com/u/29060467?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nea Ohvo</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AVirvatuli" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/leeuwe"><img src="https://avatars.githubusercontent.com/u/66635066?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Elout van Leeuwen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=leeuwe" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/LDerikx"><img src="https://avatars.githubusercontent.com/u/26576024?v=4?s=100" width="100px;" alt=""/><br /><sub><b>LDerikx</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=LDerikx" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/olga-"><img src="https://avatars.githubusercontent.com/u/9334057?v=4?s=100" width="100px;" alt=""/><br /><sub><b>olga-</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=olga-" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aolga-" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/bollwyvl"><img src="https://avatars.githubusercontent.com/u/45380?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nicholas Bollweg</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=bollwyvl" title="Documentation">📖</a></td>
    <td align="center"><a href="http://villesalonen.fi"><img src="https://avatars.githubusercontent.com/u/1070813?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ville Salonen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AVilleSalonen" title="Bug reports">🐛</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://rasjani.github.io"><img src="https://avatars.githubusercontent.com/u/27887?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jani Mikkonen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arasjani" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/JaPyR"><img src="https://avatars.githubusercontent.com/u/7773301?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Aleh Borysiewicz</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AJaPyR" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://www.binary-overflow.de"><img src="https://avatars.githubusercontent.com/u/25060709?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jürgen Knauth</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajkpubsrc" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/dalaakso"><img src="https://avatars.githubusercontent.com/u/50731554?v=4?s=100" width="100px;" alt=""/><br /><sub><b>dalaakso</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Adalaakso" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/msirkka"><img src="https://avatars.githubusercontent.com/u/84907426?v=4?s=100" width="100px;" alt=""/><br /><sub><b>msirkka</b></sub></a><br /><a href="#ideas-msirkka" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/osrjv"><img src="https://avatars.githubusercontent.com/u/29481017?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ossi R.</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=osrjv" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/adrian-evo"><img src="https://avatars.githubusercontent.com/u/19324942?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Adrian V.</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=adrian-evo" title="Code">💻</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aadrian-evo" title="Bug reports">🐛</a> <a href="#ideas-adrian-evo" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/ssallmen"><img src="https://avatars.githubusercontent.com/u/39527407?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sami Sallmén</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Assallmen" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://eliga.fi"><img src="https://avatars.githubusercontent.com/u/114985?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Pekka Klärck</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=pekkaklarck" title="Code">💻</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Apekkaklarck" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/janipalsamaki"><img src="https://avatars.githubusercontent.com/u/1157184?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jani Palsamäki</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajanipalsamaki" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/AllanMedeiros"><img src="https://avatars.githubusercontent.com/u/34678196?v=4?s=100" width="100px;" alt=""/><br /><sub><b>AllanMedeiros</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAllanMedeiros" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
