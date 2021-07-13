=====================
Browser library 5.2.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 5.2.0 is a new release with
support saving storage state to disk and using state when opening context.
Also there are few bug fixes.
All issues targeted for Browser library v5.2.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==5.2.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 5.2.0 was released on Tuesday July 13, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av5.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Allow reusing already authenticated contexts when opening a new context (`#1030`_)
----------------------------------------------------------------------------------
It is not possible to save cookies and storage state to disk and reuse the state
when opening new context. 

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1030`_
      - enhancement
      - high
      - Allow reusing already authenticated contexts when opening a new context

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av5.2.0>`__.

.. _#1030: https://github.com/MarketSquare/robotframework-browser/issues/1030
