======================
Browser library 17.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 17.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v17.0.0 can be found
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
install it manually. Browser library 17.0.0 was released on Tuesday July 11, 2023.
Browser supports Python 3.8+, Node 16/18 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.35.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v17.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Remove support for Python 3.7 (`#2907`_)
- Frame-Selector >>> does not work with `element=xxx` selector (`#2662`_)
- added Click With Options to deprecated ugly modifiers (`#2617`_)
- Support for PW getBy locators (`#2877`_)
- Add support for multiple JS-Plugins (`#2930`_)
- SessionStorage and LocaStorage keywords shall support frames from different orgigin. (`#2937`_)

Backwards incompatible changes
==============================

- Wait For Response, no way to specify modifiers when using regex for the matcher? (`#2822`_)
- Topic/switched selector strategies for frames to internal: (`#2917`_)
- Removed deprecated Positional Arguments of New Browser, New Context, New Persistent Context, Take Screenshot (`#2931`_)

Deprecated features
===================

- added Click With Options to deprecated ugly modifiers (`#2617`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2907`_
      - enhancement
      - critical
      - Remove support for Python 3.7
    * - `#2662`_
      - bug
      - high
      - Frame-Selector >>> does not work with `element=xxx` selector
    * - `#2617`_
      - enhancement
      - high
      - added Click With Options to deprecated ugly modifiers
    * - `#2877`_
      - enhancement
      - high
      - Support for PW getBy locators
    * - `#2930`_
      - enhancement
      - high
      - Add support for multiple JS-Plugins
    * - `#2937`_
      - enhancement
      - high
      - SessionStorage and LocaStorage keywords shall support frames from different orgigin.
    * - `#2795`_
      - bug
      - medium
      - For "Get Element Count" keyword, combination "iframe selector >>> element selector inside a frame" throws an error, where it shouldn't
    * - `#2875`_
      - bug
      - medium
      - WebKit is not supported when using Persistent Context
    * - `#2822`_
      - bug
      - ---
      - Wait For Response, no way to specify modifiers when using regex for the matcher?
    * - `#2935`_
      - bug
      - ---
      - `Local Storage Set Item` & `Session Storage Set Item` can not have " (quotes) unescaped in value.
    * - `#2917`_
      - enhancement
      - ---
      - Topic/switched selector strategies for frames to internal:
    * - `#2931`_
      - enhancement
      - ---
      - Removed deprecated Positional Arguments of New Browser, New Context, New Persistent Context, Take Screenshot
    * - `#2934`_
      - enhancement
      - ---
      - set loglevel to info if screenshot could not be done because page was not open on failure

Altogether 13 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av17.0.0>`__.

.. _#2907: https://github.com/MarketSquare/robotframework-browser/issues/2907
.. _#2662: https://github.com/MarketSquare/robotframework-browser/issues/2662
.. _#2617: https://github.com/MarketSquare/robotframework-browser/issues/2617
.. _#2877: https://github.com/MarketSquare/robotframework-browser/issues/2877
.. _#2930: https://github.com/MarketSquare/robotframework-browser/issues/2930
.. _#2937: https://github.com/MarketSquare/robotframework-browser/issues/2937
.. _#2795: https://github.com/MarketSquare/robotframework-browser/issues/2795
.. _#2875: https://github.com/MarketSquare/robotframework-browser/issues/2875
.. _#2822: https://github.com/MarketSquare/robotframework-browser/issues/2822
.. _#2935: https://github.com/MarketSquare/robotframework-browser/issues/2935
.. _#2917: https://github.com/MarketSquare/robotframework-browser/issues/2917
.. _#2931: https://github.com/MarketSquare/robotframework-browser/issues/2931
.. _#2934: https://github.com/MarketSquare/robotframework-browser/issues/2934
