# robotframework-browser
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-89-orange.svg?style=flat-square)](#contributors-)
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

1. Install node.js e.g. from https://nodejs.org/en/download/
2. Update pip `pip install -U pip` to ensure latest version is used
3. Install robotframework-browser from the commandline: `pip install robotframework-browser`
4. Install the node dependencies: run `rfbrowser init` in your shell
  - if `rfbrowser` is not found, try `python -m Browser.entry init`

Please note that by default Chromium, Firefox and WebKit browser are installed, even those would be already
installed in the system. The installation size depends on the operating system, but usually is +700Mb.
It is possible to skip browser binaries installation with `rfbrowser init --skip-browsers` command, but then user
is responsible for browser binary installation.

Or use the [docker images](https://github.com/MarketSquare/robotframework-browser/pkgs/container/robotframework-browser%2Frfbrowser-stable). Documented at [docker/README.md](https://github.com/MarketSquare/robotframework-browser/blob/main/docker/README.md).

## Update instructions

To upgrade your already installed robotframework-browser library

1. Update from commandline: `pip install -U robotframework-browser`
2. Clean old node side dependencies and browser binaries: `rfbrowser clean-node`
3. Install the node dependencies for the newly installed version: `rfbrowser init`

## Uninstall instructions

To completely install library, including the browser binaries installed by Playwright,
run following commands:
1. Clean old node side dependencies and browser binaries: `rfbrowser clean-node`
2. Uninstall with pip: `pip uninstall robotframework-browser`

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
async function myGoToKeyword(url, page, logger) {
    logger("Going to " + url)
    return await page.goto(url);
}
myGoToKeyword.rfdoc = "This is my own go to keyword";
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

See [example](https://github.com/MarketSquare/robotframework-browser/tree/main/docs/examples/babelES2015).
Ready made extensions and a place to share your own at [robotframework-browser-extensions](https://github.com/MarketSquare/robotframework-browser-extensions).

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

### Parallel test execution using Pabot

You can let RF Browser spawn separate processes for every pabot process. This is very simple, just run the tests normally using pabot (see https://github.com/mkorpela/pabot#basic-use ). However if you have small tests do not use `--testlevelsplit`, it will cause lots of overhead because tests cannot share the browsers in any case.

You can share the node side RF Browser processes by using the `ROBOT_FRAMEWORK_BROWSER_NODE_PORT` environment variable, and `from Browser.utils import spawn_node_process` helper ([see the docs for the helper](https://github.com/MarketSquare/robotframework-browser/blob/a7d3e59a1e8e3e75f64b9146a088385445a5af30/Browser/utils/misc.py#L35) ). This saves some overhead based on how many splits of tests you are running. Clean up the process afterwards.

### Re-using authentication credentials

- Figure out how the page is storing authentication
- If it is localstorage or cookies `Save Storage State` should work. See usage example: https://marketsquare.github.io/robotframework-browser/Browser.html#Save%20Storage%20State

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
  <tbody>
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
      <td align="center"><a href="https://github.com/emanlove"><img src="https://avatars1.githubusercontent.com/u/993527?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ed Manlove</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=emanlove" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aemanlove" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/estimation"><img src="https://avatars1.githubusercontent.com/u/16793171?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Brian Tsao</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aestimation" title="Bug reports">🐛</a> <a href="#userTesting-estimation" title="User Testing">📓</a></td>
      <td align="center"><a href="https://github.com/mawentao119"><img src="https://avatars0.githubusercontent.com/u/26617186?v=4?s=100" width="100px;" alt=""/><br /><sub><b>charis</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=mawentao119" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/s-galante"><img src="https://avatars2.githubusercontent.com/u/4580052?v=4?s=100" width="100px;" alt=""/><br /><sub><b>s-galante</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3As-galante" title="Bug reports">🐛</a></td>
      <td align="center"><a href="http://www.elabit.de"><img src="https://avatars3.githubusercontent.com/u/1897410?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Simon Meggle</b></sub></a><br /><a href="#userTesting-simonmeggle" title="User Testing">📓</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Asimonmeggle" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=simonmeggle" title="Tests">⚠️</a></td>
      <td align="center"><a href="https://github.com/Anna-Gunda"><img src="https://avatars3.githubusercontent.com/u/13298792?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Anna-Gunda</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAnna-Gunda" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/anton264"><img src="https://avatars0.githubusercontent.com/u/10194266?v=4?s=100" width="100px;" alt=""/><br /><sub><b>anton264</b></sub></a><br /><a href="#userTesting-anton264" title="User Testing">📓</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/emakaay"><img src="https://avatars.githubusercontent.com/u/72747481?v=4?s=100" width="100px;" alt=""/><br /><sub><b>emakaay</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aemakaay" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://virvatuli.itch.io/"><img src="https://avatars.githubusercontent.com/u/29060467?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nea Ohvo</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AVirvatuli" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/leeuwe"><img src="https://avatars.githubusercontent.com/u/66635066?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Elout van Leeuwen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=leeuwe" title="Documentation">📖</a> <a href="#ideas-leeuwe" title="Ideas, Planning, & Feedback">🤔</a></td>
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
      <td align="center"><a href="https://github.com/ealap"><img src="https://avatars.githubusercontent.com/u/15620712?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Emmanuel Alap</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aealap" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=ealap" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/ankurbhalla-gmail"><img src="https://avatars.githubusercontent.com/u/90744440?v=4?s=100" width="100px;" alt=""/><br /><sub><b>ankurbhalla-gmail</b></sub></a><br /><a href="#ideas-ankurbhalla-gmail" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/UliSei"><img src="https://avatars.githubusercontent.com/u/89480399?v=4?s=100" width="100px;" alt=""/><br /><sub><b>UliSei</b></sub></a><br /><a href="#ideas-UliSei" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AUliSei" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=UliSei" title="Code">💻</a> <a href="#userTesting-UliSei" title="User Testing">📓</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/tomekTieto"><img src="https://avatars.githubusercontent.com/u/39945193?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Tomasz Pawlak</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AtomekTieto" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/mtoskamp"><img src="https://avatars.githubusercontent.com/u/58772827?v=4?s=100" width="100px;" alt=""/><br /><sub><b>mtoskamp</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amtoskamp" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/zastress"><img src="https://avatars.githubusercontent.com/u/37159441?v=4?s=100" width="100px;" alt=""/><br /><sub><b>zastress</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Azastress" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://paazmaya.fi"><img src="https://avatars.githubusercontent.com/u/369881?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Juga Paazmaya</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=paazmaya" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/Leemur89"><img src="https://avatars.githubusercontent.com/u/26330630?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Raphael Smadja</b></sub></a><br /><a href="#ideas-Leemur89" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Leemur89" title="Code">💻</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ALeemur89" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/Pakkanen1"><img src="https://avatars.githubusercontent.com/u/5936882?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Antti Pakkanen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3APakkanen1" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/luchoagomezt"><img src="https://avatars.githubusercontent.com/u/4672517?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Luis A Gomez-Tinoco</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aluchoagomezt" title="Bug reports">🐛</a> <a href="#example-luchoagomezt" title="Examples">💡</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=luchoagomezt" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/ePlanLori"><img src="https://avatars.githubusercontent.com/u/61252623?v=4?s=100" width="100px;" alt=""/><br /><sub><b>ePlanLori</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AePlanLori" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/laguna357"><img src="https://avatars.githubusercontent.com/u/86680503?v=4?s=100" width="100px;" alt=""/><br /><sub><b>laguna357</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Alaguna357" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/GavinRodgers-EN0055"><img src="https://avatars.githubusercontent.com/u/72198546?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Gavin Rodgers</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AGavinRodgers-EN0055" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/pokaalinkanssayohon"><img src="https://avatars.githubusercontent.com/u/34340500?v=4?s=100" width="100px;" alt=""/><br /><sub><b>pokaalinkanssayohon</b></sub></a><br /><a href="#ideas-pokaalinkanssayohon" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/rsandbach"><img src="https://avatars.githubusercontent.com/u/8907955?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ryan Sandbach</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arsandbach" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=rsandbach" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/Kahiis"><img src="https://avatars.githubusercontent.com/u/26903759?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Niko Kahilainen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AKahiis" title="Bug reports">🐛</a></td>
      <td align="center"><a href="http://www.loire-atlantique.fr/"><img src="https://avatars.githubusercontent.com/u/29864642?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Guillaume Gautier</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=GuillaumeGautierLA" title="Documentation">📖</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/robinmatz"><img src="https://avatars.githubusercontent.com/u/76647407?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Robin Matz</b></sub></a><br /><a href="#ideas-robinmatz" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/stdedos"><img src="https://avatars.githubusercontent.com/u/133706?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Stavros Ntentos</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=stdedos" title="Documentation">📖</a></td>
      <td align="center"><a href="https://github.com/Massukio"><img src="https://avatars.githubusercontent.com/u/13176540?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Massukio</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AMassukio" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/Atihinen"><img src="https://avatars.githubusercontent.com/u/5866905?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Atihinen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAtihinen" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/gvr-kumar"><img src="https://avatars.githubusercontent.com/u/11802756?v=4?s=100" width="100px;" alt=""/><br /><sub><b>gvrkumar</b></sub></a><br /><a href="#ideas-gvr-kumar" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/laurihelkkula"><img src="https://avatars.githubusercontent.com/u/26920007?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Lauri Helkkula</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Alaurihelkkula" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/rlall07"><img src="https://avatars.githubusercontent.com/u/20052315?v=4?s=100" width="100px;" alt=""/><br /><sub><b>rlall07</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arlall07" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://medium.com/@eldadu1985"><img src="https://avatars.githubusercontent.com/u/55621402?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Eldad Uzman</b></sub></a><br /><a href="#ideas-eldaduzman" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/mgarcibu"><img src="https://avatars.githubusercontent.com/u/41591471?v=4?s=100" width="100px;" alt=""/><br /><sub><b>mgarcibu</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amgarcibu" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/dgalezow"><img src="https://avatars.githubusercontent.com/u/48494061?v=4?s=100" width="100px;" alt=""/><br /><sub><b>DominikG</b></sub></a><br /><a href="#ideas-dgalezow" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/jokinr"><img src="https://avatars.githubusercontent.com/u/46047015?v=4?s=100" width="100px;" alt=""/><br /><sub><b>jokinr</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=jokinr" title="Tests">⚠️</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajokinr" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/jchenuw"><img src="https://avatars.githubusercontent.com/u/29134340?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jier Chen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=jchenuw" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/IDvoe"><img src="https://avatars.githubusercontent.com/u/104168783?v=4?s=100" width="100px;" alt=""/><br /><sub><b>IDvoe</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AIDvoe" title="Bug reports">🐛</a></td>
      <td align="center"><a href="http://cosmins.life"><img src="https://avatars.githubusercontent.com/u/709053?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Cosmin Poieana</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Acmin764" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/shenthils"><img src="https://avatars.githubusercontent.com/u/68647820?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Shenthil</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ashenthils" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/mardukbp"><img src="https://avatars.githubusercontent.com/u/1140106?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Marduk Bolaños</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amardukbp" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/amodzelewski"><img src="https://avatars.githubusercontent.com/u/35276905?v=4?s=100" width="100px;" alt=""/><br /><sub><b>amodzelewski</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aamodzelewski" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/TimDicos"><img src="https://avatars.githubusercontent.com/u/106802639?v=4?s=100" width="100px;" alt=""/><br /><sub><b>TimDicos</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ATimDicos" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/vinismarques"><img src="https://avatars.githubusercontent.com/u/33668018?v=4?s=100" width="100px;" alt=""/><br /><sub><b>vinismarques</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Avinismarques" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/nizwiz"><img src="https://avatars.githubusercontent.com/u/19755352?v=4?s=100" width="100px;" alt=""/><br /><sub><b>nizwiz</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Anizwiz" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/Reddriver"><img src="https://avatars.githubusercontent.com/u/7867213?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Reddriver</b></sub></a><br /><a href="#ideas-Reddriver" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/SeppoTuura"><img src="https://avatars.githubusercontent.com/u/105704978?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Seppo</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ASeppoTuura" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/rousku"><img src="https://avatars.githubusercontent.com/u/2264792?v=4?s=100" width="100px;" alt=""/><br /><sub><b>rousku</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arousku" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/tomaspekarovic"><img src="https://avatars.githubusercontent.com/u/68331267?v=4?s=100" width="100px;" alt=""/><br /><sub><b>tomaspekarovic</b></sub></a><br /><a href="#ideas-tomaspekarovic" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/robinmackaij-kadaster"><img src="https://avatars.githubusercontent.com/u/97301504?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Robin Mackaij</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arobinmackaij-kadaster" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/nixuewei"><img src="https://avatars.githubusercontent.com/u/20495497?v=4?s=100" width="100px;" alt=""/><br /><sub><b>nixuewei</b></sub></a><br /><a href="#ideas-nixuewei" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
