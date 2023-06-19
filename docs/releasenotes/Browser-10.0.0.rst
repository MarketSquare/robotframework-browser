======================
Browser library 10.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 10.0.0 is a new release with
enhancements for how selectors are resolved and bug fixes.
All issues targeted for Browser library v10.0.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init

to install the latest available release or use
::
   pip install robotframework-browser==10.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 10.0.0 was released on Tuesday October 26, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.16.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av10.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

`Click` keyword fails if locator is mix of `element` and something else (`#1084`_)
----------------------------------------------------------------------------------
For historical reasons there used to be many ways in the library node side to find and interact
with Playwright on elements in the page. This difference made it possible to have bugs like this
and also it made library maintenance harder. With this release, internal node side is changed to
use Playwright Locator_ class, instead of mixture of different approaches.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1084`_
      - bug
      - critical
      - `Click` keyword fails if locator is mix of `element` and something else
    * - `#1407`_
      - enhancement
      - medium
      - Add stable state for Wait For Elements State keyword

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av10.0.0>`__.

.. _#1084: https://github.com/MarketSquare/robotframework-browser/issues/1084
.. _#1407: https://github.com/MarketSquare/robotframework-browser/issues/1407
.. _Locator: https://playwright.dev/docs/api/class-locator
