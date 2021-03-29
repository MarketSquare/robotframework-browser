=====================
Browser library 4.2.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 4.2.0 is a new release with
HAR record support and record + analyze browser console logs. Also there fixes
to documentation  enhancements and capturing screenshot in error situation.
All issues targeted for Browser library v4.2.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==4.2.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 4.2.0 was released on Monday March 29, 2021. Browser supports
Python **3.7+**, and Robot Framework **3.2+** and NodeJS 12 and 14 LTS versions.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av4.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Documentation explaining automatic closing is not clear. (`#819`_)
------------------------------------------------------------------
Documentation for automatic closing was unclear and caused confusing in users how it
actually works. Now the documentation has been to fixed and hopefully it causes less
confusing in the users.

Keyword 'Take Screenshot' could not be run on failure: 'NoneType' object is not iterable (`#868`_)
--------------------------------------------------------------------------------------------------
Under certains contains with RF 4 test case name is not available and caused test name to be returned
as Python None. This did lead to unhandled exception in Python side and error in library. This is now
fixed.

Read  assertion operator table from assertion engine  (`#863`_)
---------------------------------------------------------------
In the past assertion operators documentation was hard coded in the library docs. Now the assertion operator
is read from the assertion engine tool and is dynamically updated when tool also updates.

Exposing Playwirght channel API for easier support for different browsers (`#865`_)
-----------------------------------------------------------------------------------
Playwright comes with inbuild Chromium browser, but starting from 1.10 release, it has been
possible to use preinstalled Chrome/Chromium Edge browsers with channel argument. This
is now exposed argument in Browser library side too.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#819`_
      - bug
      - critical
      - Documentation explaining automatic closing is not clear.
    * - `#868`_
      - bug
      - critical
      -  Keyword 'Take Screenshot' could not be run on failure: 'NoneType' object is not iterable
    * - `#863`_
      - bug
      - high
      - Read  assertion operator table from assertion engine 
    * - `#865`_
      - enhancement
      - high
      - Exposing pleywirght channel API for easier support for different browsers
    * - `#791`_
      - bug
      - medium
      - Download need pageot be loaded before keyword can perform the download
    * - `#745`_
      - enhancement
      - ---
      - Record and analyze console log

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av4.2.0>`__.

.. _#819: https://github.com/MarketSquare/robotframework-browser/issues/819
.. _#868: https://github.com/MarketSquare/robotframework-browser/issues/868
.. _#863: https://github.com/MarketSquare/robotframework-browser/issues/863
.. _#865: https://github.com/MarketSquare/robotframework-browser/issues/865
.. _#791: https://github.com/MarketSquare/robotframework-browser/issues/791
.. _#745: https://github.com/MarketSquare/robotframework-browser/issues/745
