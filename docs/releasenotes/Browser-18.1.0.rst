======================
Browser library 18.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.1.0 is a new release with
enhancements and bug fixes. All issues targeted for Browser library v18.1.0
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
install it manually. Browser library 18.1.0 was released on Wednesday February 7, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.41.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
"Wait Until Network Is Idle" failure message shows inapropriate "tip"  (`#3333`_)
---------------------------------------------------------------------------------
We did show incorrect help in the failure of some keywords, about increasing 
the timeout. Now this is fixed.

Wrong example in `Add Cookie` (`#3387`_)
----------------------------------------
Cookie expire did not workcorrectly, this is now fixed.


Acknowledgements
================

Cannot launch browser server with Additional arguements from terminal or cmd. (`#3363`_)
----------------------------------------------------------------------------------------
Many thanks for gitkatsi for fixing the problem with bug on parsing parameters for
chromiumn. 


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3333`_
      - bug
      - high
      - "Wait Until Network Is Idle" failure message shows inapropriate "tip" 
    * - `#3387`_
      - enhancement
      - high
      - Wrong example in `Add Cookie`
    * - `#3280`_
      - bug
      - medium
      - Video from Browserstack
    * - `#3334`_
      - bug
      - medium
      - Documentation: "Click" does not have "noWaitAfter" option
    * - `#3363`_
      - bug
      - medium
      - Cannot launch browser server with Additional arguements from terminal or cmd.
    * - `#3395`_
      - bug
      - medium
      - Remove verbose Catalog logging from Get Browser Catalog 
    * - `#3308`_
      - bug
      - low
      - New Context docs improvement

Altogether 7 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.1.0>`__.

.. _#3333: https://github.com/MarketSquare/robotframework-browser/issues/3333
.. _#3387: https://github.com/MarketSquare/robotframework-browser/issues/3387
.. _#3280: https://github.com/MarketSquare/robotframework-browser/issues/3280
.. _#3334: https://github.com/MarketSquare/robotframework-browser/issues/3334
.. _#3363: https://github.com/MarketSquare/robotframework-browser/issues/3363
.. _#3395: https://github.com/MarketSquare/robotframework-browser/issues/3395
.. _#3308: https://github.com/MarketSquare/robotframework-browser/issues/3308
