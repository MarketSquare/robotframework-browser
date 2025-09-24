======================
Browser library 19.8.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.8.0 is a new release with
New Keyword to merge coverage reports to a single one. The other main reason
for this release is to update Playwright to the 1.55.1 version and to fix
Chromium CVE-2025-10585. We also declare support for NodeJS 24 LTS. There are
also fixes to NodeJS side Pino logger to have on instance and shorter the
folder listing when there is error in rfbrowser init. Also in some cases
rfbrowser --version displayed Playwright version wrong.  All issues targeted
for Browser library v19.8.0 can be found from the `issue tracker`_.
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
install it manually. Browser library 19.8.0 was released on Wednesday September 24, 2025.
Browser supports Python 3.9+, Node 20/22/24 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.55.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.8.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

update Playwright to the 1.55.1
-------------------------------
Update Playwright to the 1.55.1 to fix Chromium CVE-2025-10585. Users are urged
to update their Browser library installations to 19.8.0 version.

When there is error in rfbrowser init folder listing is too long (`#4367`_)
---------------------------------------------------------------------------
When there is error in rfbrowser init folder listing of node_modules is
too long. We still list folder but we filter and display only the important
ones.

New keyword for merging coverage reports to a single one (`#4002`_)
-------------------------------------------------------------------
New keyword Merge Coverage Reports to merge multiple coverage reports
into a single one. This is useful when several contexts are opened and
each parallel contexts generates its own coverage report.

Declare support for NodeJS 24 LTS (`#4402`_)
--------------------------------------------
We now declare support for NodeJS 24 LTS. Browser library has been
tested to work with NodeJS 20, 22 and 24 LTS.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4367`_
      - bug
      - high
      - When there is error in rfbrowser init folder listing is too long
    * - `#4002`_
      - enhancement
      - high
      - New keyword for merging coverage reports to a single one
    * - `#4402`_
      - enhancement
      - high
      - Declare support for NodeJS 24 LTS
    * - `#4410`_
      - bug
      - medium
      - PLaywright version is displayed wrong in rfbrowser --version command
    * - `#4373`_
      - bug
      - low
      - Improve NodeJS pino logger to only have one instance

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.8.0>`__.

.. _#4367: https://github.com/MarketSquare/robotframework-browser/issues/4367
.. _#4002: https://github.com/MarketSquare/robotframework-browser/issues/4002
.. _#4402: https://github.com/MarketSquare/robotframework-browser/issues/4402
.. _#4410: https://github.com/MarketSquare/robotframework-browser/issues/4410
.. _#4373: https://github.com/MarketSquare/robotframework-browser/issues/4373
