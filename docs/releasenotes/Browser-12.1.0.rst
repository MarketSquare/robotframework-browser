======================
Browser library 12.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 12.1.0 is a new release with
commit state for Wait For Navigation keyword and and bug fix for Select Options
By keyword. All issues targeted for Browser library v12.1.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==12.1.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 12.1.0 was released on Saturday February 26, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.19.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av12.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Select Options By with duplicate values fails... (`#1808`_)
-------------------------------------------------------------
There was bug in Select Options By keyword logic. It assumed that options element
value tag was unique, but there are cases when it was not unique for valid reasons
and in that case library raised an exception even it should not do it.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1808`_
      - bug
      - critical
      - Select Options By    with duplicate values fails...
    * - `#1802`_
      - enhancement
      - medium
      - Wait For Navigation should also support Playwrigh commit state

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av12.1.0>`__.

.. _#1808: https://github.com/MarketSquare/robotframework-browser/issues/1808
.. _#1802: https://github.com/MarketSquare/robotframework-browser/issues/1802
