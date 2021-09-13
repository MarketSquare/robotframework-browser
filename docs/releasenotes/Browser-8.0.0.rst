=====================
Browser library 8.0.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 8.0.0 is a new release with
enables Playwright strict mode and other bug fixes.
All issues targeted for Browser library v8.0.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==8.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 8.0.0 was released on Monday September 13, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.14.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av8.0.0


.. contents::
   :depth: 2
   :local:

Backwards incompatible and most important changes
=================================================

- Strict mode (`#1233`_)
------------------------
This release enables Playwright strict mode for the browser library. Strict mode is enabled by default
and strict mode can be controlled by library import or by Set Strict Mode keyword. When strict mode is
enabled and if keyword selector points to multiple elements, keyword will fail. If strict mode is mode
is disabled, keyword will not fail if selector does point to multiple elements.

Keywords which should interact with single element, like Click and Get Text keyword uses strict mode.
Keywords which should interact with multiple elements, like Get Elements are do not use strict mode.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1233`_
      - enhancement
      - critical
      - Strict mode

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av8.0.0>`__.

.. _#1233: https://github.com/MarketSquare/robotframework-browser/issues/1233
