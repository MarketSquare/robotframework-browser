======================
Browser library 18.9.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.9.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v18.9.0 can be found
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
install it manually. Browser library 18.9.0 was released on Monday October 7, 2024.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.47.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.9.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Update of interpreters
----------------------

Due to End-of-Life of Python 3.8 we dropped the support for it. (`#3775`_)

Browser officially also supports NodeJS 22 together with 18 and 20 (`#3810`_)


New Keyword ``Wait For Alerts``
-------------------------------

``Wait For Alerts`` is a new keyword which waits for multiple alerts to be present. (`#3785`_)

This keyword works similar to ``Wait For Alert`` but accepts lists of actions, prompts and messages to be verified.


Improvements to ``Highlight Elements``
--------------------------------------

Depending on the pages box-sizing the border of the highlighted element was not always correct. (`#3614`_)
This is now fixed and the border whick is used to highlight an element is always outside of the selected elements.

``Highlight Elements`` now has a new named-only argument ``mode`` which enables the mode ``playwright``,
which will highlight elements with Playwrights `locator.highlight()` method. (`#3827`_)


``Get BoundingBox`` improvements for non-visible elements
---------------------------------------------------------

``Get BoundingBox`` now fails with proper error message if element is not visible. (`#3651`_)
It did fail before as well, but the error message was not helpful.
If the keyword shall not fail for hidden elements, use the new named-only argument ``allow_hidden`` and set it to ``True``,
which then cases the keyword to return ``${None}`` instead of failing for elements without bounding box.


Initialization of Browser library and Playwright changed
-------------------------------------------------------

Previously the Playwright process was started when the Browser library was imported in Robot Framework but also if libdoc was used.
Which means when i.e. RobotCode gathered the available keywords from Browser a Playwright process was started and all its dependencies were needed.

Also if Browser library was imported, but actually never used, the Playwright process was started and node was needed.

We did now change that behavior so that the Playwright process is started lazily, when the first keyword is called or if extensions are used. (`#3757`_)

This does cause some changes in the behavior of the library, but should not affect the normal usage of the library.

If ``rfbrowser init`` was not executed before it is now not longer directly visible in your Editor that the Browser library is not initialized.
This enables you to use the Browser library in your code without the need to initialize it first, but also postpones the error to a later point.

We also improved the error message shown, if the initialization was not executed. (`#3583`_)
It should now be more clear.




Backwards incompatible changes
==============================

- Drop support of Python 3.8 (`#3775`_)
- Lazy initializing of Playwright (`#3757`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3775`_
      - enhancement
      - critical
      - Drop support of Python 3.8
    * - `#3810`_
      - enhancement
      - critical
      - Support NodeJS 22
    * - `#3286`_
      - bug
      - high
      - Issues with downloadsPath variable
    * - `#3614`_
      - bug
      - high
      - Highlight Elements border has the the wrong position
    * - `#3651`_
      - bug
      - high
      - "Get BoundingBox" fails if element is not visible, wo proper error.
    * - `#3789`_
      - bug
      - high
      - Protobuf gencode version 5.27.2 is older then the runtime version 5.28.1 at playwright.proto
    * - `#3757`_
      - enhancement
      - high
      - Lazy initializing of playwright
    * - `#3827`_
      - enhancement
      - high
      - Add Playwrights `locator.highlight()` mode to `Highlight Elements`
    * - `#3452`_
      - bug
      - medium
      - Improve Error message when importing Browser Library, if rfbrowser init was not executed
    * - `#3557`_
      - enhancement
      - medium
      - Remove the "tips" and ANSI colors on errors
    * - `#3785`_
      - enhancement
      - medium
      - RFB can not handle two consecutives alerts
    * - `#3583`_
      - bug
      - low
      - In rfbrowser init error case print better folder structure

Altogether 12 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.9.0>`__.

.. _#3775: https://github.com/MarketSquare/robotframework-browser/issues/3775
.. _#3810: https://github.com/MarketSquare/robotframework-browser/issues/3810
.. _#3286: https://github.com/MarketSquare/robotframework-browser/issues/3286
.. _#3614: https://github.com/MarketSquare/robotframework-browser/issues/3614
.. _#3651: https://github.com/MarketSquare/robotframework-browser/issues/3651
.. _#3789: https://github.com/MarketSquare/robotframework-browser/issues/3789
.. _#3757: https://github.com/MarketSquare/robotframework-browser/issues/3757
.. _#3827: https://github.com/MarketSquare/robotframework-browser/issues/3827
.. _#3452: https://github.com/MarketSquare/robotframework-browser/issues/3452
.. _#3557: https://github.com/MarketSquare/robotframework-browser/issues/3557
.. _#3785: https://github.com/MarketSquare/robotframework-browser/issues/3785
.. _#3583: https://github.com/MarketSquare/robotframework-browser/issues/3583
