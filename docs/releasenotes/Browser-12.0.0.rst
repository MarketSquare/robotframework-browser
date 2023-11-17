======================
Browser library 12.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 12.0.0 is a new release which
raises minimum required Robot Framework version to 4.1 and bug fixes to
Close Browser and Select Options By keywords. All issues targeted for
Browser library v12.0.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==12.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 12.0.0 was released on Tuesday February 22, 2022. Browser supports
Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. Library was
tested with Playwright 1.19.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av12.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Closing a browser should await for contexts of that browser to be closed (`#1133`_)
-----------------------------------------------------------------------------------
Now we close context explicitly context associated to the browser. Also we create
possible trace file when contex is closed.

Select Options By Keyword throws Error: locator.elementHandle (`#1622`_)
-------------------------------------------------------------------------------
This error happened when option element did not contain value attribute. If
option element does not contain value attribute, we try locate the option element
with the text in select.

Backwards incompatible changes
==============================

Raise minimum required RF version to 4.1.3 (`#1769`_)
-----------------------------------------------------
Browser library uses IntEnums in some keywords arguments, but Robot Framework 4.0 has
a bug in the argument conversion. This bug has been fixed in Robot Framework 4.1 release
and therefore minimum required version is raised to 4.1.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1133`_
      - bug
      - high
      - Closing a browser should await for contexts of that browser to be closed
    * - `#1622`_
      - bug
      - high
      - Select Options By Keyword throws Error: locator.elementHandle
    * - `#1769`_
      - enhancement
      - high
      - Raise minimum required RF version to 4.1.3


Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av12.0.0>`__.

.. _#1133: https://github.com/MarketSquare/robotframework-browser/issues/1133
.. _#1622: https://github.com/MarketSquare/robotframework-browser/issues/1622
.. _#1769: https://github.com/MarketSquare/robotframework-browser/issues/1769
