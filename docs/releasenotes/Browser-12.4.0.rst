======================
Browser library 12.4.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 12.4.0 is a new release with
table keywords enhancements and several bug fixes. Now example trace viewer
should work without re-installing Playwright. All issues targeted for Browser
library v12.4.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==12.4.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 12.4.0 was released on Tuesday May 17, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.22.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av12.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

${OUTPUT_DIR}/browser has deleted between suites, when test case fails (`#1889`_)
---------------------------------------------------------------------------------
${OUTPUT_DIR}/browser has deleted was deleted between suites, but it should have been
deleted only at start of the test execution.

Wait for alert keyword fails at wait for promise  (`#1980`_)
------------------------------------------------------------
This was caused by accepting invalid case for the keyword and is now filed

74 MB File size limit (`#1497`_)
--------------------------------
This was limitation on Playwright side and now it has been fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1889`_
      - bug
      - critical
      - ${OUTPUT_DIR}/browser has deleted between suites, when test case fails
    * - `#1980`_
      - bug
      - high
      - Wait for alert keyword fails at wait for promise 
    * - `#1497`_
      - enhancement
      - high
      - 74 MB File size limit
    * - `#1867`_
      - bug
      - medium
      - Catalog contains pages' title with None values
    * - `#2002`_
      - bug
      - medium
      - rfbrowser trace viewer does not work
    * - `#2025`_
      - bug
      - ---
      - fixed Table Bug
    * - `#1926`_
      - enhancement
      - ---
      - added capability to select ALL when switching

Altogether 7 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av12.4.0>`__.

.. _#1889: https://github.com/MarketSquare/robotframework-browser/issues/1889
.. _#1980: https://github.com/MarketSquare/robotframework-browser/issues/1980
.. _#1497: https://github.com/MarketSquare/robotframework-browser/issues/1497
.. _#1867: https://github.com/MarketSquare/robotframework-browser/issues/1867
.. _#2002: https://github.com/MarketSquare/robotframework-browser/issues/2002
.. _#2025: https://github.com/MarketSquare/robotframework-browser/issues/2025
.. _#1926: https://github.com/MarketSquare/robotframework-browser/issues/1926
