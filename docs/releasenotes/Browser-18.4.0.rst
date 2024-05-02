======================
Browser library 18.4.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.4.0 is a new release with
enchancement for creating translation enhancements and bug fixes to keyword
documentation. All issues targeted for Browser library v18.4.0 can be found
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
install it manually. Browser library 18.4.0 was released on Thursday May 2, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.43.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Compare translations (`#3543`_)
-------------------------------
Enhance rfbrowser command to compare translation json file checksum from the checksum from library keyword doc.
Output must list all keyword which where sha256 sum does not match. Also if there is keyword which can not be
anymore found (either from library or from translation file) must be listed in the output.

Fix translation documentation in README (`#3518`_)
--------------------------------------------------
Many thanks for Lukas Boekenoogen fixing typos in README documentation

Fix typos in library init and intro documentation  (`#3525`_)
-------------------------------------------------------------
Again many thanks for Lukas Boekenoogen fixing typos in library into documentation.


Acknowledgements
================

Documentation: Get Cookies "expiry" value should be "expires" instead (`#3532`_)
--------------------------------------------------------------------------------
Many thanks anacomparada for fixing Get Cookies documentation.

Wait For Response's response display Error 'the JSON object must be str, bytes or bytearray, not NoneType' (`#3549`_)
---------------------------------------------------------------------------------------------------------------------
Handle empty response body correctly. 

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3543`_
      - enhancement
      - critical
      - Compare translations
    * - `#3518`_
      - bug
      - high
      - Fix translation documentation in README
    * - `#3525`_
      - bug
      - high
      - Fix typos in library init and intro documentation
    * - `#3530`_
      - bug
      - high
      - Improve Wait Until Network Is Idle keyword deprecation warning to contain information on browser transform
    * - `#3532`_
      - bug
      - medium
      - Documentation: Get Cookies "expiry" value should be "expires" instead
    * - `#3549`_
      - bug
      - medium
      - Wait For Response's response display Error 'the JSON object must be str, bytes or bytearray, not NoneType'

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.4.0>`__.

.. _#3543: https://github.com/MarketSquare/robotframework-browser/issues/3543
.. _#3518: https://github.com/MarketSquare/robotframework-browser/issues/3518
.. _#3525: https://github.com/MarketSquare/robotframework-browser/issues/3525
.. _#3530: https://github.com/MarketSquare/robotframework-browser/issues/3530
.. _#3532: https://github.com/MarketSquare/robotframework-browser/issues/3532
.. _#3549: https://github.com/MarketSquare/robotframework-browser/issues/3549
