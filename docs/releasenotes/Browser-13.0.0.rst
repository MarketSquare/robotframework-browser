======================
Browser library 13.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 13.0.0 is a new release with
New Persistent Context keyword enhancements and removes drop argument from
Drag And Drop By Coordinates keyword. All issues targeted for Browser library
v13.0.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==13.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 13.0.0 was released on Wednesday May 25, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.22.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av13.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

How can I use this library and still request a different profile when browser is launched?   (`#963`_)
------------------------------------------------------------------------------------------------------
Library is enhanced to support persistent context, this is supported by New Persistent Context keyword.
This example support adding extension with the opened browser. Please note that New Persistent
Context keyword is not support with WebKit.

Backwards incompatible changes
==============================

Remove drop argument from Drag And Drop By Coordinates keyword.  (`#2042`_)
---------------------------------------------------------------------------
Drop argument did not work and is removed from Drag And Drop By Coordinates
keyword.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2042`_
      - enhancement
      - critical
      - Remove drop argument from Drag And Drop By Coordinates keyword. 
    * - `#963`_
      - enhancement
      - high
      - How can I use this library and still request a different profile when browser is launched?  
    * - `#2035`_
      - bug
      - medium
      - Log file name typo (`"rfborwser.log"` -> `"rfbrowser.log"`)

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av13.0.0>`__.

.. _#2042: https://github.com/MarketSquare/robotframework-browser/issues/2042
.. _#963: https://github.com/MarketSquare/robotframework-browser/issues/963
.. _#2035: https://github.com/MarketSquare/robotframework-browser/issues/2035
