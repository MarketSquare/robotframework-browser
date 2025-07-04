======================
Browser library 19.6.2
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.6.2 is a new hotfix
release which updates Playwright to version 1.53.2. All issues targeted
for Browser library v19.6.2 can be found from the `issue tracker`_.
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
install it manually. Browser library 19.6.2 was released on Friday July 4, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.53.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.6.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Playwright 1.53.2 (`#4285`_)
------------------------------

  This release updates Playwright to version 1.53.2, which includes
  various bug fixes and enhancements from the Playwright team.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4285`_
      - bug
      - high
      - Playwright 1.53.2

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.6.2>`__.

.. _#4285: https://github.com/MarketSquare/robotframework-browser/issues/4285
