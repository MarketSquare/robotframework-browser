======================
Browser library 12.2.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 12.2.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v12.2.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==12.2.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 12.2.0 was released on Sunday March 13, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.19.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av12.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- Should be able to change color and timeout for "enable_presenter_mode" argument in the "Library" (`#1816`_)
- JS extensions to support more than just positional arguments (`#1833`_)
- Added keyword `Drag And Drop Relative To` (`#1838`_)
- Adding Table related keywords (`Get Table Cell Element`) (`#1847`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1816`_
      - enhancement
      - high
      - Should be able to change color and timeout for "enable_presenter_mode" argument in the "Library"
    * - `#1833`_
      - enhancement
      - high
      - JS extensions to support more than just positional arguments
    * - `#1838`_
      - enhancement
      - high
      - Added keyword `Drag And Drop Relative To`
    * - `#1847`_
      - ---
      - high
      - Adding Table related keywords (`Get Table Cell Element`)
    * - `#1716`_
      - enhancement
      - medium
      - Extension of keyword Drag And Drop By Coordinates: make release of the mouse button flexible
    * - `#1835`_
      - enhancement
      - medium
      - Should be able to highlight for "Get Text" keyword also when the "enable_presenter_mode" argument is True in the "Library"
    * - `#1843`_
      - ---
      - ---
      - Added Table Keywords
    * - `#1850`_
      - ---
      - ---
      - added Keyword `Scroll To Element`
    * - `#1852`_
      - ---
      - ---
      - New Keyword `Scroll To Element`
    * - `#1853`_
      - ---
      - ---
      - Change Dict Returning Keywords to Robot DotDict class
    * - `#1854`_
      - ---
      - ---
      - New `Evaluate JavaScript` Keyword

Altogether 11 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av12.2.0>`__.

.. _#1816: https://github.com/MarketSquare/robotframework-browser/issues/1816
.. _#1833: https://github.com/MarketSquare/robotframework-browser/issues/1833
.. _#1838: https://github.com/MarketSquare/robotframework-browser/issues/1838
.. _#1847: https://github.com/MarketSquare/robotframework-browser/issues/1847
.. _#1716: https://github.com/MarketSquare/robotframework-browser/issues/1716
.. _#1835: https://github.com/MarketSquare/robotframework-browser/issues/1835
.. _#1843: https://github.com/MarketSquare/robotframework-browser/issues/1843
.. _#1850: https://github.com/MarketSquare/robotframework-browser/issues/1850
.. _#1852: https://github.com/MarketSquare/robotframework-browser/issues/1852
.. _#1853: https://github.com/MarketSquare/robotframework-browser/issues/1853
.. _#1854: https://github.com/MarketSquare/robotframework-browser/issues/1854
