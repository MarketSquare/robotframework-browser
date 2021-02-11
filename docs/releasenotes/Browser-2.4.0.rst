=====================
Browser library 2.4.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 2.4.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v2.4.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==2.4.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 2.4.0 was released on Monday December 14, 2020. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av2.4.0


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
    * - `#296`_
      - enhancement
      - ---
      - Connect Browser keyword
    * - `#579`_
      - ---
      - ---
      - Store screenshots in browser/screenshots and videos in browser/videos by default
    * - `#580`_
      - ---
      - ---
      - Add `logger` and `playwright` arguments to JS keyword signature

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av2.4.0>`__.

.. _#296: https://github.com/MarketSquare/robotframework-browser/issues/296
.. _#579: https://github.com/MarketSquare/robotframework-browser/issues/579
.. _#580: https://github.com/MarketSquare/robotframework-browser/issues/580
