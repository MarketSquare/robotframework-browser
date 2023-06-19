=====================
Browser library 4.3.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 4.3.0 is a new release with
screenshot supporting quality attributes enhancements. All issues targeted
for Browser library v4.3.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==4.3.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 4.3.0 was released on Friday April 9, 2021. Browser supports
Python 3.7+, Robot Framework 3.2+ and Node LTS 12 and 14.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av4.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add support for Added timeout, fileType and quality arguments to take_screenshot (`#913`_)
------------------------------------------------------------------------------------------
Enhancement allows to better control screenshot size by exposing timeout, fileType and quality
arguments from Playwright side.

Many thanks for vincenzo-gasparo for providing the PR.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#913`_
      - enhancement
      - high
      - Add support for Added timeout, fileType and quality arguments to take_screenshot
    * - `#886`_
      - bug
      - medium
      - Get Classes returns not a list when only 1 css class on element

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av4.3.0>`__.

.. _#913: https://github.com/MarketSquare/robotframework-browser/issues/913
.. _#886: https://github.com/MarketSquare/robotframework-browser/issues/886
