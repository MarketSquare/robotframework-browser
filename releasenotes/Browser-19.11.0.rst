=======================
Browser library 19.11.0
=======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.11.0 is a new release which
add support for local-network-access in New Context keyword. Also robotidy is
switched to robotframework-robocop because robotidy is deprecated. Also there are
some Minor adjustments to Promise To Upload File keyword. All issues targeted for
Browser library v19.11.0 can be found from the `issue tracker`_.
For first time installation with pip_ and BrowserBatteries_ just run
::
   pip install robotframework-browser robotframework-browser-batteries
   rfbrowser install
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser robotframework-browser-batteries
   rfbrowser clean-node
   rfbrowser install
For first time installation with pip_ with Browser library only, just run
::
   pip install robotframework-browser
   rfbrowser init
If you upgrading from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and
install it manually. Browser library 19.11.0 was released on Sunday November 23, 2025.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.56.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _BrowserBatteries: https://pypi.org/project/robotframework-browser-batteries/
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.11.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Update robotframework-tidy to robotframework-robocop (`#4539`_)
---------------------------------------------------------------
robotframework-tidy is switched to robotframework-robocop because robotidy is deprecated.
The functionality remains the same.

Support for local-network-access in New Context permissions (`#4549`_)
----------------------------------------------------------------------
Added support for local-network-access in New Context permissions.


Minor adjustments to promise_to_upload_file keyword (`#4546`_)
--------------------------------------------------------------
Many thanks to Luis A Gomez-Tinoco for making Minor adjustments to Promise To Upload
File keyword (`#4546`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4539`_
      - enhancement
      - high
      - Update robotframework-tidy to robotframework-robocop
    * - `#4549`_
      - feature
      - high
      - Support for local-network-access in New Context permissions
    * - `#4546`_
      - bug
      - medium
      - Mirod adjustements to promise_to_upload_file keyword
    * - `#3150`_
      - enhancement
      - medium
      - Run minimal docker tests on every commit

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.11.0>`__.

.. _#4539: https://github.com/MarketSquare/robotframework-browser/issues/4539
.. _#4549: https://github.com/MarketSquare/robotframework-browser/issues/4549
.. _#4546: https://github.com/MarketSquare/robotframework-browser/issues/4546
.. _#3150: https://github.com/MarketSquare/robotframework-browser/issues/3150
