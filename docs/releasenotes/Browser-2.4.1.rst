=====================
Browser library 2.4.1
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 2.4.1 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v2.4.1 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==2.4.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 2.4.1 was released on Friday December 18, 2020. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av2.4.1


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
    * - `#600`_
      - ---
      - ---
      - Fix macOS 11.1 by depending on newer playwright version
    * - 
      - ---
      - --§
      - New Playwright CSS selector extensions and other features from 1.7.0 https://github.com/microsoft/playwright/releases/tag/v1.7.0

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av2.4.1>`__.

.. _#600: https://github.com/MarketSquare/robotframework-browser/issues/600
