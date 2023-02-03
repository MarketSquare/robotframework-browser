======================
Browser library 11.4.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 11.4.0 is a new release with
new et Element States keyword enhancements and bug fixes to Type/Fill Secret
keyword. All issues targeted for Browser library v11.4.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==11.4.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 11.4.0 was released on Wednesday February 9, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.18.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av11.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Improve Assertion of Element State. `Get Element States` (`#1592`_)
-------------------------------------------------------------------
Get Elements States allows to assert and return multiple elements states
with one keyword call. The old keyword required one call for each element
state.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1592`_
      - enhancement
      - high
      - Improve Assertion of Element State. `Get Element States`
    * - `#1738`_
      - bug
      - medium
      - Fill Secret keyword fails with `${EMPTY}`

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av11.4.0>`__.

.. _#1592: https://github.com/MarketSquare/robotframework-browser/issues/1592
.. _#1738: https://github.com/MarketSquare/robotframework-browser/issues/1738
