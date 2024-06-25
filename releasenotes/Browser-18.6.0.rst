======================
Browser library 18.6.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.6.0 is a new release with
update docker image to latest from Playwright and fixing on logging when
installation is done in Windows OS. All issues targeted for Browser
library v18.6.0 can be found from the `issue tracker`_.
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
install it manually. Browser library 18.6.0 was released on Friday June 21, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.44.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.6.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Bump up browser docker base image (`#3625`_)
--------------------------------------------
Docker had been build with older version of base image from Playwright,
image has been updated to playwright:v1.44.1-focal and it should have
never NodeJs installed.

rfbrowser init in windows shows errors when logging node output. (`#3633`_)
---------------------------------------------------------------------------
In older Windows rfbrowser init could display lot if error information
which is related logging in console. Now all windows output is cleaned
from anything alse expect plain ascii charaters.

Documentation for New Context keyword and baseURL argument does not mention  Wait For Navigation (`#3636`_)
-----------------------------------------------------------------------------------------------------------
Keyword documentation was laccking essential information, this is now fixed.

Many thanks to Jani Mikkonen for providing the fix.

Acknowledgements
================

Fix typo in translation section  (`#3611`_)
-------------------------------------------
Type has been fixed in documentation, many thanks to Jani Mikkonen for providing the fix.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3625`_
      - bug
      - critical
      - Bump up browser docker base image
    * - `#3633`_
      - bug
      - high
      - rfbrowser init in windows shows errors when logging node output.
    * - `#3636`_
      - bug
      - high
      - Documentation for New Context keyword and baseURL argument does not mention  Wait For Navigation
    * - `#3611`_
      - bug
      - medium
      - Fix typo in translation section

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.6.0>`__.

.. _#3625: https://github.com/MarketSquare/robotframework-browser/issues/3625
.. _#3633: https://github.com/MarketSquare/robotframework-browser/issues/3633
.. _#3636: https://github.com/MarketSquare/robotframework-browser/issues/3636
.. _#3611: https://github.com/MarketSquare/robotframework-browser/issues/3611
