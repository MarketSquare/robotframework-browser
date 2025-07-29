======================
Browser library 19.7.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.7.0 is a new release with
enhancement to datetime.datetime in Add Cookie. Also we dropped support for
Node 18 and small enhancements where made on NodeJS side logging. Internally
project now uses pyproject.toml instead of setup.py for package metadata.
All issues targeted for Browser library v19.7.0 can be found
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
install it manually. Browser library 19.7.0 was released on Tuesday July 29, 2025.
Browser supports Python 3.9+, Node 20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.54.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.7.0


.. contents::
   :depth: 2
   :local:

Backwards incompatible changes
==============================

Drop node 18 support (`#4267`_)
===============================
Node 18 is no longer supported by Playwright and Browser library. If you
are using Node 18, you need to upgrade to Node 20 or 22 LTS.
This change is made to keep the library up to date with NodeJS support and
making sure that in future we can make nesasary changes to the library.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4267`_
      - enhancement
      - critical
      - Drop node 18 support
    * - `#4257`_
      - enhancement
      - medium
      - Support `datetime.datetime` in `Add Cookie` argument `expires`

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.7.0>`__.

.. _#4267: https://github.com/MarketSquare/robotframework-browser/issues/4267
.. _#4257: https://github.com/MarketSquare/robotframework-browser/issues/4257
