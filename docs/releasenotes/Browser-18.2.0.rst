======================
Browser library 18.2.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.2.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v18.2.0 can be found
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
install it manually. Browser library 18.2.0 was released on Friday February 16, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.41.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Support starting and stopping trace by a keyword (`#3427`_)
- New Keyword: Wait for Load State (`#3327`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3427`_
      - enhancement
      - critical
      - Support starting and stopping trace by a keyword
    * - `#3327`_
      - enhancement
      - high
      - New Keyword: Wait for Load State
    * - `#3436`_
      - bug
      - high
      - `Promise To Wait For Download` does not work with connected "Remote Browser"

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.2.0>`__.

.. _#3427: https://github.com/MarketSquare/robotframework-browser/issues/3427
.. _#3327: https://github.com/MarketSquare/robotframework-browser/issues/3327
.. _#3436: https://github.com/MarketSquare/robotframework-browser/issues/3436
