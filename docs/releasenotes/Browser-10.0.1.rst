======================
Browser library 10.0.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 10.0.1 is a new release with
bug fix for Wait For Element State keyword. All issues targeted for Browser
library v10.0.1 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init

to install the latest available release or use
::
   pip install robotframework-browser==10.0.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 10.0.1 was released on Thursday October 28, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.16.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av10.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Elements State detached broken in version 10.0.0 (`#1437`_)
-----------------------------------------------------------
There was regression in 10.0 release which broke the Wait For Element State keyword when
using detached state. This is not fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1437`_
      - bug
      - critical
      - Elements State detached broken in version 10.0.0

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av10.0.1>`__.

.. _#1437: https://github.com/MarketSquare/robotframework-browser/issues/1437
