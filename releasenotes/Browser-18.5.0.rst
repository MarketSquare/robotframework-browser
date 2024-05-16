======================
Browser library 18.5.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.5.0 is a new release with
which has Playwright 1.44.0 and bug fix to rfbrowser --version command. Also
there is small refactoring to creating Docker container. All issues targeted
for Browser library v18.5.0 can be found from the `issue tracker`_.
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
install it manually. Browser library 18.5.0 was released on Thursday May 16, 2024.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.44.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.5.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

rfbrowser --version fails with exception from  (`#3600`_)
---------------------------------------------------------
New priting out version does not fail.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3600`_
      - bug
      - critical
      - rfbrowser --version fails with exception from

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.5.0>`__.

.. _#3600: https://github.com/MarketSquare/robotframework-browser/issues/3600
