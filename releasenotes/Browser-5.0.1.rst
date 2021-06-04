=====================
Browser library 5.0.1
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 5.0.1 is a new release with
bug fixes. This release fixes when using library from Python and when
passing httpCredentials as secret in New Context keyword. All issues
targeted for Browser library v5.0.1 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==5.0.1
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 5.0.1 was released on Friday June 4, 2021. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av5.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

httpCredentials with $variable is not working (`#1046`_)
--------------------------------------------------------
If New Context httpCredentials was  used as {'username': '$username', 'password': '$pwd'}
then it not resolve $username and $pwd correctly. Now variables are resolved
correctly.

Acknowledgements
================

Lingering node processes when running in Python (`#1033`_)
----------------------------------------------------------
Many thanks for Ossi R. for fixing bug when using library directly from Python side.
Library did not perform cleanup properly if library was used from Python and
now when library closes browsers/context/pages when atexit is called.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1046`_
      - bug
      - critical
      - httpCredentials with $variable is not working
    * - `#1033`_
      - bug
      - high
      - Lingering node processes when running in Python

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av5.0.1>`__.

.. _#1046: https://github.com/MarketSquare/robotframework-browser/issues/1046
.. _#1033: https://github.com/MarketSquare/robotframework-browser/issues/1033
