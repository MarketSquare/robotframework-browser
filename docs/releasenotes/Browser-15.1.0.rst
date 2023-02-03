======================
Browser library 15.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 15.1.0 is a new release with
new Mouse Wheel keyword and allowing providing parameters to the node process. 
Also there is bug fixes when installing the librqry with rfbrowser init command.
All issues targeted for Browser library v15.1.0 can be found
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
install it manually. Browser library 15.1.0 was released on Wednesday January 18, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.29.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v15.1.0


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
    * - `#2519`_
      - bug
      - medium
      - Can't write rfbrowser.log to Browser lib installation directory
    * - `#2347`_
      - enhancement
      - medium
      - new keyword provide for playwright mouse wheel
    * - `#2544`_
      - enhancement
      - medium
      - Enhance install log file to preserve for longer time, example use Python RotatingFileHandler
    * - `#2545`_
      - enhancement
      - medium
      - Enhance rfbrowser command to show library and Playwright version numbers
    * - `#2568`_
      - enhancement
      - medium
      - [Enhancement] Add the possiblity enable debugging for the node process

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av15.1.0>`__.

.. _#2519: https://github.com/MarketSquare/robotframework-browser/issues/2519
.. _#2347: https://github.com/MarketSquare/robotframework-browser/issues/2347
.. _#2544: https://github.com/MarketSquare/robotframework-browser/issues/2544
.. _#2545: https://github.com/MarketSquare/robotframework-browser/issues/2545
.. _#2568: https://github.com/MarketSquare/robotframework-browser/issues/2568
