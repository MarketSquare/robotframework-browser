=====================
Browser library 5.0.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 5.0.0 is a new release with
masking password username and password in the New Context keyword and
Wait For Alert keyword to get alert text enhancements. All issues targeted
for Browser library v5.0.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==5.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 5.0.0 was released on Wednesday May 19, 2021. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av5.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

New Context >> httpCredentials Logs password clearly to log.html (`#946`_)
--------------------------------------------------------------------------
New Context httpCredentials argument used to leak username and password to output
files. Also it is possible to provide username and password with % abd $ prefix
which will allows to keyword to discover the variable values internally. This will
prevent leaking the secrets in the Robot Framework output files, but if Playwright
debug log is enabled, secrets are written to debug log as plain text.

Because keyword now logs a warning if secrets are inputted as plain text and
therefore this change is backwards indomitable.

Assert future dialogs (`#440`_)
-------------------------------
There is a new keyword: Wait For Alert, which must be used with Promise To keyword.
But new keyword returns the text from alert and offers possibility to assert the
text in the alert.

Backwards incompatible changes
==============================

**EXPLAIN** or remove these.

- New Context >> httpCredentials Logs password clearly to log.html (`#946`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#946`_
      - bug
      - high
      - New Context >> httpCredentials Logs password clearly to log.html
    * - `#440`_
      - enhancement
      - high
      - Assert future dialogs


Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av5.0.0>`__.

.. _#946: https://github.com/MarketSquare/robotframework-browser/issues/946
.. _#440: https://github.com/MarketSquare/robotframework-browser/issues/440
