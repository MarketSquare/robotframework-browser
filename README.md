# robotframework-browser
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-170-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Version](https://img.shields.io/pypi/v/robotframework-browser.svg)](https://pypi.python.org/pypi/robotframework-browser)
[![Actions Status](https://github.com/MarketSquare/robotframework-browser/workflows/Continuous%20integration/badge.svg)](https://github.com/MarketSquare/robotframework-browser/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

----

[Robot Framework](https://robotframework.org) Browser library powered by [Playwright](https://playwright.dev/). Moving browser automation to year 2023!

Aiming for :rocket: speed, :white_check_mark: reliability and :microscope: visibility.

See [keyword documentation](https://marketsquare.github.io/robotframework-browser/Browser.html) and
[web page](https://robotframework-browser.org/) for more details.

# Installation instructions

Only Python 3.9 or newer is supported. From Node side 18, 20 and 22 LTS versions are supported.

1. Install node.js e.g. from https://nodejs.org/en/download/
2. Update pip `pip install -U pip` to ensure latest version is used
3. Install robotframework-browser from the commandline: `pip install robotframework-browser`
4. Install the node dependencies: run `rfbrowser init` in your shell
  - if `rfbrowser` is not found, try `python -m Browser.entry init`

Please note that by default Chromium, Firefox and WebKit browser are installed, even those would be already
installed in the system. The installation size depends on the operating system, but usually is +700Mb.
It is possible to skip browser binaries installation with `rfbrowser init --skip-browsers` command, but then user
is responsible for browser binary installation. It is possible to install only selected browser binaries by adding
`chromium`, `firefox` or `webkit` as arguments to init command. Example `rfbrowser init firefox` would install
only Firefox binaries and `rfbrowser init firefox chromium` would install both Firefox and Chromium binaries.

Or use the [docker images](https://github.com/MarketSquare/robotframework-browser/pkgs/container/robotframework-browser%2Frfbrowser-stable). Documented at [docker/README.md](https://github.com/MarketSquare/robotframework-browser/blob/main/docker/README.md).

## Install with transformer

Starting from release 18.3.0 Browser library has optional dependency with
[Robotidy](https://robotidy.readthedocs.io/en/stable/). Install library with Robotidy, run install with:
`pip install robotframework-browser[tidy]`. Starting from 18.3.0 release, library will provide external
Robotidy [transformer](https://robotidy.readthedocs.io/en/stable/external_transformers.html). Transformer provided
by Browser library can be run with command: `rfbrowser transform --transformer-name /path/to/tests`. Example:
`rfbrowser transform --wait-until-network-is-idle /path/to/tests` would transform deprecated `Wait Until Network Is Idle`
keyword to `Wait For Load State` keyword. To see full list of transformers provided by Browser library, run
command: `rfbrowser transform --help`.

## Update instructions

To upgrade your already installed robotframework-browser library

1. Update from commandline: `pip install -U robotframework-browser`
2. Clean old node side dependencies and browser binaries: `rfbrowser clean-node`
3. Install the node dependencies for the newly installed version: `rfbrowser init`

## Uninstall instructions

To completely uninstall library, including the browser binaries installed by Playwright,
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
Evaluate JavaScript    ${ref}    (elem) => elem.innerText = "abc"
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
${response}=    HTTP    /api/post    POST    {"name": "John"}
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
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mkorpela"><img src="https://avatars1.githubusercontent.com/u/136885?v=4?s=100" width="100px;" alt="Mikko Korpela"/><br /><sub><b>Mikko Korpela</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=mkorpela" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aaltat"><img src="https://avatars0.githubusercontent.com/u/2665023?v=4?s=100" width="100px;" alt="Tatu Aalto"/><br /><sub><b>Tatu Aalto</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=aaltat" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://robocorp.com"><img src="https://avatars1.githubusercontent.com/u/8512727?v=4?s=100" width="100px;" alt="Antti Karjalainen"/><br /><sub><b>Antti Karjalainen</b></sub></a><br /><a href="#fundingFinding-aikarjal" title="Funding Finding">🔍</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/ismoaro/"><img src="https://avatars2.githubusercontent.com/u/1047173?v=4?s=100" width="100px;" alt="Ismo Aro"/><br /><sub><b>Ismo Aro</b></sub></a><br /><a href="#fundingFinding-IsNoGood" title="Funding Finding">🔍</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://twitter.com/janneharkonen"><img src="https://avatars3.githubusercontent.com/u/159146?v=4?s=100" width="100px;" alt="Janne Härkönen"/><br /><sub><b>Janne Härkönen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=yanne" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://xylix.fi"><img src="https://avatars1.githubusercontent.com/u/13387304?v=4?s=100" width="100px;" alt="Kerkko Pelttari"/><br /><sub><b>Kerkko Pelttari</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=xylix" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://robocorp.com"><img src="https://avatars3.githubusercontent.com/u/54288445?v=4?s=100" width="100px;" alt="Robocorp"/><br /><sub><b>Robocorp</b></sub></a><br /><a href="#financial-robocorp" title="Financial">💵</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Snooz82"><img src="https://avatars0.githubusercontent.com/u/41592183?v=4?s=100" width="100px;" alt="René"/><br /><sub><b>René</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Snooz82" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://wordpress.com/read/feeds/39696435"><img src="https://avatars0.githubusercontent.com/u/1123938?v=4?s=100" width="100px;" alt="Bryan Oakley"/><br /><sub><b>Bryan Oakley</b></sub></a><br /><a href="#ideas-boakley" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/idxn"><img src="https://avatars3.githubusercontent.com/u/2438992?v=4?s=100" width="100px;" alt="Tanakiat Srisaranyakul"/><br /><sub><b>Tanakiat Srisaranyakul</b></sub></a><br /><a href="#ideas-idxn" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://visible-quality.blogspot.com"><img src="https://avatars1.githubusercontent.com/u/5338157?v=4?s=100" width="100px;" alt="Maaret Pyhäjärvi"/><br /><sub><b>Maaret Pyhäjärvi</b></sub></a><br /><a href="#userTesting-maaretp" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.tentamen.eu"><img src="https://avatars2.githubusercontent.com/u/777520?v=4?s=100" width="100px;" alt="Karlo Smid"/><br /><sub><b>Karlo Smid</b></sub></a><br /><a href="#userTesting-karlosmid" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aspargillus"><img src="https://avatars0.githubusercontent.com/u/4592889?v=4?s=100" width="100px;" alt="Frank Schimmel"/><br /><sub><b>Frank Schimmel</b></sub></a><br /><a href="#userTesting-Aspargillus" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tuxmux28"><img src="https://avatars3.githubusercontent.com/u/2794048?v=4?s=100" width="100px;" alt="Christoph"/><br /><sub><b>Christoph</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=tuxmux28" title="Tests">⚠️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikahanninen"><img src="https://avatars2.githubusercontent.com/u/1019528?v=4?s=100" width="100px;" alt="Mika Hänninen"/><br /><sub><b>Mika Hänninen</b></sub></a><br /><a href="#question-mikahanninen" title="Answering Questions">💬</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.imbus.de"><img src="https://avatars0.githubusercontent.com/u/67375753?v=4?s=100" width="100px;" alt="imbus"/><br /><sub><b>imbus</b></sub></a><br /><a href="#financial-imbus" title="Financial">💵</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Finalrykku"><img src="https://avatars0.githubusercontent.com/u/19802569?v=4?s=100" width="100px;" alt="Niklas"/><br /><sub><b>Niklas</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Finalrykku" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gdroes"><img src="https://avatars1.githubusercontent.com/u/6716450?v=4?s=100" width="100px;" alt="gdroes"/><br /><sub><b>gdroes</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=gdroes" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://reaktor.com"><img src="https://avatars2.githubusercontent.com/u/71799?v=4?s=100" width="100px;" alt="Reaktor"/><br /><sub><b>Reaktor</b></sub></a><br /><a href="#financial-reaktor" title="Financial">💵</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adrianyorke"><img src="https://avatars1.githubusercontent.com/u/30093433?v=4?s=100" width="100px;" alt="Adrian Yorke"/><br /><sub><b>Adrian Yorke</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=adrianyorke" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/pulls?q=is%3Apr+reviewed-by%3Aadrianyorke" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wangzimeiyingtao"><img src="https://avatars0.githubusercontent.com/u/70925596?v=4?s=100" width="100px;" alt="Nanakawa"/><br /><sub><b>Nanakawa</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=wangzimeiyingtao" title="Tests">⚠️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/emanlove"><img src="https://avatars1.githubusercontent.com/u/993527?v=4?s=100" width="100px;" alt="Ed Manlove"/><br /><sub><b>Ed Manlove</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=emanlove" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aemanlove" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/estimation"><img src="https://avatars1.githubusercontent.com/u/16793171?v=4?s=100" width="100px;" alt="Brian Tsao"/><br /><sub><b>Brian Tsao</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aestimation" title="Bug reports">🐛</a> <a href="#userTesting-estimation" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mawentao119"><img src="https://avatars0.githubusercontent.com/u/26617186?v=4?s=100" width="100px;" alt="charis"/><br /><sub><b>charis</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=mawentao119" title="Code">💻</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amawentao119" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/s-galante"><img src="https://avatars2.githubusercontent.com/u/4580052?v=4?s=100" width="100px;" alt="s-galante"/><br /><sub><b>s-galante</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3As-galante" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.elabit.de"><img src="https://avatars3.githubusercontent.com/u/1897410?v=4?s=100" width="100px;" alt="Simon Meggle"/><br /><sub><b>Simon Meggle</b></sub></a><br /><a href="#userTesting-simonmeggle" title="User Testing">📓</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Asimonmeggle" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=simonmeggle" title="Tests">⚠️</a> <a href="#ideas-simonmeggle" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Anna-Gunda"><img src="https://avatars3.githubusercontent.com/u/13298792?v=4?s=100" width="100px;" alt="Anna-Gunda"/><br /><sub><b>Anna-Gunda</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAnna-Gunda" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/anton264"><img src="https://avatars0.githubusercontent.com/u/10194266?v=4?s=100" width="100px;" alt="anton264"/><br /><sub><b>anton264</b></sub></a><br /><a href="#userTesting-anton264" title="User Testing">📓</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/emakaay"><img src="https://avatars.githubusercontent.com/u/72747481?v=4?s=100" width="100px;" alt="emakaay"/><br /><sub><b>emakaay</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aemakaay" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://virvatuli.itch.io/"><img src="https://avatars.githubusercontent.com/u/29060467?v=4?s=100" width="100px;" alt="Nea Ohvo"/><br /><sub><b>Nea Ohvo</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AVirvatuli" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/leeuwe"><img src="https://avatars.githubusercontent.com/u/66635066?v=4?s=100" width="100px;" alt="Elout van Leeuwen"/><br /><sub><b>Elout van Leeuwen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=leeuwe" title="Documentation">📖</a> <a href="#ideas-leeuwe" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=leeuwe" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/LDerikx"><img src="https://avatars.githubusercontent.com/u/26576024?v=4?s=100" width="100px;" alt="LDerikx"/><br /><sub><b>LDerikx</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=LDerikx" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/olga-"><img src="https://avatars.githubusercontent.com/u/9334057?v=4?s=100" width="100px;" alt="olga-"/><br /><sub><b>olga-</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=olga-" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aolga-" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bollwyvl"><img src="https://avatars.githubusercontent.com/u/45380?v=4?s=100" width="100px;" alt="Nicholas Bollweg"/><br /><sub><b>Nicholas Bollweg</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=bollwyvl" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://villesalonen.fi"><img src="https://avatars.githubusercontent.com/u/1070813?v=4?s=100" width="100px;" alt="Ville Salonen"/><br /><sub><b>Ville Salonen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AVilleSalonen" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://rasjani.github.io"><img src="https://avatars.githubusercontent.com/u/27887?v=4?s=100" width="100px;" alt="Jani Mikkonen"/><br /><sub><b>Jani Mikkonen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arasjani" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=rasjani" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JaPyR"><img src="https://avatars.githubusercontent.com/u/7773301?v=4?s=100" width="100px;" alt="Aleh Borysiewicz"/><br /><sub><b>Aleh Borysiewicz</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AJaPyR" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.binary-overflow.de"><img src="https://avatars.githubusercontent.com/u/25060709?v=4?s=100" width="100px;" alt="Jürgen Knauth"/><br /><sub><b>Jürgen Knauth</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajkpubsrc" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dalaakso"><img src="https://avatars.githubusercontent.com/u/50731554?v=4?s=100" width="100px;" alt="dalaakso"/><br /><sub><b>dalaakso</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Adalaakso" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/msirkka"><img src="https://avatars.githubusercontent.com/u/84907426?v=4?s=100" width="100px;" alt="msirkka"/><br /><sub><b>msirkka</b></sub></a><br /><a href="#ideas-msirkka" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/osrjv"><img src="https://avatars.githubusercontent.com/u/29481017?v=4?s=100" width="100px;" alt="Ossi R."/><br /><sub><b>Ossi R.</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=osrjv" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adrian-evo"><img src="https://avatars.githubusercontent.com/u/19324942?v=4?s=100" width="100px;" alt="Adrian V."/><br /><sub><b>Adrian V.</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=adrian-evo" title="Code">💻</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aadrian-evo" title="Bug reports">🐛</a> <a href="#ideas-adrian-evo" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ssallmen"><img src="https://avatars.githubusercontent.com/u/39527407?v=4?s=100" width="100px;" alt="Sami Sallmén"/><br /><sub><b>Sami Sallmén</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Assallmen" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=ssallmen" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://eliga.fi"><img src="https://avatars.githubusercontent.com/u/114985?v=4?s=100" width="100px;" alt="Pekka Klärck"/><br /><sub><b>Pekka Klärck</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=pekkaklarck" title="Code">💻</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Apekkaklarck" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/janipalsamaki"><img src="https://avatars.githubusercontent.com/u/1157184?v=4?s=100" width="100px;" alt="Jani Palsamäki"/><br /><sub><b>Jani Palsamäki</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajanipalsamaki" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AllanMedeiros"><img src="https://avatars.githubusercontent.com/u/34678196?v=4?s=100" width="100px;" alt="AllanMedeiros"/><br /><sub><b>AllanMedeiros</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAllanMedeiros" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ealap"><img src="https://avatars.githubusercontent.com/u/15620712?v=4?s=100" width="100px;" alt="Emmanuel Alap"/><br /><sub><b>Emmanuel Alap</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aealap" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=ealap" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ankurbhalla-gmail"><img src="https://avatars.githubusercontent.com/u/90744440?v=4?s=100" width="100px;" alt="ankurbhalla-gmail"/><br /><sub><b>ankurbhalla-gmail</b></sub></a><br /><a href="#ideas-ankurbhalla-gmail" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/UliSei"><img src="https://avatars.githubusercontent.com/u/89480399?v=4?s=100" width="100px;" alt="UliSei"/><br /><sub><b>UliSei</b></sub></a><br /><a href="#ideas-UliSei" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AUliSei" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=UliSei" title="Code">💻</a> <a href="#userTesting-UliSei" title="User Testing">📓</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tomekTieto"><img src="https://avatars.githubusercontent.com/u/39945193?v=4?s=100" width="100px;" alt="Tomasz Pawlak"/><br /><sub><b>Tomasz Pawlak</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AtomekTieto" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mtoskamp"><img src="https://avatars.githubusercontent.com/u/58772827?v=4?s=100" width="100px;" alt="mtoskamp"/><br /><sub><b>mtoskamp</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amtoskamp" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/zastress"><img src="https://avatars.githubusercontent.com/u/37159441?v=4?s=100" width="100px;" alt="zastress"/><br /><sub><b>zastress</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Azastress" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://paazmaya.fi"><img src="https://avatars.githubusercontent.com/u/369881?v=4?s=100" width="100px;" alt="Juga Paazmaya"/><br /><sub><b>Juga Paazmaya</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=paazmaya" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Leemur89"><img src="https://avatars.githubusercontent.com/u/26330630?v=4?s=100" width="100px;" alt="Raphael Smadja"/><br /><sub><b>Raphael Smadja</b></sub></a><br /><a href="#ideas-Leemur89" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Leemur89" title="Code">💻</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ALeemur89" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Pakkanen1"><img src="https://avatars.githubusercontent.com/u/5936882?v=4?s=100" width="100px;" alt="Antti Pakkanen"/><br /><sub><b>Antti Pakkanen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3APakkanen1" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luchoagomezt"><img src="https://avatars.githubusercontent.com/u/4672517?v=4?s=100" width="100px;" alt="Luis A Gomez-Tinoco"/><br /><sub><b>Luis A Gomez-Tinoco</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aluchoagomezt" title="Bug reports">🐛</a> <a href="#example-luchoagomezt" title="Examples">💡</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=luchoagomezt" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ePlanLori"><img src="https://avatars.githubusercontent.com/u/61252623?v=4?s=100" width="100px;" alt="ePlanLori"/><br /><sub><b>ePlanLori</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AePlanLori" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/laguna357"><img src="https://avatars.githubusercontent.com/u/86680503?v=4?s=100" width="100px;" alt="laguna357"/><br /><sub><b>laguna357</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Alaguna357" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/GavinRodgers-EN0055"><img src="https://avatars.githubusercontent.com/u/72198546?v=4?s=100" width="100px;" alt="Gavin Rodgers"/><br /><sub><b>Gavin Rodgers</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AGavinRodgers-EN0055" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pokaalinkanssayohon"><img src="https://avatars.githubusercontent.com/u/34340500?v=4?s=100" width="100px;" alt="pokaalinkanssayohon"/><br /><sub><b>pokaalinkanssayohon</b></sub></a><br /><a href="#ideas-pokaalinkanssayohon" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rsandbach"><img src="https://avatars.githubusercontent.com/u/8907955?v=4?s=100" width="100px;" alt="Ryan Sandbach"/><br /><sub><b>Ryan Sandbach</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arsandbach" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=rsandbach" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Kahiis"><img src="https://avatars.githubusercontent.com/u/26903759?v=4?s=100" width="100px;" alt="Niko Kahilainen"/><br /><sub><b>Niko Kahilainen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AKahiis" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.loire-atlantique.fr/"><img src="https://avatars.githubusercontent.com/u/29864642?v=4?s=100" width="100px;" alt="Guillaume Gautier"/><br /><sub><b>Guillaume Gautier</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=GuillaumeGautierLA" title="Documentation">📖</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/robinmatz"><img src="https://avatars.githubusercontent.com/u/76647407?v=4?s=100" width="100px;" alt="Robin Matz"/><br /><sub><b>Robin Matz</b></sub></a><br /><a href="#ideas-robinmatz" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/stdedos"><img src="https://avatars.githubusercontent.com/u/133706?v=4?s=100" width="100px;" alt="Stavros Ntentos"/><br /><sub><b>Stavros Ntentos</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=stdedos" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Massukio"><img src="https://avatars.githubusercontent.com/u/13176540?v=4?s=100" width="100px;" alt="Massukio"/><br /><sub><b>Massukio</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AMassukio" title="Bug reports">🐛</a> <a href="#ideas-Massukio" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Atihinen"><img src="https://avatars.githubusercontent.com/u/5866905?v=4?s=100" width="100px;" alt="Atihinen"/><br /><sub><b>Atihinen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAtihinen" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gvr-kumar"><img src="https://avatars.githubusercontent.com/u/11802756?v=4?s=100" width="100px;" alt="gvrkumar"/><br /><sub><b>gvrkumar</b></sub></a><br /><a href="#ideas-gvr-kumar" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/laurihelkkula"><img src="https://avatars.githubusercontent.com/u/26920007?v=4?s=100" width="100px;" alt="Lauri Helkkula"/><br /><sub><b>Lauri Helkkula</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Alaurihelkkula" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rlall07"><img src="https://avatars.githubusercontent.com/u/20052315?v=4?s=100" width="100px;" alt="rlall07"/><br /><sub><b>rlall07</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arlall07" title="Bug reports">🐛</a> <a href="#ideas-rlall07" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://medium.com/@eldadu1985"><img src="https://avatars.githubusercontent.com/u/55621402?v=4?s=100" width="100px;" alt="Eldad Uzman"/><br /><sub><b>Eldad Uzman</b></sub></a><br /><a href="#ideas-eldaduzman" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mgarcibu"><img src="https://avatars.githubusercontent.com/u/41591471?v=4?s=100" width="100px;" alt="mgarcibu"/><br /><sub><b>mgarcibu</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amgarcibu" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dgalezow"><img src="https://avatars.githubusercontent.com/u/48494061?v=4?s=100" width="100px;" alt="DominikG"/><br /><sub><b>DominikG</b></sub></a><br /><a href="#ideas-dgalezow" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jokinr"><img src="https://avatars.githubusercontent.com/u/46047015?v=4?s=100" width="100px;" alt="jokinr"/><br /><sub><b>jokinr</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=jokinr" title="Tests">⚠️</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajokinr" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jchenuw"><img src="https://avatars.githubusercontent.com/u/29134340?v=4?s=100" width="100px;" alt="Jier Chen"/><br /><sub><b>Jier Chen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=jchenuw" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/IDvoe"><img src="https://avatars.githubusercontent.com/u/104168783?v=4?s=100" width="100px;" alt="IDvoe"/><br /><sub><b>IDvoe</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AIDvoe" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://cosmins.life"><img src="https://avatars.githubusercontent.com/u/709053?v=4?s=100" width="100px;" alt="Cosmin Poieana"/><br /><sub><b>Cosmin Poieana</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Acmin764" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/shenthils"><img src="https://avatars.githubusercontent.com/u/68647820?v=4?s=100" width="100px;" alt="Shenthil"/><br /><sub><b>Shenthil</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ashenthils" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mardukbp"><img src="https://avatars.githubusercontent.com/u/1140106?v=4?s=100" width="100px;" alt="Marduk Bolaños"/><br /><sub><b>Marduk Bolaños</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amardukbp" title="Bug reports">🐛</a> <a href="#ideas-mardukbp" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/amodzelewski"><img src="https://avatars.githubusercontent.com/u/35276905?v=4?s=100" width="100px;" alt="amodzelewski"/><br /><sub><b>amodzelewski</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aamodzelewski" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/TimDicos"><img src="https://avatars.githubusercontent.com/u/106802639?v=4?s=100" width="100px;" alt="TimDicos"/><br /><sub><b>TimDicos</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ATimDicos" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vinismarques"><img src="https://avatars.githubusercontent.com/u/33668018?v=4?s=100" width="100px;" alt="vinismarques"/><br /><sub><b>vinismarques</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Avinismarques" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nizwiz"><img src="https://avatars.githubusercontent.com/u/19755352?v=4?s=100" width="100px;" alt="nizwiz"/><br /><sub><b>nizwiz</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Anizwiz" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Reddriver"><img src="https://avatars.githubusercontent.com/u/7867213?v=4?s=100" width="100px;" alt="Reddriver"/><br /><sub><b>Reddriver</b></sub></a><br /><a href="#ideas-Reddriver" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SeppoTuura"><img src="https://avatars.githubusercontent.com/u/105704978?v=4?s=100" width="100px;" alt="Seppo"/><br /><sub><b>Seppo</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ASeppoTuura" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rousku"><img src="https://avatars.githubusercontent.com/u/2264792?v=4?s=100" width="100px;" alt="rousku"/><br /><sub><b>rousku</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arousku" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tomaspekarovic"><img src="https://avatars.githubusercontent.com/u/68331267?v=4?s=100" width="100px;" alt="tomaspekarovic"/><br /><sub><b>tomaspekarovic</b></sub></a><br /><a href="#ideas-tomaspekarovic" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/robinmackaij-kadaster"><img src="https://avatars.githubusercontent.com/u/97301504?v=4?s=100" width="100px;" alt="Robin Mackaij"/><br /><sub><b>Robin Mackaij</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Arobinmackaij-kadaster" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nixuewei"><img src="https://avatars.githubusercontent.com/u/20495497?v=4?s=100" width="100px;" alt="nixuewei"/><br /><sub><b>nixuewei</b></sub></a><br /><a href="#ideas-nixuewei" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/slavaGanzin"><img src="https://avatars.githubusercontent.com/u/1011721?v=4?s=100" width="100px;" alt="Slava"/><br /><sub><b>Slava</b></sub></a><br /><a href="#ideas-slavaGanzin" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AslavaGanzin" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=slavaGanzin" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kariharju"><img src="https://avatars.githubusercontent.com/u/56814402?v=4?s=100" width="100px;" alt="Kari Harju"/><br /><sub><b>Kari Harju</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Akariharju" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/you"><img src="https://avatars.githubusercontent.com/u/57100752?v=4?s=100" width="100px;" alt="you"/><br /><sub><b>you</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ayou" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/axiom41"><img src="https://avatars.githubusercontent.com/u/9963199?v=4?s=100" width="100px;" alt="axiom41"/><br /><sub><b>axiom41</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aaxiom41" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/amankul"><img src="https://avatars.githubusercontent.com/u/43149375?v=4?s=100" width="100px;" alt="amankul"/><br /><sub><b>amankul</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aamankul" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jcb-entrnce"><img src="https://avatars.githubusercontent.com/u/73102679?v=4?s=100" width="100px;" alt="jcb-entrnce"/><br /><sub><b>jcb-entrnce</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajcb-entrnce" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Remppa"><img src="https://avatars.githubusercontent.com/u/17778362?v=4?s=100" width="100px;" alt="Remppa"/><br /><sub><b>Remppa</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ARemppa" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tomekPawlak"><img src="https://avatars.githubusercontent.com/u/39945193?v=4?s=100" width="100px;" alt="Tomasz Pawlak"/><br /><sub><b>Tomasz Pawlak</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AtomekPawlak" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/stude1"><img src="https://avatars.githubusercontent.com/u/5876939?v=4?s=100" width="100px;" alt="Timo Stordell"/><br /><sub><b>Timo Stordell</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Astude1" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MarcinGmurczyk"><img src="https://avatars.githubusercontent.com/u/11760932?v=4?s=100" width="100px;" alt="Marcin Gmurczyk"/><br /><sub><b>Marcin Gmurczyk</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=MarcinGmurczyk" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.imbus.de"><img src="https://avatars.githubusercontent.com/u/7069968?v=4?s=100" width="100px;" alt="Daniel Biehl"/><br /><sub><b>Daniel Biehl</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ad-biehl" title="Bug reports">🐛</a> <a href="#ideas-d-biehl" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rarajabs"><img src="https://avatars.githubusercontent.com/u/1460421?v=4?s=100" width="100px;" alt="rarajabs"/><br /><sub><b>rarajabs</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ararajabs" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sandeepvaidya"><img src="https://avatars.githubusercontent.com/u/6525205?v=4?s=100" width="100px;" alt="Sandeep Vaidya"/><br /><sub><b>Sandeep Vaidya</b></sub></a><br /><a href="#ideas-sandeepvaidya" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/falk7"><img src="https://avatars.githubusercontent.com/u/61115124?v=4?s=100" width="100px;" alt="falk"/><br /><sub><b>falk</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=falk7" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ciadoh"><img src="https://avatars.githubusercontent.com/u/68943309?v=4?s=100" width="100px;" alt="ciadoh"/><br /><sub><b>ciadoh</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aciadoh" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/johanvaniperen"><img src="https://avatars.githubusercontent.com/u/36015334?v=4?s=100" width="100px;" alt="Johan van Iperen"/><br /><sub><b>Johan van Iperen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=johanvaniperen" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fabioz"><img src="https://avatars.githubusercontent.com/u/117621?v=4?s=100" width="100px;" alt="Fabio Zadrozny"/><br /><sub><b>Fabio Zadrozny</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Afabioz" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BCGST"><img src="https://avatars.githubusercontent.com/u/105816460?v=4?s=100" width="100px;" alt="BCGST"/><br /><sub><b>BCGST</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=BCGST" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wvanasten"><img src="https://avatars.githubusercontent.com/u/93996238?v=4?s=100" width="100px;" alt="Wilfried van Asten"/><br /><sub><b>Wilfried van Asten</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Awvanasten" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=wvanasten" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.vizrt.com/"><img src="https://avatars.githubusercontent.com/u/20283377?v=4?s=100" width="100px;" alt="Mikal H Henriksen"/><br /><sub><b>Mikal H Henriksen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AMHHenriksen" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alexinoDr"><img src="https://avatars.githubusercontent.com/u/126524368?v=4?s=100" width="100px;" alt="alexinoDr"/><br /><sub><b>alexinoDr</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AalexinoDr" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/trybuskrzysztof"><img src="https://avatars.githubusercontent.com/u/27352125?v=4?s=100" width="100px;" alt="trybuskrzysztof"/><br /><sub><b>trybuskrzysztof</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Atrybuskrzysztof" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Aino1980"><img src="https://avatars.githubusercontent.com/u/25761977?v=4?s=100" width="100px;" alt="Aino1980"/><br /><sub><b>Aino1980</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAino1980" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BjornAhmark"><img src="https://avatars.githubusercontent.com/u/134600409?v=4?s=100" width="100px;" alt="BjornAhmark"/><br /><sub><b>BjornAhmark</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ABjornAhmark" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Mezohren"><img src="https://avatars.githubusercontent.com/u/135019714?v=4?s=100" width="100px;" alt="Mezohren"/><br /><sub><b>Mezohren</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AMezohren" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://zouper.cn"><img src="https://avatars.githubusercontent.com/u/29817738?v=4?s=100" width="100px;" alt="Zoupers Zou"/><br /><sub><b>Zoupers Zou</b></sub></a><br /><a href="#ideas-Zoupers" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lasselindqvist"><img src="https://avatars.githubusercontent.com/u/13466645?v=4?s=100" width="100px;" alt="lasselindqvist"/><br /><sub><b>lasselindqvist</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Alasselindqvist" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/david-ns"><img src="https://avatars.githubusercontent.com/u/50212780?v=4?s=100" width="100px;" alt="David Nieto Sanz"/><br /><sub><b>David Nieto Sanz</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Adavid-ns" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://gil.badall.net"><img src="https://avatars.githubusercontent.com/u/1155680?v=4?s=100" width="100px;" alt="Gil Forcada Codinachs"/><br /><sub><b>Gil Forcada Codinachs</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=gforcada" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Agforcada" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://nathanhannig.com"><img src="https://avatars.githubusercontent.com/u/8210763?v=4?s=100" width="100px;" alt="Nathan Hannig"/><br /><sub><b>Nathan Hannig</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Anathanhannig" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/madworx"><img src="https://avatars.githubusercontent.com/u/6368715?v=4?s=100" width="100px;" alt="Martin Kjellstrand"/><br /><sub><b>Martin Kjellstrand</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amadworx" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://medv.io"><img src="https://avatars.githubusercontent.com/u/141232?v=4?s=100" width="100px;" alt="Anton Medvedev"/><br /><sub><b>Anton Medvedev</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=antonmedv" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/martamedovova-ext91522"><img src="https://avatars.githubusercontent.com/u/130643867?v=4?s=100" width="100px;" alt="martamedovova-ext91522"/><br /><sub><b>martamedovova-ext91522</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amartamedovova-ext91522" title="Bug reports">🐛</a> <a href="#ideas-martamedovova-ext91522" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/DirkRichter"><img src="https://avatars.githubusercontent.com/u/20930315?v=4?s=100" width="100px;" alt="Dr. Dirk Richter"/><br /><sub><b>Dr. Dirk Richter</b></sub></a><br /><a href="#ideas-DirkRichter" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/RatexMak"><img src="https://avatars.githubusercontent.com/u/33491425?v=4?s=100" width="100px;" alt="RatexMak"/><br /><sub><b>RatexMak</b></sub></a><br /><a href="#ideas-RatexMak" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/horzuff"><img src="https://avatars.githubusercontent.com/u/63282033?v=4?s=100" width="100px;" alt="horzuff"/><br /><sub><b>horzuff</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=horzuff" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/naibra"><img src="https://avatars.githubusercontent.com/u/76438934?v=4?s=100" width="100px;" alt="naibra"/><br /><sub><b>naibra</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Anaibra" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://aapee.kapsi.fi"><img src="https://avatars.githubusercontent.com/u/7158433?v=4?s=100" width="100px;" alt="Antti Pekka Vilkko"/><br /><sub><b>Antti Pekka Vilkko</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aapvilkko" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/infoTrainingym"><img src="https://avatars.githubusercontent.com/u/2445330?v=4?s=100" width="100px;" alt="Serafín Martín"/><br /><sub><b>Serafín Martín</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AinfoTrainingym" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JoostW21111"><img src="https://avatars.githubusercontent.com/u/130643234?v=4?s=100" width="100px;" alt="JoostW21111"/><br /><sub><b>JoostW21111</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AJoostW21111" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Camatius"><img src="https://avatars.githubusercontent.com/u/20600086?v=4?s=100" width="100px;" alt="Camatius"/><br /><sub><b>Camatius</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3ACamatius" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/terckert"><img src="https://avatars.githubusercontent.com/u/57592522?v=4?s=100" width="100px;" alt="terckert"/><br /><sub><b>terckert</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aterckert" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://mbondarew.dev"><img src="https://avatars.githubusercontent.com/u/6174054?v=4?s=100" width="100px;" alt="Maksim Bondarew"/><br /><sub><b>Maksim Bondarew</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ambondarew" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/HenrikSchuette"><img src="https://avatars.githubusercontent.com/u/98702737?v=4?s=100" width="100px;" alt="HenrikSchuette"/><br /><sub><b>HenrikSchuette</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AHenrikSchuette" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gbhandarkavathe"><img src="https://avatars.githubusercontent.com/u/130966766?v=4?s=100" width="100px;" alt="Gurunatharudh Bhandarkavathe(Infosys)"/><br /><sub><b>Gurunatharudh Bhandarkavathe(Infosys)</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Agbhandarkavathe" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alpip1997"><img src="https://avatars.githubusercontent.com/u/52825200?v=4?s=100" width="100px;" alt="alpip1997"/><br /><sub><b>alpip1997</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aalpip1997" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/terolindfors"><img src="https://avatars.githubusercontent.com/u/95089387?v=4?s=100" width="100px;" alt="terolindfors"/><br /><sub><b>terolindfors</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aterolindfors" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/TWijesundera"><img src="https://avatars.githubusercontent.com/u/21339656?v=4?s=100" width="100px;" alt="Thisara Wijesundera"/><br /><sub><b>Thisara Wijesundera</b></sub></a><br /><a href="#ideas-TWijesundera" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/masudparvez"><img src="https://avatars.githubusercontent.com/u/3022096?v=4?s=100" width="100px;" alt="masudparvez"/><br /><sub><b>masudparvez</b></sub></a><br /><a href="#ideas-masudparvez" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gitkatsi"><img src="https://avatars.githubusercontent.com/u/30192727?v=4?s=100" width="100px;" alt="gitkatsi"/><br /><sub><b>gitkatsi</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Agitkatsi" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=gitkatsi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/manykarim"><img src="https://avatars.githubusercontent.com/u/61293164?v=4?s=100" width="100px;" alt="Many Kasiriha"/><br /><sub><b>Many Kasiriha</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amanykarim" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/thulasiraju"><img src="https://avatars.githubusercontent.com/u/21201594?v=4?s=100" width="100px;" alt="Thulasi Raju"/><br /><sub><b>Thulasi Raju</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=thulasiraju" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://iliketomatoes.com/"><img src="https://avatars.githubusercontent.com/u/2039028?v=4?s=100" width="100px;" alt="Giancarlo Soverini"/><br /><sub><b>Giancarlo Soverini</b></sub></a><br /><a href="#ideas-iliketomatoes" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lennartq"><img src="https://avatars.githubusercontent.com/u/22813828?v=4?s=100" width="100px;" alt="lennartq"/><br /><sub><b>lennartq</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=lennartq" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/falcon030"><img src="https://avatars.githubusercontent.com/u/30448651?v=4?s=100" width="100px;" alt="Lukas Boekenoogen"/><br /><sub><b>Lukas Boekenoogen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=falcon030" title="Documentation">📖</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=falcon030" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/anacomparada"><img src="https://avatars.githubusercontent.com/u/166409747?v=4?s=100" width="100px;" alt="anacomparada"/><br /><sub><b>anacomparada</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aanacomparada" title="Bug reports">🐛</a> <a href="https://github.com/MarketSquare/robotframework-browser/commits?author=anacomparada" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/siongwai"><img src="https://avatars.githubusercontent.com/u/112995767?v=4?s=100" width="100px;" alt="siongwai"/><br /><sub><b>siongwai</b></sub></a><br /><a href="#ideas-siongwai" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Asiongwai" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nfaustin"><img src="https://avatars.githubusercontent.com/u/3782948?v=4?s=100" width="100px;" alt="nfaustin"/><br /><sub><b>nfaustin</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Anfaustin" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Shutgun"><img src="https://avatars.githubusercontent.com/u/20171515?v=4?s=100" width="100px;" alt="Guido Schmitz"/><br /><sub><b>Guido Schmitz</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Shutgun" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://cns.me"><img src="https://avatars.githubusercontent.com/u/715120?v=4?s=100" width="100px;" alt="Chris Nesbitt-Smith"/><br /><sub><b>Chris Nesbitt-Smith</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=chrisns" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vmmattila"><img src="https://avatars.githubusercontent.com/u/135705333?v=4?s=100" width="100px;" alt="vmmattila"/><br /><sub><b>vmmattila</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Avmmattila" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Andre-A-AtGithub"><img src="https://avatars.githubusercontent.com/u/172484553?v=4?s=100" width="100px;" alt="Andre-A-AtGithub"/><br /><sub><b>Andre-A-AtGithub</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AAndre-A-AtGithub" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Pawci3oo"><img src="https://avatars.githubusercontent.com/u/26310305?v=4?s=100" width="100px;" alt="Paweł"/><br /><sub><b>Paweł</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3APawci3oo" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/raphaelcamus"><img src="https://avatars.githubusercontent.com/u/164873162?v=4?s=100" width="100px;" alt="Raphael CAMUS"/><br /><sub><b>Raphael CAMUS</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Araphaelcamus" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Noordsestern"><img src="https://avatars.githubusercontent.com/u/5188411?v=4?s=100" width="100px;" alt="Markus"/><br /><sub><b>Markus</b></sub></a><br /><a href="#ideas-Noordsestern" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wojtekwp"><img src="https://avatars.githubusercontent.com/u/30738397?v=4?s=100" width="100px;" alt="wojtekwp"/><br /><sub><b>wojtekwp</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Awojtekwp" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Houbein"><img src="https://avatars.githubusercontent.com/u/60261063?v=4?s=100" width="100px;" alt="Rudolf"/><br /><sub><b>Rudolf</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AHoubein" title="Bug reports">🐛</a> <a href="#ideas-Houbein" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/henriquediassep"><img src="https://avatars.githubusercontent.com/u/17513934?v=4?s=100" width="100px;" alt="Henrique Branco"/><br /><sub><b>Henrique Branco</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ahenriquediassep" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mika-b"><img src="https://avatars.githubusercontent.com/u/29384035?v=4?s=100" width="100px;" alt="mika-b"/><br /><sub><b>mika-b</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Amika-b" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/okraus-ari"><img src="https://avatars.githubusercontent.com/u/176952405?v=4?s=100" width="100px;" alt="okraus-ari"/><br /><sub><b>okraus-ari</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=okraus-ari" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ecare-joost"><img src="https://avatars.githubusercontent.com/u/59823670?v=4?s=100" width="100px;" alt="ecare-joost"/><br /><sub><b>ecare-joost</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Aecare-joost" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/PaulBrandUWV"><img src="https://avatars.githubusercontent.com/u/160221050?v=4?s=100" width="100px;" alt="PaulBrandUWV"/><br /><sub><b>PaulBrandUWV</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3APaulBrandUWV" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ArttuKnowit"><img src="https://avatars.githubusercontent.com/u/105268255?v=4?s=100" width="100px;" alt="ArttuKnowit"/><br /><sub><b>ArttuKnowit</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AArttuKnowit" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tomppa65"><img src="https://avatars.githubusercontent.com/u/9744026?v=4?s=100" width="100px;" alt="T. Silvola"/><br /><sub><b>T. Silvola</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Atomppa65" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/teemuteemu"><img src="https://avatars.githubusercontent.com/u/2570951?v=4?s=100" width="100px;" alt="Teemu Kallio"/><br /><sub><b>Teemu Kallio</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ateemuteemu" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/joseajunior"><img src="https://avatars.githubusercontent.com/u/77733175?v=4?s=100" width="100px;" alt="José Almeida"/><br /><sub><b>José Almeida</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3Ajoseajunior" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/loomanw"><img src="https://avatars.githubusercontent.com/u/38555868?v=4?s=100" width="100px;" alt="William Looman"/><br /><sub><b>William Looman</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=loomanw" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mekxtari"><img src="https://avatars.githubusercontent.com/u/22319364?v=4?s=100" width="100px;" alt="mekxtari"/><br /><sub><b>mekxtari</b></sub></a><br /><a href="#ideas-mekxtari" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/keef78"><img src="https://avatars.githubusercontent.com/u/167465772?v=4?s=100" width="100px;" alt="keef78"/><br /><sub><b>keef78</b></sub></a><br /><a href="#ideas-keef78" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dean4711"><img src="https://avatars.githubusercontent.com/u/5942386?v=4?s=100" width="100px;" alt="André"/><br /><sub><b>André</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=dean4711" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MarvKler"><img src="https://avatars.githubusercontent.com/u/98239503?v=4?s=100" width="100px;" alt="MarvKler"/><br /><sub><b>MarvKler</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/issues?q=author%3AMarvKler" title="Bug reports">🐛</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
