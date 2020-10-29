=====================
Browser library 2.0.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 2.0.0 is a new release with
fixed installation problems in Windows OS by using grpc-js instead of grpc.
This release also fixes logic in internal node side implementation.
All issues targeted for Browser library v2.0.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==2.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 2.0.0 was released on Thursday October 29, 2020. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Selenium: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av2.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Installation issues with dependencies (`#455`_)
-----------------------------------------------
Browser library was difficult to install in Windows OS, because of the node grpc
dependency. It was difficult to install, because it required MS build tools and elevated
access rights to compile the dependency.

Fix internal TS logic  (`#462`_)
--------------------------------
There was several bugs in the internal node implementation when accessing Playwright
methods and attributes. This have caused at least errors in the logging and possible
unexpected freezes when executing tests. The node side implementation has been improved
and users should have better experience with the library.

Backwards incompatible changes
==============================

Remove Click With Options keyword  (`#461`_)
--------------------------------------------
Click With Options keyword was deprecated in 1.6.0 release. Now keywords is removed.
Please migrate to Click keyword, which has same capabilities as old Click With Options keyword.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#455`_
      - bug
      - critical
      - Installation issues with dependencies
    * - `#462`_
      - bug
      - critical
      - Fix internal TS logic 
    * - `#461`_
      - enhancement
      - high
      - Remove Click with options keyword 

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av2.0.0>`__.

.. _#455: https://github.com/MarketSquare/robotframework-browser/issues/455
.. _#462: https://github.com/MarketSquare/robotframework-browser/issues/462
.. _#461: https://github.com/MarketSquare/robotframework-browser/issues/461
