======================
Browser library 13.3.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 13.3.0 is a new release with
enhancements about cleaning Browser library output and several bug fixes.
All issues targeted for Browser library v13.3.0 can be found
from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and 
install it manually. Browser library 13.3.0 was released on Sunday July 10, 2022. 
Browser supports Python 3.7+, Node 12/14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.23.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av13.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Getter keywords fail on disabled but visible elements (`#2154`_)
----------------------------------------------------------------
Getter keyword failed if presenter mode was enabled. This is not fixed
and keyword should not anymore fail iwth presenter keywords.

Acknowledgements
================

Fix Close Page keyword documentation  (`#2142`_)
------------------------------------------------
Many thanks for Elout van Leeuwen for fixing documentation bugs.

Docu linting "Finding elements" and "Set Strict Mode" (`#2147`_)
----------------------------------------------------------------
Many thanks for UliSei for enhancing several keywords documentation.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2154`_
      - bug
      - high
      - Getter keywords fail on disabled but visible elements
    * - `#2142`_
      - bug
      - medium
      - Fix Close Page keyword documentation 
    * - `#2147`_
      - bug
      - medium
      - Docu linting "Finding elements" and "Set Strict Mode"
    * - `#2134`_
      - enhancement
      - medium
      - Do not blindly delete ${OUTPUT_DIR}/browser folder, because it might not be desired

Altogether 4 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av13.3.0>`__.

.. _#2154: https://github.com/MarketSquare/robotframework-browser/issues/2154
.. _#2142: https://github.com/MarketSquare/robotframework-browser/issues/2142
.. _#2147: https://github.com/MarketSquare/robotframework-browser/issues/2147
.. _#2134: https://github.com/MarketSquare/robotframework-browser/issues/2134
