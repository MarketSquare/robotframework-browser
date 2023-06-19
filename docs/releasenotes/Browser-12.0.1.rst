======================
Browser library 12.0.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 12.0.1 is a new hotfix
release for regression in Select Options By keyword. All issues targeted
for Browser library v12.0.1 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==12.0.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 12.0.1 was released on Wednesday February 23, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.19.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av12.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Select Options By is mixing value and text SelectAttribute and wrongly returns strict mode violation (`#1796`_)
---------------------------------------------------------------------------------------------------------------
There was a regression in 12.0.0 release with Select Options By keyword,
when option elements had same text and value, but in different options elements.
This bug caused keyword to fail, event it should not fail. This regression is
now fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1796`_
      - bug
      - critical
      - Select Options By is mixing value and text SelectAttribute and wrongly returns strict mode violation

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av12.0.1>`__.

.. _#1796: https://github.com/MarketSquare/robotframework-browser/issues/1796
