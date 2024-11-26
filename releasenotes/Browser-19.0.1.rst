======================
Browser library 19.0.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.0.1 is a new hotfix
release with fixes to rfbrowser coverage command line and Wait For
Response keyword. All issues targeted for Browser library v19.0.1 can
be found from the `issue tracker`_. For first time installation with
pip_, just run
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
install it manually. Browser library 19.0.1 was released on Tuesday November 26, 2024.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.49.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Wait for response keyword fails when it get a list (`#3912`_)
-------------------------------------------------------------
If response body was a list like object, then parsing the body failed.
THis regression when gRPC buffer owerflowed was fixed.

rfbrowser coverage combine does not work if Start Coverage uses folder argument (`#3911`_)
--------------------------------------------------------------------------------------------
If Start Coverage was used with folder argument, then combining the coverage
did not wokr. Also fixed the outputPath argument to resolve correcly when
using relative paths.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3912`_
      - bug
      - critical
      - Wait for response keyword fails when it get a list
    * - `#3911`_
      - bug
      - high
      - rfbrowser coverage combine does not work if Start Coverage uses folder argument

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.0.1>`__.

.. _#3912: https://github.com/MarketSquare/robotframework-browser/issues/3912
.. _#3911: https://github.com/MarketSquare/robotframework-browser/issues/3911
