=====================
Browser library 7.2.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 7.2.0 is a new release with
enhancements to record selector funtionality and bug fixes.
All issues targeted for Browser library v7.2.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==7.2.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 7.2.0 was released on Tuesday September 7, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.14.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av7.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Multiple frame piercing does not work (`#1259`_)
------------------------------------------------
There is fix for frame piercing selector. 


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1259`_
      - bug
      - critical
      - Multiple frame piercing does not work
    * - `#1257`_
      - enhancement
      - medium
      - Record Selector improvements

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av7.2.0>`__.

.. _#1259: https://github.com/MarketSquare/robotframework-browser/issues/1259
.. _#1233: https://github.com/MarketSquare/robotframework-browser/issues/1233
.. _#1257: https://github.com/MarketSquare/robotframework-browser/issues/1257
