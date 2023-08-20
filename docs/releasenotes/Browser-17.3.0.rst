======================
Browser library 17.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 17.3.0 is a new release with
New Persistent Context enhancements and bug fixes when switching pages. Also
AssertionEngine is updated and it bring new case insensitive formatter.
All issues targeted for Browser library v17.3.0 can be found
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
install it manually. Browser library 17.3.0 was released on Sunday August 20, 2023.
Browser supports Python 3.8+, Node 16/18 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.37.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v17.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Switching Browser, Context and Pages brings page to front (`#2993`_)
--------------------------------------------------------------------
Every Switch does also brings the current page to front.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2993`_
      - enhancement
      - high
      - Switching Browser, Context and Pages brings page to front
    * - `#2990`_
      - enhancement
      - medium
      - added defaultBrowser and removed non functional args

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av17.3.0>`__.

.. _#2993: https://github.com/MarketSquare/robotframework-browser/issues/2993
.. _#2990: https://github.com/MarketSquare/robotframework-browser/issues/2990
