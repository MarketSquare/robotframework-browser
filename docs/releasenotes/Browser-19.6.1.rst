======================
Browser library 19.6.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.6.1 is a new hotfix
release which updated Playwright to 1.53.1. All issues targeted for
Browser library v19.6.1 can be found from the `issue tracker`_.
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
install it manually. Browser library 19.6.1 was released on Thursday June 26, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.53.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.6.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Cannot fill programmatically enabled Textarea (`#4274`_)
--------------------------------------------------------
This is bug in Playwright that was fixed in Playwright 1.53.1.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4274`_
      - bug
      - high
      - Cannot fill programmatically enabled Textarea

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.6.1>`__.

.. _#4274: https://github.com/MarketSquare/robotframework-browser/issues/4274
