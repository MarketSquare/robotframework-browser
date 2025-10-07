======================
Browser library 19.9.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.9.0 is a new release with
enhancement to distribute RF Browser fully bundled as wheel including external
NodeJS and NPM dependencies. Therefore there is new packaging called BrowserBatteries.
There are also other enhancements and fixes listed below. All issues targeted for Browser
library v19.9.0 can be found from the `issue tracker`_.
For first time installation with pip_ and BrowserBatteries just run
::
   pip install robotframework-browser robotframework-browser-batteries
   rfbrowser install
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser robotframework-browser-batteries
   rfbrowser clean-node
   rfbrowser install
For first time installation with pip_ with Browser library only, just run
::
   pip install robotframework-browser
   rfbrowser init
If you upgrading from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and
install it manually. Browser library 19.9.0 was released on Tuesday October 7, 2025.
Browser supports Python 3.9+, Node 20/22/24 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.56.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.9.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Distribute RF Browser fully bundled as wheel including external NodeJS and NPM dependencies  (`#4303`_)
-------------------------------------------------------------------------------------------------------
Because difficulties with installing NodeJS and npm dependencies, specially in corporate
environments, NodeJS and the NodeJS dependencies are now distributed as part of the BrowserBatteries
wheel. This makes installation much easier and hopefully more reliable.

`text=` not working? (`#4313`_)
-------------------------------
There was a regression in Playwright 1.55.* that caused performance issues
when computing selectors in error case. This was fixed in Playwright 1.56.0.

Fix release process for BrowserBatteries (`#4433`_)
---------------------------------------------------
There was issues in the release process for BrowserBatteries that caused
the package to not be released correctly. This is now fixed.


Move rfbrowser coverage command to use Merge Coverage Reports internally (`#4383`_)
-----------------------------------------------------------------------------------
The rfbrowser coverage command now uses the Merge Coverage Reports keyword
internally. This makes it possible to use the command without when BrowserBatteries
is installed and NodeJS is not available.

Update grpcio and grpcio-tools to version 1.75.1 (`#4428`_)
-----------------------------------------------------------
Updated grpcio and grpcio-tools to version 1.75.1 to fix some issues with
Python 3.14.

Close Page` with page given and `context` and `browser` set to `ALL` fails but closes correctly (`#4451`_)
----------------------------------------------------------------------------------------------------------
Fixed an issue where Close Page keyword with page given and context and browser
was not working correctly when all contexts and browsers were selected.

Get Page Ids should accept context and browser ids and Assertion Engine (`#4450`_)
----------------------------------------------------------------------------------
Get Page Ids keyword now accepts context and browser ids and Assertion Engine
parameters.

Acknowledgements
================

Playwright process is not killed after tests are done (`#4421`_)
---------------------------------------------------------------
Fixed an issue where Playwright process was not killed after tests are done, this
specially affected Windows users.

Many thanks to Sander van Beek for reporting the issue and providing the fix for
bug.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4313`_
      - bug
      - critical
      - `text=` not working?
    * - `#4433`_
      - bug
      - critical
      - Fix release process for BrowserBatteries
    * - `#4303`_
      - enhancement
      - critical
      - Distribute RF Browser fully bundled as wheel including external NodeJS and NPM dependencies
    * - `#4383`_
      - enhancement
      - critical
      - Move rfbrowser coverage command to use Merge Coverage Reports internally
    * - `#4421`_
      - bug
      - high
      - Playwright process is not killed after tests are done
    * - `#4428`_
      - bug
      - high
      - Update grpcio and grpcio-tools to version 1.75.1
    * - `#4451`_
      - bug
      - high
      - `Close Page` with page given and `context` and `browser` set to `ALL` fails but closes correctly
    * - `#4450`_
      - enhancement
      - high
      - Get Page Ids should accept context and browser ids and Assertion Engine
    * - `#3385`_
      - bug
      - medium
      - screenshot filenames just replace `{index}` instead of properly formatting it.
    * - `#4241`_
      - bug
      - medium
      - Press Keys doesn't support delay

Altogether 10 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.9.0>`__.

.. _#4313: https://github.com/MarketSquare/robotframework-browser/issues/4313
.. _#4433: https://github.com/MarketSquare/robotframework-browser/issues/4433
.. _#4303: https://github.com/MarketSquare/robotframework-browser/issues/4303
.. _#4383: https://github.com/MarketSquare/robotframework-browser/issues/4383
.. _#4421: https://github.com/MarketSquare/robotframework-browser/issues/4421
.. _#4428: https://github.com/MarketSquare/robotframework-browser/issues/4428
.. _#4451: https://github.com/MarketSquare/robotframework-browser/issues/4451
.. _#4450: https://github.com/MarketSquare/robotframework-browser/issues/4450
.. _#3385: https://github.com/MarketSquare/robotframework-browser/issues/3385
.. _#4241: https://github.com/MarketSquare/robotframework-browser/issues/4241
