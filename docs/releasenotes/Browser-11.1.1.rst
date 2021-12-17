======================
Browser library 11.1.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 11.1.1 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v11.1.1 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==11.1.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 11.1.1 was released on Friday December 17, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.17.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av11.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- Move to use Playwright frameLocator  (`#1613`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1613`_
      - enhancement
      - high
      - Move to use Playwright frameLocator 
    * - `#1625`_
      - ---
      - ---
      - Document how to set download directory with Download and Promise to Wait For Download keywords

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av11.1.1>`__.

.. _#1613: https://github.com/MarketSquare/robotframework-browser/issues/1613
.. _#1625: https://github.com/MarketSquare/robotframework-browser/issues/1625
