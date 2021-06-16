=====================
Browser library 5.1.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 5.1.0 is a new release with
support Playwright traces and possibility to record locators and bug fixes.
All issues targeted for Browser library v5.1.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==5.1.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 5.1.0 was released on Wednesday June 16, 2021. Browser supports
Python 3.7+, and Robot Framework 3.2+.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av5.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Record selectors (`#1080`_)
---------------------------
Library has not possibility to record selecors when tests are created. Mikko
made video which explain the details of feature better: https://www.youtube.com/watch?v=IDAGxNxksg0

Add support to enable trace recording (`#1072`_)
------------------------------------------------
Playwright has added possibility to record trace file: https://playwright.dev/docs/trace-viewer/
Library has not possible to record trace file and view the file with command
::
   rfbowser show-trace -F /path/to/trace.zip

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1080`_
      - enhancement
      - critical
      - Record selectors
    * - `#1072`_
      - enhancement
      - high
      - Add support to enable trace recording
    * - `#1070`_
      - bug
      - medium
      - Fix warning message in keywords which resolves secred internally

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av5.1.0>`__.

.. _#1080: https://github.com/MarketSquare/robotframework-browser/issues/1080
.. _#1072: https://github.com/MarketSquare/robotframework-browser/issues/1072
.. _#1070: https://github.com/MarketSquare/robotframework-browser/issues/1070
