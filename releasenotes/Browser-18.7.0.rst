======================
Browser library 18.7.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.7.0 is a new release with
Save Page As Pdf and Emulate Media keywords and bug fixes to keyword documentation.
All issues targeted for Browser library v18.7.0 can be found
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
install it manually. Browser library 18.7.0 was released on Friday August 9, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.46.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.7.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add playwright's .pdf() conversion function as keyword (`#3481`_)
----------------------------------------------------------------
There are two new keywords Save Page As Pdf and Emulate Media which
allows to save active page as PDF and control media emulation respectively.
Media emulation is usually used before saving page as PDF.

Acknowledgements
================
Fix typo in new context keyword  (`#3689`_)
-------------------------------------------
Many thanks for rasjani for fixing typo in new context keyword.

Fix typo in library arguments (`#3696`_)
----------------------------------------
Many thanks for rasjani for fixing typo in library arguments.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3481`_
      - enhancement
      - high
      - Add playwright's .pdf() conversion function as keyword
    * - `#3689`_
      - bug
      - medium
      - Fix typo in new context keyword
    * - `#3696`_
      - bug
      - medium
      - Fix typo in library arguments

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.7.0>`__.

.. _#3481: https://github.com/MarketSquare/robotframework-browser/issues/3481
.. _#3689: https://github.com/MarketSquare/robotframework-browser/issues/3689
.. _#3696: https://github.com/MarketSquare/robotframework-browser/issues/3696
