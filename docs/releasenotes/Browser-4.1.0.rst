=====================
Browser library 4.1.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 4.1.0 is a new release with
fixing file upload and providing HAR file support. Also this relase
contains PlayWright 1.10.0. There is also refactoring in the node side,
but that should not affect users. All issues targeted for Browser library
v4.1.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init

to install the latest available release or use
::
   pip install robotframework-browser==4.1.0
   rfbrowser init

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 4.1.0 was released on Thursday March 25, 2021. Browser supports
Python 3.7+, Robot Framework >=3.2+ and Node 12 and 14 LTS versions.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av4.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add support for recordHar when creating new context (`#704`_)
-------------------------------------------------------------
HAR record support is added to New Context keyword.

Backwards incompatible changes
==============================

Clean files created by Browser library at start of the test execution (`#477`_)
-------------------------------------------------------------------------------
By default browser saves screenshots and videos to ${OUPUTDIR}/Browser folder.
Now browser library deletes the ${OUPUTDIR}/Browser folder when test execution
starts.

Acknowledgements
================
Many thanks for all people who have reported issues and provided feedback
when using a library.

Fix doc bug in Click keyword (`#811`_)
--------------------------------------
Many thanks LDerikx for fixing the Click keyword documentation.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#477`_
      - enhancement
      - high
      - Clean files created by Browser library at start of the test execution
    * - `#704`_
      - enhancement
      - high
      - Add support for recordHar when creating new context
    * - `#811`_
      - bug
      - medium
      - Fix doc bug in Click keyword
    * - `#391`_
      - enhancement
      - medium
      - Set Browser Timeout should be ok to call even when no browser is open.
    * - `#814`_
      - enhancement
      - medium
      - NTLM authentication seems to be also supported
    * - `#843`_
      - bug
      - ---
      - Upload file broken when used to handle more than a single file upload

Altogether 6 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av4.1.0>`__.

.. _#477: https://github.com/MarketSquare/robotframework-browser/issues/477
.. _#704: https://github.com/MarketSquare/robotframework-browser/issues/704
.. _#811: https://github.com/MarketSquare/robotframework-browser/issues/811
.. _#391: https://github.com/MarketSquare/robotframework-browser/issues/391
.. _#814: https://github.com/MarketSquare/robotframework-browser/issues/814
.. _#843: https://github.com/MarketSquare/robotframework-browser/issues/843
