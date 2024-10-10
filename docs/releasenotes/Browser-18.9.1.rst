======================
Browser library 18.9.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.9.1 is a new release with
and bug fix for Docker container creation. All issues targeted for Browser
library v18.9.1 can be found from the `issue tracker`_.
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
install it manually. Browser library 18.9.1 was released on Thursday October 10, 2024.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.48.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.9.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Fix Docker build (`#3835`_)
-----------------------------
Docker container creation was fixed in this release. Library code has not been changed.

Create release with Playwright 1.48 (`#3838`_)
---------------------------------------------
Library was tested with Playwright 1.48.0. Library code has not been changed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3835`_
      - bug
      - critical
      - Fix Docker build
    * - `#3838`_
      - enhancement
      - high
      - Create release with Playwright 1.48

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.9.1>`__.

.. _#3835: https://github.com/MarketSquare/robotframework-browser/issues/3835
.. _#3838: https://github.com/MarketSquare/robotframework-browser/issues/3838
