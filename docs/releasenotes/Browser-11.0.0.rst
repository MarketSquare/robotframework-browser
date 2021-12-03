======================
Browser library 11.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 11.0.0 is a new release with
enhancements to JS extension documentation, version binding to Playwright and other
enhancement and bug fixes. All issues targeted for Browser library v11.0.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==11.0.0
   rfbrowser init

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 11.0.0 was released on Saturday December 4, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.17.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av11.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Crawler fails if site has a link to a pdf (`#1463`_)
------------------------------------------------------
Crawling site did fail if there was link to pwf in the page. This is fixed in this release.

Add version binding between Playwright and Browser (`#591`_)
------------------------------------------------------------
In previous releases we did only tell minimum required Playwright version, which caused
problems with environment setups and sometimes some backwards incompatible issues. Starting
from this release, Playwright version is bind and library supports only one version of
Playwright.

Enable keyword documentation for JsExtentions (`#775`_)
-------------------------------------------------------
In previous releases we did support extending library by adding new keywords trough JS plugin,
but creating keyword documentation of the JS keywords not very well supported. This is now enhanced
and library also produces documentation from JS extension keywords.

Backwards incompatible changes
==============================

With New Page keyword return also path to video (`#1424`_)
----------------------------------------------------------
New Page returned only the UUID of the page, with this release it returns an object
which also contains path to the video if one is created.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1463`_
      - bug
      - high
      - Crawler fails if site has a link to a pdf
    * - `#591`_
      - enhancement
      - high
      - Add version binding between Playwright and Browser
    * - `#775`_
      - enhancement
      - high
      - Enable keyword documentation for JsExtentions
    * - `#1536`_
      - bug
      - medium
      - yarn run lint does not work on Windows because lint script in package.json is using single quotes
    * - `#1424`_
      - enhancement
      - medium
      - With New Page keyword return also path to video
    * - `#1465`_
      - bug
      - low
      - No library '<Browser.browser.Browser object at 0x0AB06030>' found.

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av11.0.0>`__.

.. _#1463: https://github.com/MarketSquare/robotframework-browser/issues/1463
.. _#591: https://github.com/MarketSquare/robotframework-browser/issues/591
.. _#775: https://github.com/MarketSquare/robotframework-browser/issues/775
.. _#1536: https://github.com/MarketSquare/robotframework-browser/issues/1536
.. _#1424: https://github.com/MarketSquare/robotframework-browser/issues/1424
.. _#1465: https://github.com/MarketSquare/robotframework-browser/issues/1465
