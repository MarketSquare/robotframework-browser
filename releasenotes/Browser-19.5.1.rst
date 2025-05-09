======================
Browser library 19.5.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.5.1 is a new hotfix
release with bugfix for Robot Framework version older than 7.0.
All issues targeted for Browser library v19.5.1 can be found
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
install it manually. Browser library 19.5.1 was released on Friday May 9, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.52.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.5.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

With 19.5.0 "rfbrowser init" fails for Robot Framework version older than 7.0 (`#4206`_)
----------------------------------------------------------------------------------------
The "rfbrowser init" command fails with Robot Framework version older than 7.0. Also
fixed similar issued in few other places in the code.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4206`_
      - bug
      - critical
      - With 19.5.0 "rfbrowser init" fails for Robot Framework version older than 7.0

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.5.1>`__.

.. _#4206: https://github.com/MarketSquare/robotframework-browser/issues/4206
