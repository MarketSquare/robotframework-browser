======================
Browser library 17.1.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 17.1.1 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v17.1.1 can be found
from the `issue tracker`_.
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
install it manually. Browser library 17.1.1 was released on Thursday July 27, 2023.
Browser supports Python 3.8+, Node 16/18 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.36.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v17.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Wait For Response does raise error on OPTIONS response with Preflighted requests in CORS (`#2970`_)
- Updated dependencies (incl. Playwright 1.36.2)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2970`_
      - bug
      - critical
      - Wait For Response does raise error on OPTIONS response with Preflighted requests in CORS

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av17.1.1>`__.

.. _#2970: https://github.com/MarketSquare/robotframework-browser/issues/2970
