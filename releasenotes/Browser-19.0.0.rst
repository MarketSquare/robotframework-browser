======================
Browser library 19.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 19.0.0 is a new release with
coverage reporting, trace groups, locator hadnler and clock enhancements and
bug fixes for too large gRPC responces and docker image. All issues targeted
for Browser library v19.0.0 can be found from the `issue tracker`_.
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
install it manually. Browser library 19.0.0 was released on Tuesday November 26, 2024.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.49.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v19.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Support Playwright locator handler  (`#3845`_)
---------------------------------------------
When testing a web page, sometimes unexpected overlays like a "Sign up" dialog appear and block
actions you want to automate, e.g. clicking a button. These overlays don't always show up in the
same way or at the same time, making them tricky to handle in automated tests.

This keywords lets you set up a special list of Playwright API calls, called a handler, that activates
when it detects that overlay is visible. The handler's job is to remove the overlay, allowing your
test to continue as if the overlay wasn't there.

Add support for Playwright Clock (`#3846`_)
------------------------------------------
The Playwright Clock API allows you to control the passage of time in your tests. This can be useful
example simulate sleeping of the comuter and waking up.

Add browser and contex be available in the JS extension side (`#3903`_)
-----------------------------------------------------------------------
This enhancement allows you to access the browser and context objects from the JS extension side.

Received message larger than max (5406604 vs. 4194304) (`#1815`_)
-----------------------------------------------------------------
We now support streaming of large gRPC responses. This is usefull when responces containst large
payload and would exteed the default gRPC message size limit.

Code coverage possibility by using monocart-coverage-reports (`#1502`_)
-----------------------------------------------------------------------
It is nos possile to start and stop front end code coverage and get the coverage report.

Add `timeout` and `waitUntil` to `page.reload` (`#3394`_)
---------------------------------------------------------
The `timeout` and `waitUntil` options are now available for the Reload keyword.

Keyword "Get page source": Add selector for partial source code (`#3460`_)
-------------------------------------------------------------------------
It is now documented how element shource code can be fetched.


Backwards incompatible changes
==============================

Add support Playwright trace groups (`#3908`_)
----------------------------------------------
The trace group feature allows you to see where is test data this playwright API call is coming from.

Also there are other enhancements for creation and cleaning the traces.

Because these other enhancements are not always backwards compatible, we have decided to bump the mjor version.

Acknowledgements
================

Support for new_context clientCertificates (`#3860`_)
-----------------------------------------------------
Many thanks for okraus-ari for making contoribution for adding the clientCertificates argument
to the New Context keyword. Also he made extra effort to our test server can accept client certificates.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3845`_
      - enhancement
      - critical
      - Support Playwright locator handler
    * - `#3846`_
      - enhancement
      - critical
      - Add support for Playwright Clock
    * - `#3903`_
      - enhancement
      - critical
      - Add browser and contex be available in the JS extension side
    * - `#3908`_
      - enhancement
      - critical
      - Add support Playwright trace groups
    * - `#1815`_
      - bug
      - high
      - Received message larger than max (5406604 vs. 4194304)
    * - `#1502`_
      - enhancement
      - high
      - Code coverage possibility by using monocart-coverage-reports
    * - `#3394`_
      - enhancement
      - high
      - Add `timeout` and `waitUntil` to `page.reload`
    * - `#3460`_
      - enhancement
      - high
      - Keyword "Get page source": Add selector for partial source code
    * - `#3860`_
      - enhancement
      - high
      - Support for new_context clientCertificates
    * - `#3843`_
      - bug
      - medium
      - Change of default /usr/local/python3 from python3.8 to python3.12 breaks library imports
    * - `#3301`_
      - enhancement
      - medium
      - Upload Files

Altogether 11 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.0.0>`__.

.. _#3845: https://github.com/MarketSquare/robotframework-browser/issues/3845
.. _#3846: https://github.com/MarketSquare/robotframework-browser/issues/3846
.. _#3903: https://github.com/MarketSquare/robotframework-browser/issues/3903
.. _#3908: https://github.com/MarketSquare/robotframework-browser/issues/3908
.. _#1815: https://github.com/MarketSquare/robotframework-browser/issues/1815
.. _#1502: https://github.com/MarketSquare/robotframework-browser/issues/1502
.. _#3394: https://github.com/MarketSquare/robotframework-browser/issues/3394
.. _#3460: https://github.com/MarketSquare/robotframework-browser/issues/3460
.. _#3860: https://github.com/MarketSquare/robotframework-browser/issues/3860
.. _#3843: https://github.com/MarketSquare/robotframework-browser/issues/3843
.. _#3301: https://github.com/MarketSquare/robotframework-browser/issues/3301
