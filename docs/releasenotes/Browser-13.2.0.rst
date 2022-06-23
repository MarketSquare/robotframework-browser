======================
Browser library 13.2.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 13.2.0 is a new release with
enhancements to Get Elements States and Evaluate JavaScript keyword and bug fixes
when installing in Windows OS. All issues targeted for Browser library
v13.2.0 can be found from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and 
install it manually. Browser library 13.2.0 was released on Friday June 24, 2022. 
Browser supports Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.22.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av13.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Timeout argument on 'New Browser' (`#2064`_)
--------------------------------------------
new Browser timeout argument did not work properly in all values and
this is now fixed.

Many thanks to Luis A Gomez-Tinoco for providing a PR to fix the problem.

Release 13.1.0 may be affected by CVE-2022-25878 (`#2099`_)
-----------------------------------------------------------
Release 13.1.0 contained a dependency which was affected by CVE-2022-25878.
This release updated dependencies and CVE-2022-25878 is fixed.

Get Element States keyword in presenter mode (`#2068`_)
-------------------------------------------------------
Get Element States keyword did not always work correctly if presenter
mode was enabled. Keyword did return incorrect states and this should be
now fixed.

Wait For Navigation fails: 'str' object has no attribute 'name' (`#2081`_)
--------------------------------------------------------------------------
There was a bug in internal argument conversion which caused Wait For Navigation
keyword to fail in few caes. This is now fixed.

Many thanks to Luis A Gomez-Tinoco for providing a PR to fix the problem.

Rfbrowser init fails downloading chromium (Logger seems to be at fault) (`#2083`_)
----------------------------------------------------------------------------------
rfboroser init writes a log file, but with Windows OS, writing the log file
fails on string encoding problem. This issue should be now fixed.

Improved StrictMode behavior of Evaluate JavaScript (`#2109`_)
--------------------------------------------------------------
Evaluate JavaScript keyword could encounter strict mode violation, even when
finding multiple elements was desired. This prolem is now fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2064`_
      - bug
      - critical
      - Timeout argument on 'New Browser'
    * - `#2099`_
      - bug
      - critical
      - Release 13.1.0 may be affected by CVE-2022-25878
    * - `#2068`_
      - bug
      - high
      - Get Element States keyword in presenter mode
    * - `#2081`_
      - bug
      - high
      - Wait For Navigation fails: 'str' object has no attribute 'name'
    * - `#2083`_
      - bug
      - high
      - Rfbrowser init fails downloading chromium (Logger seems to be at fault)
    * - `#2109`_
      - enhancement
      - high
      - improved StrictMode behavior of Evaluate JavaScript

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av13.2.0>`__.

.. _#2064: https://github.com/MarketSquare/robotframework-browser/issues/2064
.. _#2099: https://github.com/MarketSquare/robotframework-browser/issues/2099
.. _#2068: https://github.com/MarketSquare/robotframework-browser/issues/2068
.. _#2081: https://github.com/MarketSquare/robotframework-browser/issues/2081
.. _#2083: https://github.com/MarketSquare/robotframework-browser/issues/2083
.. _#2109: https://github.com/MarketSquare/robotframework-browser/issues/2109
