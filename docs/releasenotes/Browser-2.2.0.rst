=====================
Browser library 2.2.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 2.2.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v2.2.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==2.2.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 2.2.0 was released on Thursday November 19, 2020. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av2.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Truncate exceptions over grpc (`#468`_)
---------------------------------------
If long error messages where generated in the node side
it could lead to overflow in the grpc side and 
hide the original error from the users. This is now
fixed and error messages are now trunkated to 5 000
characters.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#468`_
      - bug
      - high
      - Truncate exceptions over grpc
    * - `#492`_
      - enhancement
      - medium
      - Improve assertion engine errors message and documentation to help users to understand about different types
    * - `#509`_
      - ---
      - ---
      - Improved system browser workflow
    * - `#511`_
      - ---
      - ---
      - Bump to playwright 1.6.2
    * - `#512`_
      - ---
      - ---
      - `#510`_ with github-actions node-path setting completely removed

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av2.2.0>`__.

.. _#468: https://github.com/MarketSquare/robotframework-browser/issues/468
.. _#492: https://github.com/MarketSquare/robotframework-browser/issues/492
.. _#509: https://github.com/MarketSquare/robotframework-browser/issues/509
.. _#511: https://github.com/MarketSquare/robotframework-browser/issues/511
.. _#512: https://github.com/MarketSquare/robotframework-browser/issues/512
