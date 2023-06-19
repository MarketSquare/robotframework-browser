======================
Browser library 16.0.4
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 16.0.4 is a new release with
bug fixes to rfbroser init. All issues targeted for Browser library v16.0.4
can be found from the `issue tracker`_.
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
install it manually. Browser library 16.0.4 was released on Sunday April 30, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.33.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v16.0.4


.. contents::
   :depth: 2
   :local:

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2727`_
      - bug
      - medium
      - Teamcity build fails during installation rfbrowser node dependencies with UnicodeEncodeError

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av16.0.4>`__.

.. _#2727: https://github.com/MarketSquare/robotframework-browser/issues/2727
