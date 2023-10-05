======================
Browser library 17.5.1
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 17.5.1 is a new release with
bug fixes rfbroser init when installing to Linux distributions and
creating docker image. All issues targeted for Browser library v17.5.1 can
be found from the `issue tracker`_.
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
install it manually. Browser library 17.5.1 was released on Monday September 25, 2023.
Browser supports Python 3.8+, Node 16/18 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.38.1

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v17.5.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
python -m Browser.entry does not anymore work (`#3100`_)
--------------------------------------------------------
Which broke docker image creation and supported entry point.

Remove forced usage --with-deps option from init (`#3105`_)
-----------------------------------------------------------
--with-deps was added because Playwright changed the installation procedure and library
added the --with-deps option on every installation. This did broke Linux installations outside
the supported Ubuntu distribution. Now --with-deps can be used as opt in way with `rfbrowser init`
command.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#3100`_
      - bug
      - critical
      - python -m Browser.entry does not anymore work
    * - `#3105`_
      - bug
      - critical
      - Remove forced usage --with-deps option from init

Altogether 2 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av17.5.1>`__.

.. _#3100: https://github.com/MarketSquare/robotframework-browser/issues/3100
.. _#3105: https://github.com/MarketSquare/robotframework-browser/issues/3105
