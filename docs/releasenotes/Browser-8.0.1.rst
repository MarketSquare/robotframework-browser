=====================
Browser library 8.0.1
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 8.0.1 is a new release with
bug fixes to strict mode documentation. All issues targeted for Browser
library v8.0.1 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::

   pip install --upgrade robotframework-browser
   rfbrowser init

to install the latest available release or use
::

   pip install robotframework-browser==8.0.1
   rfbrowser init

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 8.0.1 was released on Monday September 13, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+. Library was
tested with Playwright 1.14.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av8.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Fix strict mode docs (`#1301`_)
---------------------------------

This release fixes documentation bug with strict mode. Nothing else is changed to
8.0.0 release.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1301`_
      - bug
      - critical
      - Fix strict mode docs

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av8.0.1>`__.

.. _#1301: https://github.com/MarketSquare/robotframework-browser/issues/1301
