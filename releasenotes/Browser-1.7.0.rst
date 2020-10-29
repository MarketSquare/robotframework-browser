=====================
Browser library 1.7.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 1.7.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v1.7.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==1.7.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 1.7.0 was released on Monday October 26, 2020. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Selenium: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av1.7.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- When creating new page, library does not obey the `timeout` value. Instead it will timeout in 10seconds.  (`#435`_)
- Wait for response matchers not working (`#230`_)
- Docs for "Wait For Request/Response" have wrong timeout unit (`#442`_)
- Increase grpc and grpc-tools to 1.33.1 (`#439`_)

Backwards incompatible changes
==============================

- Increase grpc and grpc-tools to 1.33.1 (`#439`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#435`_
      - bug
      - critical
      - When creating new page, library does not obey the `timeout` value. Instead it will timeout in 10seconds. 
    * - `#230`_
      - bug
      - high
      - Wait for response matchers not working
    * - `#442`_
      - bug
      - high
      - Docs for "Wait For Request/Response" have wrong timeout unit
    * - `#439`_
      - enhancement
      - high
      - Increase grpc and grpc-tools to 1.33.1
    * - `#403`_
      - bug
      - medium
      - Improve exception raised by library when trying to click element which can not be clicked.
    * - `#448`_
      - bug
      - medium
      - Remove execution-time-log
    * - `#453`_
      - enhancement
      - medium
      - Add timeout to Go To keyword

Altogether 7 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av1.7.0>`__.

.. _#435: https://github.com/MarketSquare/robotframework-browser/issues/435
.. _#230: https://github.com/MarketSquare/robotframework-browser/issues/230
.. _#442: https://github.com/MarketSquare/robotframework-browser/issues/442
.. _#439: https://github.com/MarketSquare/robotframework-browser/issues/439
.. _#403: https://github.com/MarketSquare/robotframework-browser/issues/403
.. _#448: https://github.com/MarketSquare/robotframework-browser/issues/448
.. _#453: https://github.com/MarketSquare/robotframework-browser/issues/453
