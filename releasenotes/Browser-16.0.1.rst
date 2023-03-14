======================
Browser library 16.0.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 16.0.1 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v16.0.1 can be found
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
install it manually. Browser library 16.0.1 was released on Tuesday March 14, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.31.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v16.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Bugfixes for `Promise To` keyword
---------------------------------

`Promise To`_ keyword had two issues, (`#2649`_) and (`#2650`_).
The first one was related to type conversion, because it had just some converters hard coded.
Therefore you could for example not use 'Click' with button argument or any timedelta argument.
This is fixed.

Also it had issues with Keywords not matching snake_case notation.
This mostly happens with JS Extension keywords, because they often are camelCase.
These keywords or keywords that were really not part of Browser lib were causing a deadlock.

Docker Image improvements
-------------------------

Docker image is now based on playwrights docker image.
This should solve some issues with this image having missing dependencies.
It also should improve compatibility with ARM architecture.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2649`_
      - bug
      - critical
      - Type Conversion does not work with `Promise To`_ keyword
    * - `#2650`_
      - bug
      - high
      - It seems `Promise To`_ does not work with JS Extension keywords.
    * - `#1756`_
      - ---
      - ---
      - Make our 3 dockerfile setup simpler

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av16.0.1>`__.

.. _#2649: https://github.com/MarketSquare/robotframework-browser/issues/2649
.. _#2650: https://github.com/MarketSquare/robotframework-browser/issues/2650
.. _#1756: https://github.com/MarketSquare/robotframework-browser/issues/1756
.. _Promise To: https://marketsquare.github.io/robotframework-browser/Browser.html#Promise%20To
