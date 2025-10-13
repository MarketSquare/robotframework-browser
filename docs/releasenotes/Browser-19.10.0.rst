=======================
Browser library 19.10.0
=======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.10.0 is a new release with
new Get Aria Snapshots keyword. Also we dropped Python 3,9 and Robot Framework 5.0.
Also Python 3.14 is now supported. All issues targeted for Browser library
v19.10.0 can be found from the `issue tracker`_.
For first time installation with pip_ and BrowserBatteries just run
::
   pip install robotframework-browser robotframework-browser-batteries
   rfbrowser install
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser robotframework-browser-batteries
   rfbrowser clean-node
   rfbrowser install
For first time installation with pip_ with Browser library only, just run
::
   pip install robotframework-browser
   rfbrowser init
If you upgrading from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and
install it manually. Browser library 19.10.0 was released on Monday October 13, 2025.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.56.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.10.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Get Aria Snapshots for Page (as alternative to 'Get Page Source') (`#4471`_)
------------------------------------------------------------------------------
New keyword to get the ARIA tree snapshot of the current page. This is useful
for accessibility testing and for verifying the structure of the page for LLM
based testing.

Browser.pyi stub file generation does not work if python > 3.9 (`#4475`_)
------------------------------------------------------------------------
Fixed the stub file generation for newer Python versions. Now we use MyPy
directly instead of relying on Robot Framework's stub generation.

Drop support for Robot Framework 5 and Python 3.9 (`#4464`_)
------------------------------------------------------------
We now require Robot Framework 6.1+ and Python 3.10+. This allows us to use
newer language features and keep the codebase cleaner.

Python 3.14 support (`#4476`_)
------------------------------
We have tested and verified that Browser library works with Python 3.14.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4475`_
      - bug
      - high
      - Browser.pyi stub file genration does not work if python > 3.9
    * - `#4464`_
      - enhancement
      - high
      - Drop support for Robot Framework 5 and Python 3.9
    * - `#4471`_
      - enhancement
      - high
      - Get Aria Snapshots for Page (as alternative to 'Get Page Source')
    * - `#4476`_
      - enhancement
      - high
      - Python 3.14 support

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.10.0>`__.

.. _#4475: https://github.com/MarketSquare/robotframework-browser/issues/4475
.. _#4464: https://github.com/MarketSquare/robotframework-browser/issues/4464
.. _#4471: https://github.com/MarketSquare/robotframework-browser/issues/4471
.. _#4476: https://github.com/MarketSquare/robotframework-browser/issues/4476
