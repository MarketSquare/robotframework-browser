======================
Browser library 12.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 12.3.0 is a new release with
enhancements when taking screenshot and bug fixes in several places.
All issues targeted for Browser library v12.3.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==12.3.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 12.3.0 was released on Sunday April 3, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.20.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av12.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Python script promise_to always got error "No library '<Browser.browser.Browser object at 0x...>' found." (`#1685`_)
--------------------------------------------------------------------------------------------------------------------
In previous releases it was not possible to use promises from external libraries.

This is not fixed and library offer better API also when used directly from Python
or from a external library.

Method get_elements returns invalid references (`#1849`_)
---------------------------------------------------------
Get Elements keyword did not work correctly with frames. This is now fixed

Proxy configuration in Browser is not working because username is defined as Username (`#1873`_)
------------------------------------------------------------------------------------------------
Argument did have wrong case, uppercase, but it should have all lower cases. This is now fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1685`_
      - bug
      - high
      - Python script promise_to always got error "No library '<Browser.browser.Browser object at 0x...>' found."
    * - `#1849`_
      - bug
      - high
      - Method get_elements returns invalid references
    * - `#1873`_
      - bug
      - high
      - Proxy configuration in Browser is not working because username is defined as Username
    * - `#1890`_
      - bug
      - high
      - Docs: New Browser keyword documentation mentions a wrong default value for `headless`
    * - `#1898`_
      - enhancement
      - medium
      - Adding an option for bypassing the actionability checks of Playwright
    * - `#1921`_
      - enhancement
      - ---
      - Added Playwright 1.20 features to `Take Screenshot`

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av12.3.0>`__.

.. _#1685: https://github.com/MarketSquare/robotframework-browser/issues/1685
.. _#1849: https://github.com/MarketSquare/robotframework-browser/issues/1849
.. _#1873: https://github.com/MarketSquare/robotframework-browser/issues/1873
.. _#1890: https://github.com/MarketSquare/robotframework-browser/issues/1890
.. _#1898: https://github.com/MarketSquare/robotframework-browser/issues/1898
.. _#1921: https://github.com/MarketSquare/robotframework-browser/issues/1921
