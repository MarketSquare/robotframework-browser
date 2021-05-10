=====================
Browser library 4.4.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 4.4.0 is a new release with
several bug fixes and dependency updates.
All issues targeted for Browser library v4.4.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==4.4.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 4.4.0 was released on Monday May 10, 2021. Browser supports
Python 3.7+, Robot Framework 3.2+ and Node LTS 12 and 14.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av4.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

When new browser or/and context is opened implicitly, display that in logs.  (`#974`_)
--------------------------------------------------------------------------------------
In the past it was not visible in the logs, if the New Page opened new browser and/or
context. Also it was visible if New Context opened new browser. This is now logged
when the keywords are called and it will help debugging problematic cases.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#974`_
      - enhancement
      - high
      - When new browser or/and context is opened implicitly, display that in logs. 
    * - `#893`_
      - bug
      - medium
      - Browser Keyword "Fill Secret" generates warning in combination with Robotframework 4.0
    * - `#953`_
      - bug
      - medium
      - More explanation during installation needed
    * - `#962`_
      - bug
      - medium
      - None is returned if `selector` is not given for `Execute JavaScript` and `Wait For Function`

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av4.4.0>`__.

.. _#974: https://github.com/MarketSquare/robotframework-browser/issues/974
.. _#893: https://github.com/MarketSquare/robotframework-browser/issues/893
.. _#953: https://github.com/MarketSquare/robotframework-browser/issues/953
.. _#962: https://github.com/MarketSquare/robotframework-browser/issues/962
