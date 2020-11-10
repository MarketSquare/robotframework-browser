=====================
Browser library 2.1.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 2.1.0 is a new release with
video support and prevents secrets for leaking in Robot Framework logs. There
are also several fixes in the release. All issues targeted for Browser
library v2.1.0 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==2.1.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 2.1.0 was released on Monday November 9, 2020. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av2.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Use Playwright video to allow recording video of the test execution. (`#148`_)
------------------------------------------------------------------------------
Playwright has supported creating video for few releases. Now the library has been
enhanced to support video creation in New Context keyword. If video is enabled in
the context, new page will create a video.

Improve library logging when waiting. (`#491`_)
-----------------------------------------------
If keyword polled page internally in the Python code side, it caused lot of extra logging
in the log.html. This is now fixed and only the last poll, fail or success, is visible
in the log file.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#148`_
      - enhancement
      - high
      - Use Playwright video to allow recording video of the test execution.
    * - `#491`_
      - enhancement
      - high
      - Improve library logging when waiting.
    * - `#421`_
      - bug
      - medium
      - `Fill secret` leaks the secret into log.html
    * - `#473`_
      - bug
      - medium
      - The link to playwright's 'deviceDescriptors.ts' of keywords 'Get Device' and 'Get Devices' has been changed
    * - `#479`_
      - bug
      - medium
      - Get Cookie fails if cookie does not have expiry date and return_type=dict. 

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av2.1.0>`__.

.. _#148: https://github.com/MarketSquare/robotframework-browser/issues/148
.. _#491: https://github.com/MarketSquare/robotframework-browser/issues/491
.. _#421: https://github.com/MarketSquare/robotframework-browser/issues/421
.. _#473: https://github.com/MarketSquare/robotframework-browser/issues/473
.. _#479: https://github.com/MarketSquare/robotframework-browser/issues/479
