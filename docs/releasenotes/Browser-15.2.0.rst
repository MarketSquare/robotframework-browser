======================
Browser library 15.2.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 15.2.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v15.2.0 can be found
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
install it manually. Browser library 15.2.0 was released on Wednesday February 1, 2023.
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+.
Library was tested with Playwright 1.30.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v15.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Improved Scope Stack [*usable for plugins*]
------------------------------------------------------

Scope of some keywords where implemented more or less manually.
This has now been updated to be usable more dynamically and that plugins can also use
scopes. See this atest example how `last_log_message` attribute is stored and read from Scope Stack:
`Example Plugin <https://github.com/MarketSquare/robotframework-browser/blob/main/atest/test/09_Plugins/ExamplePlugin.py>`__

Also `Show Keyword Banner`_ and `Register Keyword To Run On Failure`_ also got a scope parameter now.

Improved code completion when used from python
----------------------------------------------

Code completion in python plugins and also when working with Browser lib from Python
should be improved by switching from `__init__.pyi` to `browser.pyi`

Improved logging when returned values contain non-printable characters
----------------------------------------------------------------------

When non printable characters are in Element Text or attributes, these where not logged.
Therefore the debugging was somethimes a bit hard until users realize that there where special
characters present. Non printable unicode characters should be now visible with their unicode code.


Use the Get Style keyword with pseudo-elements and all avaiable css attributes
-----------------------------------------------------------------------------------------
`Get Style`_ keyword got a new argument `pseudo_element` which can be used to fetch styles
from pseudo elements like `::before` or `::after`, etc.

Also the `key` attribute is now capable to accept any css property that can be set by css directly.
i.e. the key `border` that contains all border information was not possible.
The atomic values like `border-left-width` and `border-right-width` had to be used.
Now it is possible to use any property like `border` or `border-width` as key filter.


New PythonLibCore used to enable Listern in Plugins
---------------------------------------------------

A python plugin can now be a Library Listener of Robot Framework.
Just by setting `ROBOT_LISTENER_API_VERSION` to either `2` or `3` as class field
a python plugin class can become a listener like shown in `Example Plugin <https://github.com/MarketSquare/robotframework-browser/blob/main/atest/test/09_Plugins/ExamplePlugin.py>`__


Fixed some bugs in `Record Selector` keyword
--------------------------------------------

When calling `Record Selector` keyword twice Browser lib could crash.
On Some webpages the location of the buttons were at the wrong position.


Playwright 1.30.0 used
----------------------

New Release just brings new Browser versions.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2608`_
      - bug
      - critical
      - Improved Scope Stack
    * - `#2564`_
      - enhancement
      - high
      - Ability to use the Get Style keyword to get CSS pseudo-element style
    * - `#2570`_
      - bug
      - medium
      - [Bug] Get code completion for LibraryComponent.library does not work correctly
    * - `#2598`_
      - bug
      - medium
      - Using `Record Selector` twice crashes the browser
    * - `#2614`_
      - bug
      - medium
      - Confusing documentation for `Get Classes` keyword

Altogether 5 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av15.2.0>`__.

.. _Get Style: https://marketsquare.github.io/robotframework-browser/Browser.html#Get%20Style
.. _Register Keyword To Run On Failure: https://marketsquare.github.io/robotframework-browser/Browser.html#Register%20Keyword%20To%20Run%20On%20Failure
.. _Show Keyword Banner: https://marketsquare.github.io/robotframework-browser/Browser.html#Show%20Keyword%20Banner
.. _#2608: https://github.com/MarketSquare/robotframework-browser/issues/2608
.. _#2564: https://github.com/MarketSquare/robotframework-browser/issues/2564
.. _#2570: https://github.com/MarketSquare/robotframework-browser/issues/2570
.. _#2598: https://github.com/MarketSquare/robotframework-browser/issues/2598
.. _#2614: https://github.com/MarketSquare/robotframework-browser/issues/2614
