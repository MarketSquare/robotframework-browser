======================
Browser library 18.8.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.8.1 is a new release with
Playwright 1.47. Library functionality is same as in Browser 18.8.0.
All issues targeted for Browser library v18.8.1 can be found
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
install it manually. Browser library 18.8.1 was released on Friday September 13, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.47.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.8.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Create release with Playwright 1.47.0 (`#3787`_)
----------------------------------------------
New release with Playwright 1.47.0 version. Does not contain other new features or fixes.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3787`_
      - bug
      - high
      - Create release with Playwright 1.47.0

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.8.1>`__.

.. _#3787: https://github.com/MarketSquare/robotframework-browser/issues/3787
