======================
Browser library 14.4.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 14.4.1 is a new release with
bug fixes to version numbers. Other ways this is exactly same as 14.0.0
All issues targeted for Browser library v14.4.1 can be found
from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and 
install it manually. Browser library 14.4.1 was released on Saturday January 7, 2023. 
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.29.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av14.4.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Fix version numbers in release 14.0 (`#2529`_)
----------------------------------------------
With release 14.0.0 version number was not correctly set in code.
This release fixes the problem.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2529`_
      - bug
      - critical
      - Fix version numbers in release 14.0

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av14.4.1>`__.

.. _#2529: https://github.com/MarketSquare/robotframework-browser/issues/2529
