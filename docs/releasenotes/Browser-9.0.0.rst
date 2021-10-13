=====================
Browser library 9.0.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 9.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v9.0.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==9.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 9.0.0 was released on Wednesday October 13, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.15.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av9.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Pip does not clean inside site-packages/Browser/wrapper anymore when uninstalling (`#1253`_)
    - Sometimes pip fails to completely clean up site packages (depends on pip version and environment), now there is `rfbrowser clean-node` to run before pip uninstall to ensure cleanup
- Issue with keyword documentation example - Select Options By (`#1335`_)
- Set Strict Mode keyword documentation is not correct.  (`#1320`_)
- Doc Keywords: Move closing context/page section into "Browser, Context, Page" section (`#1362`_)

Acknowledgements
================

- Thanks to https://github.com/UliSei for contributing PR for: Docu keywords: "Drag And Drop By Coordinates" and "Go To" (`#1328`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1253`_
      - bug
      - high
      - Pip does not clean inside site-packages/Browser/wrapper anymore when uninstalling
    * - `#1320`_
      - bug
      - high
      - Set Strict Mode keyword documentation is not correct. 
    * - `#1335`_
      - bug
      - high
      - Issue with keyword documentation example - Select Options By
    * - `#1362`_
      - bug
      - high
      - Doc Keywords: Move closing context/page section into "Browser, Context, Page" section
    * - `#1179`_
      - bug
      - medium
      - Chrome.json download link is broken
    * - `#1328`_
      - bug
      - medium
      - Docu keywords: "Drag And Drop By Coordinates" and "Go To"

Altogether 7 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av9.0.0>`__.

.. _#1253: https://github.com/MarketSquare/robotframework-browser/issues/1253
.. _#1320: https://github.com/MarketSquare/robotframework-browser/issues/1320
.. _#1335: https://github.com/MarketSquare/robotframework-browser/issues/1335
.. _#1362: https://github.com/MarketSquare/robotframework-browser/issues/1362
.. _#1179: https://github.com/MarketSquare/robotframework-browser/issues/1179
.. _#1328: https://github.com/MarketSquare/robotframework-browser/issues/1328
