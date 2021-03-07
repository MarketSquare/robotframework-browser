=====================
Browser library 3.3.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 3.3.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v3.3.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==3.3.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 3.3.0 was released on Sunday March 7, 2021. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av3.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- [Get Selected Options] keyword returns error "Error: page.$$eval: Evaluation failed: DOMException: Failed to execute 'evaluate' on 'Document': The string './/select[@name='brandCategory'] option' is not a valid XPath expression." (`#757`_)
- Clean files created by Browser library at start of the test execution (`#477`_)
- Auto closing and closing should log more explicitly (`#664`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#757`_
      - bug
      - high
      - [Get Selected Options] keyword returns error "Error: page.$$eval: Evaluation failed: DOMException: Failed to execute 'evaluate' on 'Document': The string './/select[@name='brandCategory'] option' is not a valid XPath expression."
    * - `#477`_
      - enhancement
      - high
      - Clean files created by Browser library at start of the test execution
    * - `#664`_
      - enhancement
      - high
      - Auto closing and closing should log more explicitly
    * - `#403`_
      - bug
      - medium
      - Improve exception raised by library when trying to click element which can not be clicked.
    * - `#391`_
      - enhancement
      - medium
      - Set Browser Timeout should be ok to call even when no browser is open.

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av3.3.0>`__.

.. _#757: https://github.com/MarketSquare/robotframework-browser/issues/757
.. _#477: https://github.com/MarketSquare/robotframework-browser/issues/477
.. _#664: https://github.com/MarketSquare/robotframework-browser/issues/664
.. _#403: https://github.com/MarketSquare/robotframework-browser/issues/403
.. _#391: https://github.com/MarketSquare/robotframework-browser/issues/391
