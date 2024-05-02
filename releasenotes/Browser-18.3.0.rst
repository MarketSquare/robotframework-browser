======================
Browser library 18.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.3.0 is a new release with
support for translation keywords and documentation. Also we provide support
for translating deprecated keyword to new format with help of RoboTidy.
All issues targeted for Browser library v18.3.0 can be found
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
install it manually. Browser library 18.3.0 was released on Tuesday April 2, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.42.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Use tidy to fix deprecated keyword: Wait Until Network Is Idle to Wait For Load State (`#3437`_)
------------------------------------------------------------------------------------------------
`rfbrowser transform` commands helps user to transfors deprecated keywords to new format.
Currently we support transforming `Wait Until Network Is Idle` to `Wait For Load State`. But
it might be possible in future to extend support for other deprecated keywords.

Support translation for keyword and documentation. (`#3497`_)
-------------------------------------------------------------
With help of `PythonLibCore`_ library now support translating keywords names and documentation to other
langueges than English. Translation to other langueges needs support for community by creating Python
packages, exampe project is created `Finnish`_

Xray compatibility: Add robot-seleniumlibrary-screenshot class to render embedded images (`#3487`_)
---------------------------------------------------------------------------------------------------
When embedding screenhot to log.html file, class="robot-seleniumlibrary-screenshot" attribute is added
to the <img> tag. This adds supports for XRay.

Acknowledgements
================

Typo in README uninstall  (`#3465`_)
------------------------------------
Many thanks to thulasiraju for fixing typo in README file.

Improve logging done by Click and Select Options By keyword  (`#3510`_)
-----------------------------------------------------------------------
Many thanks to lennartq for improving logging in Click and Select Options By keyword keywords.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3437`_
      - enhancement
      - high
      - Use tidy to fix deprecated keyword: Wait Until Network Is Idle to Wait For Load State
    * - `#3487`_
      - enhancement
      - high
      - [Xray compatibility] Add robot-seleniumlibrary-screenshot class to render embedded images
    * - `#3497`_
      - enhancement
      - high
      - Support translation for keyword and documentation.
    * - `#3465`_
      - bug
      - medium
      - Typo in README uninstall
    * - `#3510`_
      - bug
      - medium
      - Improve logging done by Click and Select Options By keyword

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.3.0>`__.

.. _#3437: https://github.com/MarketSquare/robotframework-browser/issues/3437
.. _#3487: https://github.com/MarketSquare/robotframework-browser/issues/3487
.. _#3497: https://github.com/MarketSquare/robotframework-browser/issues/3497
.. _#3465: https://github.com/MarketSquare/robotframework-browser/issues/3465
.. _#3510: https://github.com/MarketSquare/robotframework-browser/issues/3510
.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Finnish: https://github.com/MarketSquare/robotframework-browser-translation-fi
