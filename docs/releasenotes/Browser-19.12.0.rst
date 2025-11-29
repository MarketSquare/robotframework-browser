=======================
Browser library 19.12.0
=======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.12.0 is a new release with
enhancements to installation. Playwright 1.57.0 changed Chromium to Chrome for
testing. The most notable changes is that ifcon is changed from Chromium to
Chrome. With this change we have also updated rfbrowser init supported browsers,
but this depends on Playwright support and what is available in your system.
All issues targeted for Browser library v19.12.0 can be found from the
`issue tracker`_. For first time installation with pip_ and
BrowserBatteries_ just run
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
install it manually. Browser library 19.12.0 was released on Saturday November 29, 2025.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.57.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _BrowserBatteries: https://pypi.org/project/robotframework-browser-batteries/
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.12.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Drop support for Robot Framework 5 (`#4563`_)
---------------------------------------------
We did announce about dropping RF5 support in previous releases, but did
not actually drop it. Now Browser library 19.12.0 drops support for Robot Framework 5.

Playwright 1.57.0 (`#4559`_)
----------------------------
Browser library 19.12.0 updates Playwright to version 1.57.0. Playwright 1.57.0
changed Chromium to Chrome for testing. With this change we have also updated
rfbrowser init supported browsers, but this depends on Playwright support and
what is available in your system.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4563`_
      - bug
      - high
      - Drop support for Robot Framework 5
    * - `#4559`_
      - enhancement
      - high
      - Playwright 1.57.0

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.12.0>`__.

.. _#4563: https://github.com/MarketSquare/robotframework-browser/issues/4563
.. _#4559: https://github.com/MarketSquare/robotframework-browser/issues/4559
