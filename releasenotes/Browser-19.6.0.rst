======================
Browser library 19.6.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.6.0 is a new release with
enhancement to Take Screenshot keyword to support UUID and bug fixe to
Take Screenshot keyword when used from Python. All issues targeted for
Browser library v19.6.0 can be found from the `issue tracker`_.
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
install it manually. Browser library 19.6.0 was released on Sunday June 15, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.53.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.6.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Take Screenshot fails when Browser is run on python after 19.5.0 (`#4224`_)
---------------------------------------------------------------------------
Take Screenshot keyword was failing when used from Python after
Robot Framework Browser library 19.5.0. many thanks to
gitkatsi for providing a fix for this issue.

Unique names for screenshots (`#4244`_)
---------------------------------------
Take Screenshot keyword now supports unique names for screenshots
by using UUID. This is useful when you want to take multiple screenshots
with pabot.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4224`_
      - bug
      - high
      - Take Screenshot fails when Browser is run on python after 19.5.0
    * - `#4244`_
      - enhancement
      - high
      - Unique names for screenshots

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.6.0>`__.

.. _#4224: https://github.com/MarketSquare/robotframework-browser/issues/4224
.. _#4244: https://github.com/MarketSquare/robotframework-browser/issues/4244
