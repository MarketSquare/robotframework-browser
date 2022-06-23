======================
Browser library 13.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 13.1.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v13.1.0 can be found
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
install it manually. Browser library 13.1.0 was released on Friday June 3, 2022. 
Browser supports Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.22.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av13.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- Click Argument 'modifiers' Documentation doesn't work as expected (`#2049`_)
- Get Table Cell Element raises StrictModeException (`#2076`_)
- Select Option By causes super long time due to iteration over all options. (`#2077`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2049`_
      - bug
      - high
      - Click Argument 'modifiers' Documentation doesn't work as expected
    * - `#2076`_
      - bug
      - high
      - Get Table Cell Element raises StrictModeException
    * - `#2077`_
      - bug
      - high
      - Select Option By causes super long time due to iteration over all options.

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av13.1.0>`__.

.. _#2049: https://github.com/MarketSquare/robotframework-browser/issues/2049
.. _#2076: https://github.com/MarketSquare/robotframework-browser/issues/2076
.. _#2077: https://github.com/MarketSquare/robotframework-browser/issues/2077
