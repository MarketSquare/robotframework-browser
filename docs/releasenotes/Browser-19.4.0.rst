======================
Browser library 19.4.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.4.0 is a new release
with enhancements to keyboard modifier ControlOrMeta, rfbrowser —version
returns the installed Playwright version and now library follows PEP597.
All issues targeted for Browser library v19.4.0 can be found
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
install it manually. Browser library 19.4.0 was released on Sunday March 16, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.51.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.4.0


.. contents::
   :depth: 2
   :local:

Acknowledgements
================

Follow PEP597 (`#4115`_)
------------------------
Many thanks for Jani Mikkonen for making library to follow PEP597. Also Jani provided
few lint and performance fixes to the library.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4076`_
      - bug
      - medium
      - Drop support for providing translation as dictionary
    * - `#4115`_
      - bug
      - medium
      - Follow PEP597
    * - `#3968`_
      - enhancement
      - medium
      - Add new keyboard modifier key: ControlOrMeta
    * - `#4052`_
      - enhancement
      - medium
      - Updated rfbrowser —version to return installed Playwright version

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.4.0>`__.

.. _#4076: https://github.com/MarketSquare/robotframework-browser/issues/4076
.. _#4115: https://github.com/MarketSquare/robotframework-browser/issues/4115
.. _#3968: https://github.com/MarketSquare/robotframework-browser/issues/3968
.. _#4052: https://github.com/MarketSquare/robotframework-browser/issues/4052
