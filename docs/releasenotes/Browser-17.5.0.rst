======================
Browser library 17.5.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 17.5.0 is a new release with
enhancements on installation. rfbrowser init command support now also defining
which browser binaries are installed. Also closing page has runBeforeUnload and
and there id default option for automatic page closing.
All issues targeted for Browser library v17.5.0 can be found
from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and
install it manually. Browser library 17.5.0 was released on Sunday September 24, 2023.
Browser supports Python 3.8+, Node 16/18 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.38.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v17.5.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Close page does not have the runBeforeUnload option. (`#3054`_)
---------------------------------------------------------------
If runBeforeUnload is false, does not run any unload handlers and waits for the page to be closed.
If runBeforeUnload is true the method will run unload handlers, but will not wait for the page to close.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3054`_
      - enhancement
      - high
      - Close page does not have the runBeforeUnload option.
    * - `#3036`_
      - bug
      - medium
      - Wait For Condition don't honour timout value
    * - `#3083`_
      - bug
      - medium
      - Will "click" keyword be totally removed from browser library
    * - `#3098`_
      - enhancement
      - medium
      - Add support for PW 1.38 way install browsers binaries separetly

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av17.5.0>`__.

.. _#3054: https://github.com/MarketSquare/robotframework-browser/issues/3054
.. _#3036: https://github.com/MarketSquare/robotframework-browser/issues/3036
.. _#3083: https://github.com/MarketSquare/robotframework-browser/issues/3083
.. _#3098: https://github.com/MarketSquare/robotframework-browser/issues/3098
