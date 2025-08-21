======================
Browser library 19.7.2
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.7.2 is a new hotfix
release with bugfix to Docker container. All issues targeted for Browser
library v19.7.2 can be found from the `issue tracker`_.
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
install it manually. Browser library 19.7.2 was released on Thursday August 21, 2025.
Browser supports Python 3.9+, Node 20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.55.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.7.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Update Docker to use PW 1.55.0 (`#4357`_)
-------------------------------------------

We did forget to update the Docker container to use Playwright 1.55.0 in the previous release.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#4357`_
      - bug
      - critical
      - Update Docker to use PW 1.55.0

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.7.2>`__.

.. _#4357: https://github.com/MarketSquare/robotframework-browser/issues/4357
