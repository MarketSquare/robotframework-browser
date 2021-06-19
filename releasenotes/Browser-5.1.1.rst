=====================
Browser library 5.1.1
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 5.1.1 is a new release with
a bug fix for "rfbrowser show-trace" command in Windows OS.
All issues targeted for Browser library v5.1.1 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==5.1.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 5.1.1 was released on Saturday June 19, 2021. Browser supports
Python 3.7+, and Robot Framework 3.2+.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av5.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

rfbrowser show-trace can't find zipfile (`#1085`_)
--------------------------------------------------
rfbrowser show-trace did not work in Windows OS, this is now fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1085`_
      - bug
      - critical
      - rfbrowser show-trace can't find zipfile

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av5.1.1>`__.

.. _#1085: https://github.com/MarketSquare/robotframework-browser/issues/1085
