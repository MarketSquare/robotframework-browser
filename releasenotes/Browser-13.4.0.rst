======================
Browser library 13.4.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 13.4.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v13.4.0 can be found
from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and 
install it manually. Browser library 13.4.0 was released on Saturday July 30, 2022. 
Browser supports Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.24.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av13.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- Can not close context if web browser tab was auto-closed (`#2089`_)
- New Persistent Context docs improvements (`#2048`_)
- Support beforeunload dialogs (`#2098`_)

Acknowledgements
================

**EXPLAIN** or remove these.

- "Press Key" documentation could use updating. (`#2202`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2089`_
      - bug
      - high
      - Can not close context if web browser tab was auto-closed
    * - `#2048`_
      - enhancement
      - high
      - New Persistent Context docs improvements
    * - `#2098`_
      - enhancement
      - high
      - Support beforeunload dialogs
    * - `#2185`_
      - bug
      - medium
      - `New Persistent Context` documentation URL is not pointing to the right resource (`404` Not Found)
    * - `#2202`_
      - bug
      - medium
      - "Press Key" documentation could use updating.
    * - `#1811`_
      - enhancement
      - medium
      - Add waitUntil support for New Page and Go To keywords 
    * - `#2170`_
      - enhancement
      - medium
      - Command `show-trace` ends with "Trace file does not exist!" error if path is not absolute

Altogether 7 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av13.4.0>`__.

.. _#2089: https://github.com/MarketSquare/robotframework-browser/issues/2089
.. _#2048: https://github.com/MarketSquare/robotframework-browser/issues/2048
.. _#2098: https://github.com/MarketSquare/robotframework-browser/issues/2098
.. _#2185: https://github.com/MarketSquare/robotframework-browser/issues/2185
.. _#2202: https://github.com/MarketSquare/robotframework-browser/issues/2202
.. _#1811: https://github.com/MarketSquare/robotframework-browser/issues/1811
.. _#2170: https://github.com/MarketSquare/robotframework-browser/issues/2170
