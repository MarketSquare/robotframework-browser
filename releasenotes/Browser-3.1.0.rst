=====================
Browser library 3.1.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 3.1.0 is a new release with
with Playwright 1.8.0. All issues targeted for Browser library v3.1.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==3.1.0
   rfbrowser init

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 3.1.0 was released on Thursday January 21, 2021. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av3.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Update to latest Playwright (`#681`_)
-------------------------------------
This release is same as 3.0.0, but it contains Playwright 1.8.0 which should
resolve few issue that have open in the issue tracker.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#681`_
      - enhancement
      - critical
      - Update to latest Playwright

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av3.1.0>`__.

.. _#681: https://github.com/MarketSquare/robotframework-browser/issues/681
