======================
Browser library 19.5.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.5.0 is a new release with
enhances failure diagnostics by higjhlighting the selector that caused a failure.
There is fix for Robot Framework 5 support and several fixes to documentation.
Also we tired to silence the log.html by removing some of the noise from the
listener API method logging. Lastly there is a fix for rfbrowser --version
command in Windows OS:  All issues targeted for Browser library v19.5.0 can
be found from the `issue tracker`_.
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
install it manually. Browser library 19.5.0 was released on Saturday May 3, 2025.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.52.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.5.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Browser library listener API method logging makes log.html too noisy (`#4053`_)
--------------------------------------------------------------------------------
With Robot Framework 7 listener API changes, logging of listener API is
visible in the log.html. This makes the log.html too noisy and logging
is now silenced.

Highlight the selector that caused a failure (`#4196`_)
-------------------------------------------------------
If keyword fails and if there is valid selector then we highlight the
element that caused the failure. This helps to understand the failure
better.

Acknowledgements
================

rfbrowser --version function won't work on Windows: FileNotFoundError: [WinError 2]  -error (`#4158`_)
------------------------------------------------------------------------------------------------------
Many thanks for Lukas Boekenoogen for fixing the issue with rfbrowser
--version command in Windows OS.

Fix RF 5 support (`#4193`_)
---------------------------
Many thanks for Samuel Montgomery-Blinn for fixing the issue with Robot
Framework 5 support. Browser library acts as a listener and with Robot
Framework 5 the listener API does not always return path to the current
test data file.

Fix typos in the documentation (`#4131`_)
-----------------------------------------
Many thanks for Lukas Boekenoogen for fixing many typos in the library
keyword documentation.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4053`_
      - bug
      - critical
      - Browser library listener API method logging makes log.html too noisy
    * - `#4158`_
      - bug
      - high
      - rfbrowser --version function won't work on Windows: FileNotFoundError: [WinError 2]  -error
    * - `#4189`_
      - bug
      - high
      - Fix slowMo argument documentation
    * - `#4193`_
      - bug
      - high
      - Fix RF 5 support
    * - `#4196`_
      - enhancement
      - high
      - Highlight the selector that caused a failure
    * - `#4131`_
      - bug
      - medium
      - Fix typos in the documentation
    * - `#4157`_
      - bug
      - medium
      - Wrong return type in documentation for `Get Console Log` keyword
    * - `#4122`_
      - bug
      - low
      - Dependency updates
    * - `#4178`_
      - bug
      - low
      - Fix Wait For Alert example in docs

Altogether 9 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.5.0>`__.

.. _#4053: https://github.com/MarketSquare/robotframework-browser/issues/4053
.. _#4158: https://github.com/MarketSquare/robotframework-browser/issues/4158
.. _#4189: https://github.com/MarketSquare/robotframework-browser/issues/4189
.. _#4193: https://github.com/MarketSquare/robotframework-browser/issues/4193
.. _#4196: https://github.com/MarketSquare/robotframework-browser/issues/4196
.. _#4131: https://github.com/MarketSquare/robotframework-browser/issues/4131
.. _#4157: https://github.com/MarketSquare/robotframework-browser/issues/4157
.. _#4122: https://github.com/MarketSquare/robotframework-browser/issues/4122
.. _#4178: https://github.com/MarketSquare/robotframework-browser/issues/4178
