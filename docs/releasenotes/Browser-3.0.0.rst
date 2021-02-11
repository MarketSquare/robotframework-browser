=====================
Browser library 3.0.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 3.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v3.0.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==3.0.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 3.0.0 was released on Thursday January 14, 2021. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av3.0.0


.. contents::
   :depth: 2
   :local:

Backwards incompatible changes
==============================

- Wait For Download should also allow browser suggested filename (`#597`_)
  - Deprecated old Wait For Download and added Promise To Wait For Download KW.
- Change Download keyword to also return suggested filename (`#642`_)
  - The new structure of the returned data is backwards-incompatible.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#597`_
      - enhancement
      - high
      - Wait For Download should also allow browser suggested filename
    * - `#642`_
      - enhancement
      - high
      - Change Download keyword to also return suggested file name
    * - `#652`_
      - bug
      - medium
      - New Context keyword revordVideo argument is not correctly defined
    * - `#657`_
      - bug
      - medium
      - Fix Handle Future Dialogs keyword docs

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av3.0.0>`__.

.. _#597: https://github.com/MarketSquare/robotframework-browser/issues/597
.. _#642: https://github.com/MarketSquare/robotframework-browser/issues/642
.. _#652: https://github.com/MarketSquare/robotframework-browser/issues/652
.. _#657: https://github.com/MarketSquare/robotframework-browser/issues/657
