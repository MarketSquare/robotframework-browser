=====================
Browser library 9.0.2
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 9.0.2 is a new release with
bug fixes on run on failure args and Get Cookie keyword. All issues targeted
for Browser library v9.0.2 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init

to install the latest available release or use
::
   pip install robotframework-browser==9.0.2
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 9.0.2 was released on Thursday October 21, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.15.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av9.0.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Run on failure does not work correctly if named argument syntax is used (`#1396`_)
----------------------------------------------------------------------------------
Run on failure functionality support arguments, but named argument syntax was used,
using run on failure keywords did result in failure. This is now fixed and
named argument syntax is now also supported.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1396`_
      - bug
      - critical
      - Run on failure does not work correctly if named argument syntax is used
    * - `#1406`_
      - bug
      - medium
      - Get cookie returns expiry warning for Session based cookie(s) on Windows.

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av9.0.2>`__.

.. _#1396: https://github.com/MarketSquare/robotframework-browser/issues/1396
.. _#1406: https://github.com/MarketSquare/robotframework-browser/issues/1406
