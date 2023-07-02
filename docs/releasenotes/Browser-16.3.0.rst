======================
Browser library 16.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 16.3.0 is a new release with
enhancements to Take Screenshot keyword and bug fixes Click keyword. This release
drops support for NodeJS 14 and deprecates support for Python 3.7.
All issues targeted for Browser library v16.3.0 can be found
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
install it manually. Browser library 16.3.0 was released on Sunday July 2, 2023.
Browser supports Python 3.7+, Node 16/18 LTS and Robot Framework 5.0+.
Support for Python 3.7 has been deprecated and release 16.4 will drop the
support for Python 3.7. Users are strong advised to upgrade their
Python version to one which supported by Python community.
Library was tested with Playwright 1.35.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v16.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Drop NodeJS 14 support.  (`#2859`_)
-----------------------------------
NodeJs 14 is not anymore supported, Playwright dropped support for NodeJS 14 few
releases ago and therefore we are also dropping support for it.

Deprecate support for Python 3.7 (`#2906`_)
-------------------------------------------
Support for Python 3.7 is deprecated and next release will remove Python 3.7
support. Python 3.7 end of life was 2023-06-27

Can not close context if web browser tab was auto-closed (`#2089`_)
-------------------------------------------------------------------
Sometimes, when Click keyword closes the page, it can cause an error: Target closed error
This error from Playwright side is suppressed, but logged in the keyword.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2859`_
      - enhancement
      - critical
      - Drop NodeJS 14 support. 
    * - `#2906`_
      - enhancement
      - critical
      - Deprecate support for Python 3.7
    * - `#2089`_
      - bug
      - high
      - Can not close context if web browser tab was auto-closed
    * - `#2335`_
      - bug
      - medium
      - Augment the documentation of Highlight Elements for the case that it apparently did nothing
    * - `#2868`_
      - bug
      - medium
      - Plugin tag should be a capital
    * - `#2854`_
      - enhancement
      - medium
      - Improve Take Screenshot keyword to support latest additions from PW

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av16.3.0>`__.

.. _#2859: https://github.com/MarketSquare/robotframework-browser/issues/2859
.. _#2906: https://github.com/MarketSquare/robotframework-browser/issues/2906
.. _#2089: https://github.com/MarketSquare/robotframework-browser/issues/2089
.. _#2335: https://github.com/MarketSquare/robotframework-browser/issues/2335
.. _#2868: https://github.com/MarketSquare/robotframework-browser/issues/2868
.. _#2854: https://github.com/MarketSquare/robotframework-browser/issues/2854
