======================
Browser library 19.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.3.0 is a new release with
enhancements to Browser library docker container and bug fixes Get Element
States, Start/Stop Coverage keywords and fixes to rfbrowser entry point
documentation. All issues targeted for Browser library v19.3.0 can be
found from the `issue tracker`_.
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
install it manually. Browser library 19.3.0 was released on Thursday January 30, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.50.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Stop Coverage keyword should tell if it could not find file defined in config_file argument in Start Coverage keyword (`#3990`_)
--------------------------------------------------------------------------------------------------------------------------------
Added better logging if the config_file argument file can not be found. Logging is enhanced in
both Start Coverage and Stop Coverage keywords.

Get Element States keyword returns incorrect state if elements is not input type (`#4037`_)
--------------------------------------------------------------------------------------------
There was bug how readonly state was handled in Get Element States keyword. Playwright
started raising an error if element is not input like and this handling was incorrectly
fixes in Browser library side. Now Get Element States keyword returns correct state, also
if element is disabled it is considered readonly.

Issues during python package installation via pip in docker image v19.2.0 (`#4034`_)
--------------------------------------------------------------------------------------
19.2.0 release updated docker base image to Unbuntu Noble, made by Playwright team.
Because Noble prevents installation to system Python. In 19.2 release Browser library
forced installation to system Python. This caused issues with pip installation for people
using our container. Now Browser library is installed to Python virtual environent under
the pwuser, in .venv folder. Virtual environment is activated for the pwuser and
this should fix the installation issues for users.

Acknowledgements
================

Fix entry point documentation (`#4017`_)
-----------------------------------------
Many thanks for William Looman for fixing the entry point documentation
and doing some internal refactoring for module names.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3990`_
      - bug
      - high
      - Stop Coverage keyword should tell if it could not find file defined in config_file argument in Start Coverage keyword
    * - `#4037`_
      - bug
      - high
      - Get Element States keyword returns incorrect state if elements is not input type
    * - `#4034`_
      - enhancement
      - high
      - Issues during python package installation via pip in docker image v19.2.0
    * - `#4017`_
      - bug
      - medium
      - Fix entry point documentation

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.3.0>`__.

.. _#3990: https://github.com/MarketSquare/robotframework-browser/issues/3990
.. _#4037: https://github.com/MarketSquare/robotframework-browser/issues/4037
.. _#4034: https://github.com/MarketSquare/robotframework-browser/issues/4034
.. _#4017: https://github.com/MarketSquare/robotframework-browser/issues/4017
