=======================
Browser library 19.10.1
=======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.10.1 is a new hotfix
release on taking screenshot and making rfbrowser command line tool logger
lazy. All issues targeted for Browser library v19.10.1 can be found
from the `issue tracker`_.
For first time installation with pip_ and BrowserBatteries_ just run
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
install it manually. Browser library 19.10.1 was released on Thursday October 16, 2025.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.56.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _BrowserBatteries: https://pypi.org/project/robotframework-browser-batteries/
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.10.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Take Screenshot can not overwrite existing filename if it does not have {index} (`#4485`_)
------------------------------------------------------------------------------------------
Fixed an issue where Take Screenshot could not overwrite an existing filename if it did not have
{index} marker in it. Now it correctly overwrites the file as intended.

Acknowledgements
================

Make logger initialization lazy to avoid permission errors (`#4491`_)
---------------------------------------------------------------------
Fixed an issue where rfbrowser command line tool could cause permission errors
when it was run in a folder where user did not have write permissions. Now the
logger initialization is lazy and it does not try to create log file until it is
actually needed.

Many thanks for David Sommers for reporting the issue and suggesting a fix!

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4485`_
      - bug
      - critical
      - Take Screenshot can not overwrite existing filename if it does not have {index}
    * - `#4491`_
      - enhancement
      - high
      - Make logger initialization lazy to avoid permission errors

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.10.1>`__.

.. _#4485: https://github.com/MarketSquare/robotframework-browser/issues/4485
.. _#4491: https://github.com/MarketSquare/robotframework-browser/issues/4491
