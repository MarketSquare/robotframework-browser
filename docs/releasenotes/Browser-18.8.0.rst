======================
Browser library 18.8.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.8.0 is a new release with
enhancement to Playwright browser binary installation and better support for
localisation. Also noWaitAfter argument is deprecated by Playwright.
All issues targeted for Browser library v18.8.0 can be found
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
install it manually. Browser library 18.8.0 was released on Sunday August 18, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.46.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.8.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
When loading translations support loading more than one translation from found Python plugins (`#3742`_)
----------------------------------------------------------------------------------------------------------------
When loading translations support loading more than one translation from found Python plugin.
Now one project or Python plugin can provide multiple translations.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3742`_
      - enhancement
      - critical
      - When loading translations support loading more than one translation from found Python plugins
    * - `#3740`_
      - bug
      - medium
      - Tab and Click With Options keyword noWaitAfter argument is deprecated by Playwright
    * - `#3547`_
      - enhancement
      - medium
      - Add more browser types when run Browser.entry script for browser installation

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.8.0>`__.

.. _#3742: https://github.com/MarketSquare/robotframework-browser/issues/3742
.. _#3740: https://github.com/MarketSquare/robotframework-browser/issues/3740
.. _#3547: https://github.com/MarketSquare/robotframework-browser/issues/3547
