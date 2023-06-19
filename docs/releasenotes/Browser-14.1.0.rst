======================
Browser library 14.1.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 14.1.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v14.1.0 can be found
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
install it manually. Browser library 14.1.0 was released on Sunday September 25, 2022. 
Browser supports Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.25.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av14.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Implemented Selector Prefix and small Bugfixes (`#2332`_)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With prefixes to selectors, it is possible to define i.e. an iframe selector,
that shall be prefixed to all selectors used in the future.
Prefixes have also a scope, which has been added in 14.0.0.
This means, that the prefix is only valid for the scope it has been defined to
and is automatically removed when the scope is left.
Scopes can be `Global`, `Suite` and `Test`/`Task`.

Selector Prefix can also be defined on Library import.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2332`_
      - enhancement
      - high
      - implemented Selector Prefix and small Bugfixes

Altogether 1 issue. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av14.1.0>`__.

.. _#2332: https://github.com/MarketSquare/robotframework-browser/issues/2332
