=====================
Browser library 1.6.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 1.6.0 is a new release with
deprecation of Click With Options and added new Set Geolocation keyword.
All issues targeted for Browser library v1.6.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==1.6.0
   rfbrowser init

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 1.6.0 was released on Tuesday October 20, 2020. Browser supports
Python Python 3.7+ , Playwright 1.5.1 and Robot Framework 3.2.2.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av1.6.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Errors in end_test and end_suite caused by auto closing (`#380`_)
-----------------------------------------------------------------
There is still possibility of errors, but errors should not anymore
cause problems in the test execution flow.

Wait for request and response matchers (regexp at least) do not seem to work (`#230`_)
--------------------------------------------------------------------------------------
Matchers should work better.

Update geolocation keyword (`#226`_)
------------------------------------
Now it is possible to set geolocation also with Set Geolocation keyword.

Deprecated features
===================

Replace Click with Click With Options (`#424`_)
-----------------------------------------------
Features of Click With Options are merged to Click keyword
and Click With Options will be removed in next major release.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#380`_
      - bug
      - critical
      - Errors in end_test and end_suite caused by auto closing
    * - `#230`_
      - bug
      - high
      - Wait for request and response matchers (regexp at least) do not seem to work
    * - `#226`_
      - enhancement
      - high
      - Update geolocation keyword
    * - `#424`_
      - enhancement
      - high
      - Replace Click with Click With Options
    * - `#403`_
      - bug
      - medium
      - Improve exception raised by library when trying to click element which can not be clicked.
    * - `#428`_
      - enhancement
      - medium
      - use RF to convert timeout to correct value

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av1.6.0>`__.

.. _#380: https://github.com/MarketSquare/robotframework-browser/issues/380
.. _#230: https://github.com/MarketSquare/robotframework-browser/issues/230
.. _#226: https://github.com/MarketSquare/robotframework-browser/issues/226
.. _#424: https://github.com/MarketSquare/robotframework-browser/issues/424
.. _#403: https://github.com/MarketSquare/robotframework-browser/issues/403
.. _#428: https://github.com/MarketSquare/robotframework-browser/issues/428
