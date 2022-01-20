======================
Browser library 10.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 10.1.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v10.1.0 can be found
from the `issue tracker`_.

For installation see `update instructions`_.

Browser library 10.1.0 was released on Friday November 26, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.16.3

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av10.1.0
.. _update instructions https://robotframework-browser.org/#Update


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
Upload File By Selector keyword (`#1499`_)
------------------------------------------
There is new keyword to upload files.

Unable to pass "Predicate" argument to ``wait for`` keywords (`#1486`_)
- Chromium: Check Checkbox KW fails sometimes with Element is not attached to the DOM (`#1492`_)
- Release process saves wrong version from old KW docs (`#1494`_)
- Improve playwright trace log reading (`#1448`_)

Acknowledgements
================

Thanks to external contributors for these improvements!

- Unable to pass "Predicate" argument to ``wait for`` keywords (`#1486`_)
- Fix typo when logging strict mode in node side. (`#1490`_)
- Fix atest running in windows (`#1546`_)
- Issue with `Wait For Response` (`#872`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1486`_
      - bug
      - high
      - Unable to pass "Predicate" argument to ``wait for`` keywords
    * - `#1492`_
      - bug
      - high
      - Chromium: Check Checkbox KW fails sometimes with Element is not attached to the DOM
    * - `#1494`_
      - bug
      - high
      - Release process saves wrong version from old KW docs
    * - `#1448`_
      - enhancement
      - high
      - Inprove playwright trace log reading
    * - `#1545`_
      - enhancement
      - high
      - Implement file upload by Playwright setInputFiles API method
    * - `#1490`_
      - bug
      - medium
      - Fix typo when logging strict mode in node side.
    * - `#1546`_
      - bug
      - medium
      - Fix atest running in windows
    * - `#872`_
      - enhancement
      - medium
      - Issue with `Wait For Response`
    * - `#1485`_
      - ---
      - ---
      - Keyword "Wait For Elements State" is not working
    * - `#1493`_
      - ---
      - ---
      - Tune wait for http redirect to avoid random failures
    * - `#1499`_
      - ---
      - ---
      - Upload File By Selector keyword
    * - `#1510`_
      - ---
      - ---
      - Generate old keyword docs from correct tag
    * - `#1519`_
      - ---
      - ---
      - Support for _react= selector strategy
    * - `#1526`_
      - ---
      - ---
      - Unable to launch webkit on Mac M1
    * - `#1530`_
      - ---
      - ---
      - Py310 support for utest
    * - `#1533`_
      - ---
      - ---
      - Fix wait for regex and predicate handling
    * - `#1534`_
      - ---
      - ---
      - Simpler non-promise based way of uploading files
    * - `#1538`_
      - ---
      - ---
      - docs: add rsandbach as a contributor for bug
    * - `#1539`_
      - ---
      - ---
      - docs: add rsandbach as a contributor for code
    * - `#1543`_
      - ---
      - ---
      - Rfbrowser init issues
    * - `#1544`_
      - ---
      - ---
      - Log when keywords calls method from node side
    * - `#1549`_
      - ---
      - ---
      - Linting and update docs for network
    * - `#1550`_
      - ---
      - ---
      - update dead link
    * - `#1551`_
      - ---
      - ---
      - Run `inv lint-python` in CI instead of custom mypy command

Altogether 30 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av10.1.0>`__.

.. _#1486: https://github.com/MarketSquare/robotframework-browser/issues/1486
.. _#1492: https://github.com/MarketSquare/robotframework-browser/issues/1492
.. _#1494: https://github.com/MarketSquare/robotframework-browser/issues/1494
.. _#1448: https://github.com/MarketSquare/robotframework-browser/issues/1448
.. _#1545: https://github.com/MarketSquare/robotframework-browser/issues/1545
.. _#1490: https://github.com/MarketSquare/robotframework-browser/issues/1490
.. _#1546: https://github.com/MarketSquare/robotframework-browser/issues/1546
.. _#872: https://github.com/MarketSquare/robotframework-browser/issues/872
.. _#1485: https://github.com/MarketSquare/robotframework-browser/issues/1485
.. _#1493: https://github.com/MarketSquare/robotframework-browser/issues/1493
.. _#1499: https://github.com/MarketSquare/robotframework-browser/issues/1499
.. _#1510: https://github.com/MarketSquare/robotframework-browser/issues/1510
.. _#1511: https://github.com/MarketSquare/robotframework-browser/issues/1511
.. _#1513: https://github.com/MarketSquare/robotframework-browser/issues/1513
.. _#1519: https://github.com/MarketSquare/robotframework-browser/issues/1519
.. _#1526: https://github.com/MarketSquare/robotframework-browser/issues/1526
.. _#1528: https://github.com/MarketSquare/robotframework-browser/issues/1528
.. _#1530: https://github.com/MarketSquare/robotframework-browser/issues/1530
.. _#1531: https://github.com/MarketSquare/robotframework-browser/issues/1531
.. _#1533: https://github.com/MarketSquare/robotframework-browser/issues/1533
.. _#1534: https://github.com/MarketSquare/robotframework-browser/issues/1534
.. _#1535: https://github.com/MarketSquare/robotframework-browser/issues/1535
.. _#1537: https://github.com/MarketSquare/robotframework-browser/issues/1537
.. _#1538: https://github.com/MarketSquare/robotframework-browser/issues/1538
.. _#1539: https://github.com/MarketSquare/robotframework-browser/issues/1539
.. _#1543: https://github.com/MarketSquare/robotframework-browser/issues/1543
.. _#1544: https://github.com/MarketSquare/robotframework-browser/issues/1544
.. _#1549: https://github.com/MarketSquare/robotframework-browser/issues/1549
.. _#1550: https://github.com/MarketSquare/robotframework-browser/issues/1550
.. _#1551: https://github.com/MarketSquare/robotframework-browser/issues/1551
