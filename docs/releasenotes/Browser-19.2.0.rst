======================
Browser library 19.2.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.2.0 is a new release with
updated Docker image to noble. Also there fixes to documentation and
cleaning the coverage directory when new RF execution starts. Also
when we start node process, waiting time is increased to avoid
random failures. All issues targeted for Browser library v19.2.0 can be
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
install it manually. Browser library 19.2.0 was released on Sunday January 26, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.50.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
Update docker to use Playwright noble (`#4019`_)
------------------------------------------------
Playwright stopped relasing focal Docker image, this release start to
 use noble image when image is build.

Increase the node process starting waiting time (`#4005`_)
----------------------------------------------------------
When starting node process, waiting time is increased to avoid random failures
when first keyword is executed.

When new RF execution starts, coverage directory is not deleted (`#4006`_)
-------------------------------------------------------------------------
When new RF execution starts, coverage directory is not deleted, this is fixed.

Acknowledgements
================

Example for Set Geolocation is wrong, fix it. (`#4015`_)
--------------------------------------------------------
Many thanks for Lukas Boekenoogen for fixing Set Geolocation documentation.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4019`_
      - enhancement
      - critical
      - Update docker to use Playwright noble
    * - `#4005`_
      - bug
      - high
      - Increase the node process starting waiting time
    * - `#4006`_
      - bug
      - high
      - When new RF execution starts, coverage directory is not deleted
    * - `#4015`_
      - bug
      - medium
      - Example for Set Geolocation is wrong, fix it.

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.2.0>`__.

.. _#4019: https://github.com/MarketSquare/robotframework-browser/issues/4019
.. _#4005: https://github.com/MarketSquare/robotframework-browser/issues/4005
.. _#4006: https://github.com/MarketSquare/robotframework-browser/issues/4006
.. _#4015: https://github.com/MarketSquare/robotframework-browser/issues/4015
