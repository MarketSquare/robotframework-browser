======================
Browser library 16.0.2
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 16.0.2 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v16.0.2 can be found
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
install it manually. Browser library 16.0.2 was released on Wednesday March 15, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.31.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v16.0.2


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
    * - `#2701`_
      - ---
      - ---
      - Docker image is not pushing other than latest tags correctly

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av16.0.2>`__.

.. _#2701: https://github.com/MarketSquare/robotframework-browser/issues/2701
