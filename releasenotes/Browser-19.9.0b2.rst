========================
Browser library 19.9.0b2
========================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.9.0b2 is a new release with
enhancements for distributing NodeJS dependencies as part of the wheel
BrowserBatteries wheel. Because of this, there is changes to packaging and
releasing. Other enhancements and fixes are listed below. All issues targeted
for Browser library v19.9.0 can be found from the `issue tracker`_.
The differeces between 19.9.0b1 and 19.9.0b2 are mainly related to
fixing the release process for BrowserBatteries. For first time
installation with pip_ and BrowserBatteries just run
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
Alternatively you can download the source distributions from PyPI_ and
install it manually. Browser library and BrowserBatteries 19.9.0b2 was
released on Sunday September 28, 2025. Browser and BrowserBatteries
supports Python 3.9+, Node 20/22/24 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.55.1

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

Distribute NodeJS as part of the wheel (`#4303`_, beta 1)
---------------------------------------------------------
Because difficulties with installing NodeJS and npm dependencies, specially in corporate
environments, NodeJS and the NodeJS dependencies are now distributed as part of the BrowserBatteries
wheel. This makes the installation much easier and more reliable. Playwright browsers
binaries are still distributed separately and need to be installed with `rfbrowser install`
command. But if user has previously just used Browser library, user can now install
BrowserBatteries and run `rfbrowser install` to get everything working and user does not
need to install NodeJS separately.

Please note that BrowserBatteries may not be available for all platforms and architectures.
Also note that if user have extensions that require NodeJS or NodeJS dependencies, those
need to be installed separately. If you have issues with BrowserBatteries, please
open an issue to the `issue tracker`_ or use Slack #browser channel.

Move rfbrowser coverage command to use Merge Coverage Reports internally (`#4383`_, beta 1)
-------------------------------------------------------------------------------------------
The "rfbrowser coverage" command now uses "Merge Coverage Reports" keyword internally. This
should not affect users, but it makes the implementation cleaner and more maintainable.

Update grpcio and grpcio-tools to version 1.75.1 (`#4428`_, beta 1)
-------------------------------------------------------------------
Update grpcio and grpcio-tools to version 1.75.1 to address Python 3.14 support. This removes
one blocker for Python 3.14 support, but we will wait for the official release of Python 3.14,
before this projects supports it.


.. _#4303: https://github.com/MarketSquare/robotframework-browser/issues/4303
.. _#4383: https://github.com/MarketSquare/robotframework-browser/issues/4383
.. _#4428: https://github.com/MarketSquare/robotframework-browser/issues/4428

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#4433`_
      - bug
      - critical
      - Fix release process for BrowserBatteries
      - beta 2
    * - `#4303`_
      - enhancement
      - critical
      - Distribute NodeJS as part of the wheel
      - beta 1
    * - `#4383`_
      - enhancement
      - critical
      - Move rfbrowser coverage command to use Merge Coverage Reports internally
      - beta 1
    * - `#4428`_
      - bug
      - high
      - Update grpcio and grpcio-tools to version 1.75.1
      - beta 1

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.9.0>`__.

.. _#4433: https://github.com/MarketSquare/robotframework-browser/issues/4433
.. _#4303: https://github.com/MarketSquare/robotframework-browser/issues/4303
.. _#4383: https://github.com/MarketSquare/robotframework-browser/issues/4383
.. _#4428: https://github.com/MarketSquare/robotframework-browser/issues/4428
