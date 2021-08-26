=====================
Browser library 7.1.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 7.1.0 is a new release with
run on failure supporting keyword supporting arguments enhancements and
enhancements in keyword documentation. Also there are bug fixes in this
release. All issues targeted for Browser library v7.1.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==7.1.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 7.1.0 was released on Saturday August 21, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.14.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av7.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Write example to keyword documentation (`#1214`_)
Keyword docs are now updated and contains examples.
---------------------------------------------------

Enhance run on failure functionality to accept arguments (`#1215`_)
-------------------------------------------------------------------
Run on failure keyword supports now arguments in library import.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1214`_
      - enhancement
      - high
      - Write example to keyword documentation
    * - `#1215`_
      - enhancement
      - high
      - Enhance run on failure functionality to accept arguments
    * - `#1227`_
      - bug
      - medium
      - Remove not used regex argument from Wait For Navigation keyword 
    * - `#992`_
      - bug
      - medium
      - Setting browser path by PLAYWRIGHT_BROWSERS_PATH not working anymore
    * - `#1246`_
      - enhancement
      - medium
      - Add support to define node side port in library import

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av7.1.0>`__.

.. _#1214: https://github.com/MarketSquare/robotframework-browser/issues/1214
.. _#1215: https://github.com/MarketSquare/robotframework-browser/issues/1215
.. _#1227: https://github.com/MarketSquare/robotframework-browser/issues/1227
.. _#992: https://github.com/MarketSquare/robotframework-browser/issues/992
.. _#1246: https://github.com/MarketSquare/robotframework-browser/issues/1246
