=====================
Browser library 5.1.2
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 5.1.2 is a new release with
bug fixe to Wait For Element State keyword custom error message. Also
this release updates Playwright to 1.21.3. All issues targeted for
Browser library v5.1.2 can be found from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==5.1.2
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 5.1.2 was released on Tuesday June 29, 2021. Browser supports
Python 3.7+, Node 12/14 LTS and Robot Framework 3.2+.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av5.1.2


.. contents::
   :depth: 2
   :local:

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1110`_
      - bug
      - medium
      - Message formatting in "Wait For Elements State" uses the given timeout even when it is None

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av5.1.2>`__.

.. _#1110: https://github.com/MarketSquare/robotframework-browser/issues/1110
