======================
Browser library 17.5.2
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 17.5.2 is comes with new
version of grpcio to support Python 3.12. All issues targeted for Browser
library v17.5.2 can be found from the `issue tracker`_.
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
install it manually. Browser library 17.5.2 was released on Friday October 13, 2023.
Browser supports Python 3.8+, Node 16/18 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.39.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v17.5.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Installation Failure of robotframework-browser in Python 3.12 Due to grpcio Dependencies (`#3138`_)
---------------------------------------------------------------------------------------------------
grpcio is updated to support Python 3.12.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3138`_
      - bug
      - critical
      - Installation Failure of robotframework-browser in Python 3.12 Due to grpcio Dependencies

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av17.5.2>`__.

.. _#3138: https://github.com/MarketSquare/robotframework-browser/issues/3138
