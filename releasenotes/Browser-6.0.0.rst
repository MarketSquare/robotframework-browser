=====================
Browser library 6.0.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 6.0.0 is a new release with
keyword to get urls in a page enhancements and bug fixes to the
keyword assertions. All issues targeted for Browser library v6.0.0 can
be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==6.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 6.0.0 was released on Tuesday July 20, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.12.3

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av6.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Assertion engine 0.1.0 breaks keyword Get Element State (`#1152`_)
------------------------------------------------------------------
Get Element State did not work correctly with default values the
keyword arguments, if assertion engine 0.1.0 or never was used.

This change is also slightly backwards incompatible, because now it
is mandatory to define both assertion operator and expected value.

Assertion should fail if expected value is given without operator (`#1142`_)
----------------------------------------------------------------------------
This was actully bug in the assertion engine dependency, but now
this release requires assertion engine 0.2.0 or greater.

Keyword to get url in a page  (`#1167`_)
----------------------------------------
There is new keyword to get crawl pages urls.

Backwards incompatible changes
==============================

When RF 4.1 out drop support RF 3.2 (`#1153`_)
----------------------------------------------
Support for Robot Framework 3.2 is dropped in this release. RF 3.2 or older
versions might still work, but they are not tested and therefore official
support is dropped.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1152`_
      - bug
      - critical
      - Assertion engine 0.1.0 breaks keyword Get Element State
    * - `#1142`_
      - bug
      - high
      - Assertion should fail if expected value is given without operator
    * - `#1153`_
      - enhancement
      - high
      - When RF 4.1 out drop support RF 3.2
    * - `#1167`_
      - enhancement
      - high
      - Keyword to get url in a page 
    * - `#664`_
      - enhancement
      - high
      - Auto closing and closing should log more explicitly
    * - `#815`_
      - enhancement
      - high
      - Add possiblity to set up screenshot directory
    * - `#949`_
      - bug
      - medium
      - Promise To Wait For Download keyword documentation issue
    * - `#992`_
      - bug
      - medium
      - Setting browser path by PLAYWRIGHT_BROWSERS_PATH not working anymore
    * - `#1126`_
      - enhancement
      - medium
      - Add information about playwright version to documentation

Altogether 9 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av6.0.0>`__.

.. _#1152: https://github.com/MarketSquare/robotframework-browser/issues/1152
.. _#1142: https://github.com/MarketSquare/robotframework-browser/issues/1142
.. _#1153: https://github.com/MarketSquare/robotframework-browser/issues/1153
.. _#1167: https://github.com/MarketSquare/robotframework-browser/issues/1167
.. _#664: https://github.com/MarketSquare/robotframework-browser/issues/664
.. _#815: https://github.com/MarketSquare/robotframework-browser/issues/815
.. _#949: https://github.com/MarketSquare/robotframework-browser/issues/949
.. _#992: https://github.com/MarketSquare/robotframework-browser/issues/992
.. _#1126: https://github.com/MarketSquare/robotframework-browser/issues/1126
