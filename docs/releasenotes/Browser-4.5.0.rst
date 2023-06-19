=====================
Browser library 4.5.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 4.5.0 is a new release with
support Playwright 1.11.0 and prevents using RF 4.0.2 with Browser library.
All issues targeted for Browser library v4.5.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==4.5.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 4.5.0 was released on Wednesday May 12, 2021. Browser supports
Python 3.7+, Robot Framework 3.2+ and Node LTS 12 and 14. Expect RF 4.0.2 is not
supported.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av4.5.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Do not use RF 4.0.2 (`#994`_)
-----------------------------
RF 4.0.2 has regression with keyword using TypedDict: https://github.com/robotframework/robotframework/issues/3969
RF 4.0.2 is excluded in the installation.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#994`_
      - bug
      - high
      - Do not use RF 4.0.2

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av4.5.0>`__.

.. _#994: https://github.com/MarketSquare/robotframework-browser/issues/994
