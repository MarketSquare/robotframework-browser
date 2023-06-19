======================
Browser library 10.0.2
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 10.0.2 is a new release with
bug fix for Wait For Element State keyword when strict mode is false. All issues
targeted for Browser library v10.0.2 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init

to install the latest available release or use
::
   pip install robotframework-browser==10.0.2
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 10.0.2 was released on Friday October 29, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.16.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av10.0.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Wait For Element State 'hidden' results to locator.elementHandle failed (`#1442`_)
------------------------------------------------------------------------------------
Fixes, most likely, a bug with Wait For Element State 'hidden' state when strict mode
is disabled.

Wrong arguments order for "Select Options By" in documentation (`#1443`_)
-------------------------------------------------------------------------
Arguments should be now in correct order in docs.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1442`_
      - bug
      - critical
      - Wait For Element State 'hidden' results to locator.elementHandle failed
    * - `#1443`_
      - bug
      - high
      - Wrong arguments order for "Select Options By" in documentation

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av10.0.2>`__.

.. _#1442: https://github.com/MarketSquare/robotframework-browser/issues/1442
.. _#1443: https://github.com/MarketSquare/robotframework-browser/issues/1443
