=====================
Browser library 2.5.0
=====================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 2.5.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v2.5.0 can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser==2.5.0
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library 2.5.0 was released on Thursday January 7, 2021. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av2.5.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Add optional message parameter to all keywords using assertion engine. (`#602`_)
- Playwright has deprecated videoSize and videosPath arguments and users should move to recordVideo (`#617`_)

Deprecated features
===================

- Playwright has deprecated videoSize and videosPath arguments and users should move to recordVideo (`#617`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#446`_
      - enhancement
      - high
      - Add optional message parameter to 'Wait For Elements State' 
    * - `#617`_
      - enhancement
      - high
      - Playwright has deprecated videoSize and videosPath arguments and users should move to recordVideo
    * - `#602`_
      - enhancement
      - medium
      - Add optional message parameter to all keywords using assertion engine.

Altogether 3 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av2.5.0>`__.

.. _#446: https://github.com/MarketSquare/robotframework-browser/issues/446
.. _#617: https://github.com/MarketSquare/robotframework-browser/issues/617
.. _#602: https://github.com/MarketSquare/robotframework-browser/issues/602
