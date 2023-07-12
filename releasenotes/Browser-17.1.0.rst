======================
Browser library 17.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 17.1.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v17.1.0 can be found
from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and
install it manually. Browser library 17.1.0 was released on Wednesday July 12, 2023.
Browser supports Python 3.8+, Node 16/18 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.36.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v17.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- Keyword Docs are missing Forum Comment entries for new keywords in 17.0.0 (`#2945`_)
- Tap keyword was accidentally named Tab  (`#2948`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2945`_
      - bug
      - critical
      - Keyword Docs are missing Forum Comment entries for new keywords in 17.0.0
    * - `#2948`_
      - bug
      - critical
      - Tap keyword was accidentally named Tab 

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av17.1.0>`__.

.. _#2945: https://github.com/MarketSquare/robotframework-browser/issues/2945
.. _#2948: https://github.com/MarketSquare/robotframework-browser/issues/2948
