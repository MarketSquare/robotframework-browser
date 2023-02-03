======================
Browser library 10.0.3
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 10.0.3 is a new hotfix
release with bug fixes for locating elements and waiting their state.
All issues targeted for Browser library v10.0.3 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init

to install the latest available release or use
::
   pip install robotframework-browser==10.0.3
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 10.0.3 was released on Monday November 8, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.16.3

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av10.0.3


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Get Element Count returns 1 when counting elements inside iframe (`#1457`_)
---------------------------------------------------------------------------
Counting elements inside did not work correctly. This was regression since 9.0.2 and
due internal refactoring.

Get Elements keyword returning 0 because it does not wait element attached state. (`#1467`_)
--------------------------------------------------------------------------------------------
There was regression since 9.0.2 release, because Get Elements keyword did not wait that first
element is not visible in the page. Now keyword waits element(s) to be visible.

Acknowledgements
================

The Get Devices links is not anymore valid (`#1461`_)
-----------------------------------------------------
The Get Devices keyword documentation link did not anymore point to valid documentation
in Playwright side. This is now fixed.

Many thanks Raphael Smadja for providing the fix.

Fix wait_for_navigation argument name in documentation  (`#1474`_)
------------------------------------------------------------------
There was bug in keyword documentation, there was type in keyword argument name.

Many thanks Raphael Smadja for providing the fix.

Fix typo in node side PW wrapper: laywirght-invoke to playwright-invoke (`#1481`_)
----------------------------------------------------------------------------------
There was a type in node side file names, laywirght-invoke is renamed to playwright-invoke.

Many thanks for Juga Paazmaya for providing the fix.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1457`_
      - bug
      - high
      - Get Element Count returns 1 when counting elements inside iframe
    * - `#1461`_
      - bug
      - high
      - The Get Devices links is not anymore valid
    * - `#1467`_
      - bug
      - high
      - Get Elements keyword returning 0 because it does not wait element attached state.
    * - `#1455`_
      - bug
      - medium
      - ImportError: cannot import name 'DialogAction' from 'Browser'
    * - `#1474`_
      - bug
      - medium
      - Fix wait_for_navigation argument name in documentation 
    * - `#1481`_
      - bug
      - medium
      - Fix typo in node side PW wrapper: laywirght-invoke to playwright-invoke

Altogether 7 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av10.0.3>`__.

.. _#1457: https://github.com/MarketSquare/robotframework-browser/issues/1457
.. _#1461: https://github.com/MarketSquare/robotframework-browser/issues/1461
.. _#1467: https://github.com/MarketSquare/robotframework-browser/issues/1467
.. _#1455: https://github.com/MarketSquare/robotframework-browser/issues/1455
.. _#1474: https://github.com/MarketSquare/robotframework-browser/issues/1474
.. _#1481: https://github.com/MarketSquare/robotframework-browser/issues/1481
