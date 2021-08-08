=====================
Browser library 7.0.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 7.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v7.0.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==7.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 7.0.0 was released on Sunday August 8, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.13.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av7.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- Write example to keyword documentation (`#1184`_)
- Remove deprected keyword from the library (`#1200`_)

Backwards incompatible changes
==============================

**EXPLAIN** or remove these.

- Remove deprected keyword from the library (`#1200`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1184`_
      - bug
      - critical
      - Write example to keyword documentation
    * - `#1200`_
      - enhancement
      - high
      - Remove deprected keyword from the library

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av7.0.0>`__.

.. _#1184: https://github.com/MarketSquare/robotframework-browser/issues/1184
.. _#1200: https://github.com/MarketSquare/robotframework-browser/issues/1200
