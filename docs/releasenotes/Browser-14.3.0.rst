======================
Browser library 14.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 14.3.0 is a new release with
enhancements for the Wait For Condition keyword.
All issues targeted for Browser library v14.3.0 can be found
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
install it manually. Browser library 14.3.0 was released on Sunday December 4, 2022. 
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.27.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av14.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

"Wait for Condition" not working if Selenium Lib is installed (`#2373`_)
------------------------------------------------------------------------
Wait For Condition did work correctly if there was two or more keywords with
same mane. Wait For Condition will only use keywords coming from the Browser
library. 

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2373`_
      - bug
      - high
      - "Wait for Condition" not working if Selenium Lib is installed

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av14.3.0>`__.

.. _#2373: https://github.com/MarketSquare/robotframework-browser/issues/2373
