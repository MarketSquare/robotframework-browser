======================
Browser library 16.2.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 16.2.0 is a new release with
add Tab keyword to the library. All issues targeted for Browser library
v16.2.0 can be found from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and
install it manually. Browser library 16.2.0 was released on Saturday May 27, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.34.3

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v16.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

New keyword provide for playwright locator.tap (`#2301`_)
---------------------------------------------------------
For better support for mobile emulation Tab keyword was added to the
library. Many thanks for nixuewei for the idea.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2301`_
      - enhancement
      - high
      - new keyword provide for playwright locator.tap
    * - `#2479`_
      - bug
      - medium
      - Red herring: Installation directory `[..]\venv\Lib\site-packages\Browser\wrapper` does not contain the required files

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av16.2.0>`__.

.. _#2301: https://github.com/MarketSquare/robotframework-browser/issues/2301
.. _#2479: https://github.com/MarketSquare/robotframework-browser/issues/2479
