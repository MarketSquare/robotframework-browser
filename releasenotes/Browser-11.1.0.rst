======================
Browser library 11.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 11.1.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v11.1.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==11.1.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 11.1.0 was released on Friday December 10, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.17.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av11.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Select Options By keyword should return options which was selected (`#1594`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1594`_
      - enhancement
      - high
      - Select Options By keyword should return options which was selected
    * - `#1589`_
      - bug
      - medium
      - Document that Get Text keyword also work with <input> and <textarea> elements.
    * - 5cf90c43_
      - docs
      - ---
      - Document sharing state between pages ((https://github.com/MarketSquare/robotframework-browser/commit/5cf90c43))
    * - `#1609`_
      - docs
      - ---
      - In depth examples 
    * - `7aefb973`_
      - docs
      - ---
      - Improve documentation of Download and Promise to Download File
    * - `4e48629d`_
      - docs
      - ---
      - Document in release notes that RF 4.0+ is minimum required version
    * - `fc111f82`_
      - docs
      - ---
      - Improve Select Options By documentation and examples
    * - ---
      - fix
      - ---
      - Fix type stub generation
    * - ---
      - enhancement
      - ---
      - Support node 16
    * - ---
      - docs
      - ---
      - Document that Get Text also works with input and textarea elements


Altogether 11 significant changes. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av11.1.0>`__.

.. _#1594: https://github.com/MarketSquare/robotframework-browser/issues/1594
.. _#1589: https://github.com/MarketSquare/robotframework-browser/issues/1589
.. _5cf90c43: https://github.com/MarketSquare/robotframework-browser/commit/5cf90c43
.. _#1609: https://github.com/MarketSquare/robotframework-browser/issues/1609
.. _7aefb973: https://github.com/MarketSquare/robotframework-browser/commit/7aefb973
.. _4e48629d: https://github.com/MarketSquare/robotframework-browser/commit/4e48629d
.. _fc111f82: https://github.com/MarketSquare/robotframework-browser/commit/fc111f82
