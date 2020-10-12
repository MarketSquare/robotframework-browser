=====================
Browser library 1.4.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 1.4.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v1.4.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run
::
   pip install --pre --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==1.4.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 1.4.0 was released on Monday October 12, 2020. Browser supports
Python **ADD VERSIONS**, Playwright **ADD VERSIONS** and
Robot Framework **ADD VERSIONS**.
.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Selenium: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av1.4.0


.. contents::
   :depth: 2
   :local:

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#366`_
      - enhancement
      - high
      - Get Elements should not raise timeout exception when no elements found. It should return an empty list.
    * - `#136`_
      - bug
      - ---
      - Document BrowserLibrarys `Get Selected Options` differences to SeleniumLibrarys `Select Element _`
    * - `#411`_
      - ---
      - ---
      - Open Browser: Option to stop execution on failure and keep browser and page open

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av1.4.0>`__.

.. _#366: https://github.com/MarketSquare/robotframework-browser/issues/366
.. _#136: https://github.com/MarketSquare/robotframework-browser/issues/136
.. _#411: https://github.com/MarketSquare/robotframework-browser/issues/411
