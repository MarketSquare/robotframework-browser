======================
Browser library 11.2.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 11.2.0 is a new release with
enhancements for setting and clearning permission for the active contex and bug
fixes for not leaking secrets when keyword fails. All issues targeted for Browser
library v11.2.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==11.2.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 11.2.0 was released on Friday January 14, 2022. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.17.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av11.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Feature: Introduce ``AssertionsEngine``'s formatter to BrowserLibrary (`#1645`_)
--------------------------------------------------------------------------------
AssertionEngine support formatters which allows applying changes for the received
and expected value. Formatter are applied for most keyword which use assertions
and formatter must be define before the keyword is called.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1645`_
      - enhancement
      - high
      - Feature: Introduce ``AssertionsEngine``'s formatter to BrowserLibrary
    * - `#1669`_
      - bug
      - medium
      - `url` attribute not listed in docs for `Wait For Response` keyword
    * - `#229`_
      - enhancement
      - medium
      - Expose grantPermissions keyword

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av11.2.0>`__.

.. _#1645: https://github.com/MarketSquare/robotframework-browser/issues/1645
.. _#1669: https://github.com/MarketSquare/robotframework-browser/issues/1669
.. _#229: https://github.com/MarketSquare/robotframework-browser/issues/229
