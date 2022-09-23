======================
Browser library 14.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 14.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v14.0.0 can be found
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
install it manually. Browser library 14.0.0 was released on Friday September 23, 2022. 
Browser supports Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.25.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av14.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Improved argument docs and updated signatures for consistency (`#2308`_)
- Added Scope feature to timeout, retry_assertion and strice_mode (`#2319`_)
- `Wait For Condition` to check any information that may happen on page...  (`#2331`_)
- FIXED: Switch Page fails when context and browser id are given as well. (`#2327`_)
- FIXED:New Context with viewport set to None does not behave as in Playwright (`#2054`_)

Backwards incompatible changes
==============================

- Some Assertion Keywords have old argument names `expected_value` (`#2329`_)

Deprecated features
===================

- Deprecation of `delay` in milliseconds to introduce support for timedelta (`#2330`_)
- Deprecation of positional arguments on `Import`, `New Browser`, `New Context` & `New Persistent Context` (`#2328`_)

Acknowledgements
================

- "Press Key" documentation could use updating. (`#2202`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2327`_
      - bug
      - critical
      - Switch Page fails when context and browser id are given as well.
    * - `#2308`_
      - enhancement
      - critical
      - Topic/argument docs
    * - `#2054`_
      - bug
      - high
      - New Context with viewport set to None does not behave as in Playwright
    * - `#2319`_
      - enhancement
      - high
      - Added Scope feature to timeout, retry_assertion and strice_mode
    * - `#2331`_
      - enhancement
      - high
      - `Wait For Condition` to check any information that may happen on page... 
    * - `#2185`_
      - bug
      - medium
      - `New Persistent Context` documentation URL is not pointing to the right resource (`404` Not Found)
    * - `#2202`_
      - bug
      - medium
      - "Press Key" documentation could use updating.
    * - `#2330`_
      - bug
      - medium
      - Deprecation of `delay` in milliseconds to introduce support for timedelta
    * - `#2170`_
      - enhancement
      - medium
      - Command `show-trace` ends with "Trace file does not exist!" error if path is not absolute
    * - `#2328`_
      - enhancement
      - medium
      - Deprecation of positional arguments on `Import`, `New Browser`, `New Context` & `New Persistent Context`
    * - `#2329`_
      - bug
      - low
      - Some Assertion Keywords have old argument names `expected_value`

Altogether 11 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av14.0.0>`__.

.. _#2327: https://github.com/MarketSquare/robotframework-browser/issues/2327
.. _#2308: https://github.com/MarketSquare/robotframework-browser/issues/2308
.. _#2054: https://github.com/MarketSquare/robotframework-browser/issues/2054
.. _#2319: https://github.com/MarketSquare/robotframework-browser/issues/2319
.. _#2331: https://github.com/MarketSquare/robotframework-browser/issues/2331
.. _#2185: https://github.com/MarketSquare/robotframework-browser/issues/2185
.. _#2202: https://github.com/MarketSquare/robotframework-browser/issues/2202
.. _#2330: https://github.com/MarketSquare/robotframework-browser/issues/2330
.. _#2170: https://github.com/MarketSquare/robotframework-browser/issues/2170
.. _#2328: https://github.com/MarketSquare/robotframework-browser/issues/2328
.. _#2329: https://github.com/MarketSquare/robotframework-browser/issues/2329
