======================
Browser library 19.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.1.0 is a new release with enhancements and bug fixes.
All issues targeted for Browser library v19.1.0 can be found
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
install it manually. Browser library 19.1.0 was released on Sunday December 1, 2024.
Happy first Advent ✨🎄🎅🏿🎅🎅🏼🧑🏿‍🎄🧑‍🎄🧑🏻‍🎄!

Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.49.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.1.0


.. contents::
   :depth: 2
   :local:

Enhancements
===========================

Improved Converage to use it in real live (`#3927`_)
-----------------------------------------------------

Code coverage logging that was introduced in 19.0.0 was improved to be more useful in real live.
We improved the way how top define the path where the coverage reports are stored. See docs.

Also we introduced an automatic saving of the coverage report when the page or context is closed.
This works as well with auto-closing of pages and contexts.


Regression Bug fixes
===========================

- Wait For keyword raise exception for wrong data type (`#3922`_)
- rfbrowser logs errors when running robotframework with --dryrun argument (`#3915`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3922`_
      - bug
      - critical
      - Wait For keyword raise exception for wrong data type
    * - `#3927`_
      - enhancement
      - critical
      - Improved Converage to use it in real live
    * - `#3915`_
      - bug
      - high
      - rfbrowser logs errors when running robotframework with --dryrun argument
    * - `#3668`_
      - enhancement
      - high
      - Add the kwarg timeout to Connect to Browser
    * - `#3924`_
      - bug
      - medium
      - A logger.console statement in get_element_by_role bloating console output

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.1.0>`__.

.. _#3922: https://github.com/MarketSquare/robotframework-browser/issues/3922
.. _#3927: https://github.com/MarketSquare/robotframework-browser/issues/3927
.. _#3915: https://github.com/MarketSquare/robotframework-browser/issues/3915
.. _#3668: https://github.com/MarketSquare/robotframework-browser/issues/3668
.. _#3924: https://github.com/MarketSquare/robotframework-browser/issues/3924
