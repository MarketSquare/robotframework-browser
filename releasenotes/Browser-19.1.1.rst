======================
Browser library 19.1.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.1.1 is a new hotfix
release which fixes two critical issues found in the previous release.
The previous release used the protobuf package which was yanked from PyPI.
Also there was bug for rfbrowser init command which prevented the library
installation. All issues targeted for Browser library v19.1.1 can be found
from the `issue tracker`_. For first time installation with pip_, just run
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
install it manually. Browser library 19.1.1 was released on Wednesday December 11, 2024.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.49.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

"rfbrowser init" fails due to "UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 1022-1023: unexpected end of data" after latest 19.1.0 release (`#3938`_)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
There was regression, which caused rfbrowser init command to fail with UnicodeDecodeError. This was caused by the latest release beatifying the output of the rfbrowser
init command. This issue is now fixed. The rfbrowser init command should now work as expected in all environments.

Protobuf version used by robotframework-browser was yanked from PyPI (`#3946`_)
-------------------------------------------------------------------------------
The protobuf package used by robotframework-browser was yanked from PyPI. This caused the installation of
the library to fail. This issue is now fixed by upgrading the protobuf package to the latest version.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3938`_
      - bug
      - critical
      - "rfbrowser init" fails due to "UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 1022-1023: unexpected end of data" after latest 19.1.0 release
    * - `#3946`_
      - bug
      - critical
      - Protobuf version used by robotframework-browser was yanked from PyPI

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.1.1>`__.

.. _#3938: https://github.com/MarketSquare/robotframework-browser/issues/3938
.. _#3946: https://github.com/MarketSquare/robotframework-browser/issues/3946
