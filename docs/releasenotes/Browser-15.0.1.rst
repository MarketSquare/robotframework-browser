======================
Browser library 15.0.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 15.0.1 is a new release with
bug fixes on the Plugin API usage with JS extension. All issues targeted for
Browser library v15.0.1 can be found
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
install it manually. Browser library 15.0.1 was released on Monday January 16, 2023. 
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.29.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av15.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Using `call_js_keyword` in Plugin API should not need the dummy page, logger or playwright  arguments. (`#2563`_)
------------------------------------------------------------------------------------------------------------------
Using call_js_keyword in Plugin API should not need the dummy page , logger or playwright arguments. Instead
calling the call_js_keyword function just need the custom arguments.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2563`_
      - bug
      - critical
      - Using `call_js_keyword` in Plugin API should not need the dummy page , logger or playwright  arguments.

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av15.0.1>`__.

.. _#2563: https://github.com/MarketSquare/robotframework-browser/issues/2563
