======================
Browser library 19.1.2
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.1.2 is a new release with
which bumbs monocart-coverage-reports to 2.11.5. The previous version of
monocart-coverage-reports could crash the node side grpc server. All issues
targeted for Browser library v19.1.2 can be found from the `issue tracker`_.
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
install it manually. Browser library 19.1.2 was released on Friday December 20, 2024.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.49.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.1.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Update monocart-coverage-reports Node dependecy to the latest version (`#3973`_)
--------------------------------------------------------------------------------
The previous version of monocart-coverage-reports could crash the node side grpc server
when coverage reports were generated under certain conditions. This update fixes the issue.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3973`_
      - bug
      - critical
      - Update monocart-coverage-reports Node dependecy to the latest version

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.1.2>`__.

.. _#3973: https://github.com/MarketSquare/robotframework-browser/issues/3973
