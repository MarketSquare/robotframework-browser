======================
Browser library 11.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 11.3.0 is a new release with
adding New Context keyword arguments and creating log file during the install
process. Also New Context keyword acceptDownloads default value is changed to
True. There is also fixes to Get Elements(s) keyword documentation. All
issues targeted for Browser library v11.3.0 can be found from the
`issue tracker`_. If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==11.3.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 11.3.0 was released on Sunday January 30, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.18.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av11.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Fix Get Element and Get Elements keywords docs, library now uses Playwright locators (`#1707`_)
-----------------------------------------------------------------------------------------------
Since Browser library moved to use Playwrigh locators, we did forget to fix the
the Get Element(s) keyword documentation, because it did still talk about DOM
elements. The current implementation saves references to Locators.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1707`_
      - bug
      - high
      - Fix Get Element and Get Elements keywords docs, library now uses Playwright locators
    * - `#1686`_
      - bug
      - medium
      - Python scripts Browser(run_on_failure=..) & register_keyword_to_run_on_failure both not working
    * - `#1117`_
      - enhancement
      - medium
      - Improved troubleshooting output on `rfbrowser init` failure
    * - `#1717`_
      - enhancement
      - medium
      - Change New Context keyword 
    * - `#1719`_
      - enhancement
      - medium
      - Add reducedMotion and forcedColors arguments to New Context keyword

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av11.3.0>`__.

.. _#1707: https://github.com/MarketSquare/robotframework-browser/issues/1707
.. _#1686: https://github.com/MarketSquare/robotframework-browser/issues/1686
.. _#1117: https://github.com/MarketSquare/robotframework-browser/issues/1117
.. _#1717: https://github.com/MarketSquare/robotframework-browser/issues/1717
.. _#1719: https://github.com/MarketSquare/robotframework-browser/issues/1719
