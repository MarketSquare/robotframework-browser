======================
Browser library 16.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 16.1.0 is a new release with
adding link to playwright-log.txt when keyword fails. Also there is bug a fix
to support Robot Framework 6.1b1 release. All issues targeted for Browser
library v16.1.0 can be found from the `issue tracker`_.
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
install it manually. Browser library 16.1.0 was released on Monday May 8, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.33.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v16.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add support for RF 6.1  (`#2785`_)
----------------------------------
Robot Framework enhances automatic conversion of arguments and this caused
at least New Context keyword to fail, when permissions are defined by a user.

Linking playwright-log.txt to log.html (`#1925`_)
-------------------------------------------------
When keyword fails, there might be more information available in the
playwright-log.txt file. But there is not information available, in the
log.html files where that file is. Now there is link to the file,
when keyword fails.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2785`_
      - bug
      - high
      - Add support for RF 6.1 
    * - `#1925`_
      - enhancement
      - high
      - Linking playwright-log.txt to log.html

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av16.1.0>`__.

.. _#2785: https://github.com/MarketSquare/robotframework-browser/issues/2785
.. _#1925: https://github.com/MarketSquare/robotframework-browser/issues/1925
