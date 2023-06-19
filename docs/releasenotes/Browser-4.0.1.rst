=====================
Browser library 4.0.1
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 4.0.1 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v4.0.1 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==4.0.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 4.0.1 was released on Thursday March 25, 2021. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av4.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- [Get Selected Options] keyword returns error "Error: page.$$eval: Evaluation failed: DOMException: Failed to execute 'evaluate' on 'Document': The string './/select[@name='brandCategory'] option' is not a valid XPath expression." (`#757`_)

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
    * - `#732`_
      - bug
      - medium
      - Add SeleniumLibrary Set Screenshot Directory keyword counterpart

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av4.0.1>`__.

.. _#757: https://github.com/MarketSquare/robotframework-browser/issues/757
.. _#732: https://github.com/MarketSquare/robotframework-browser/issues/732
