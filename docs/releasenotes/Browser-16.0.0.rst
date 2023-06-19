======================
Browser library 16.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 16.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v16.0.0 can be found
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
install it manually. Browser library 16.0.0 was released on Monday February 6, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.30.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v16.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

New Browser to skip if exists and switch (`#1319`_) BWIC
--------------------------------------------------------

`New Browser`_ keyword does by default switch to an existing browser as long as it is configured the same way.
That has no affect on the "Contexts" you are using or independence of sessions, but should speedup your tests and save resources.
If you call the keyword again with different arguments, it still will open a new Browser with that new config.
This can be configured by the argument `reuse_existing=False` to always open a new browser.

Get Browser Console Logs support (`#2176`_)
--------------------------------------------
`Get Console Log`_ keyword and `Get Page Errors`_ keyword are new.
They do return a list of console messages and errors from the browser.
See their keyword documentation for more details.

Take Screenshot keyword supports returning the image (`#2625`_)
---------------------------------------------------------------
`Take Screenshot`_ keyword now supports returning the image as a variable and deactivate its logging.
This can be done by setting the argument `return_as=<option>` and `log_screenshot=False`.

Return types can be either `bytes` or `base64` of the screenshot or the path to the screenshot as
`string` or `pathlib.Path` object.

If `log_screenshot` is set to `False`, the screenshot will not be logged to the log.html.

Backwards incompatible changes
==============================

- New Browser to skip if exists and switch (`#1319`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1319`_
      - enhancement
      - critical
      - New Browser to skip if exists and switch
    * - `#2176`_
      - enhancement
      - high
      - Get Browser Console Logs  support
    * - `#2535`_
      - bug
      - medium
      - New persistent context - "Switch page" to tab opened by a test cannot see the new tab 
    * - `#2625`_
      - enhancement
      - medium
      - Take Screenshot should be able to return the actual image to instead of path

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av16.0.0>`__.


.. _New Browser: https://marketsquare.github.io/robotframework-browser/Browser.html#New%20Browser
.. _Get Console Log: https://marketsquare.github.io/robotframework-browser/Browser.html#Get%20Console%20Log
.. _Get Page Errors: https://marketsquare.github.io/robotframework-browser/Browser.html#Get%20Page%20Errors
.. _Take Screenshot: https://marketsquare.github.io/robotframework-browser/Browser.html#Take%20Screenshot
.. _#1319: https://github.com/MarketSquare/robotframework-browser/issues/1319
.. _#2176: https://github.com/MarketSquare/robotframework-browser/issues/2176
.. _#2535: https://github.com/MarketSquare/robotframework-browser/issues/2535
.. _#2625: https://github.com/MarketSquare/robotframework-browser/issues/2625
