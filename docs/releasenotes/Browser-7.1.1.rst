=====================
Browser library 7.1.1
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 7.1.1 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v7.1.1 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==7.1.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 7.1.1 was released on Thursday August 26, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.14.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av7.1.1


.. contents::
   :depth: 2
   :local:

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1247`_
      - ---
      - ---
      - Link keywords in example to docs
    * - `#1255`_
      - ---
      - ---
      - Fix PLAYWRIGHT_BROWSERS_PATH overriding in entry.py

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av7.1.1>`__.

.. _#1247: https://github.com/MarketSquare/robotframework-browser/issues/1247
.. _#1255: https://github.com/MarketSquare/robotframework-browser/issues/1255
