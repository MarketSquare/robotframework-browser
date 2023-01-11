======================
Browser library 15.0.0
======================


.. default-role:: code

⚠️ **Release 15.0.0 has some breaking changes. Please read the release notes carefully.** ⚠️

Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 15.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v15.0.0 can be found
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
install it manually. Browser library 15.0.0 was released on Wednesday January 11, 2023. 
Browser supports Python 3.7+, Node 14/16 LTS and Robot Framework 4.0+. 
Library was tested with Playwright 1.29.2

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3Av15.0.0
.. _Plugin Documentation: https://github.com/MarketSquare/robotframework-browser/blob/main/docs/plugins/README.md


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- 🔌 **Python & JavaScript Plugins can now be used together.** See `Plugin Documentation`_ for more information and examples.
- Calling "New Page" fails after creating the context using "New Persistent Context" with recordVideo argument (`#2214`_)
- `New Context` with `recordVideo` without size does not default to viewport. (`#2530`_)
- Value of variable '@{attributes}' is not list or list-like. (`#2513`_)
- "New Context" and "New Persistent Context" keywords should always return a Path-object with full video path in recordVideo dictionary (`#2215`_)
- Reimports of Browser library cleans ${OUTPUT_DIR}/browser during the same robot run (`#2522`_)
- Remove support for direct value assignment for Type/Fill Secret (`#2523`_)
- Keyword "Fill Secret": Too tight/incomplete coupling with CryptoLibrary (`#2536`_)
- Topic/fixes & removed deprecations (`#2524`_)

Backwards incompatible changes
==============================

Return values of some keyword are not always list. (`#2513`_)
-------------------------------------------------------------
The keyword `Get Attribute Names`, `Get Classes` and `Get Selected Options` did return
lists except if there was only one value to return, then it was the single value.
This was inconsistent and now all of them return lists even if there is nothing to
return. In this case it would be an empty list.

New Context and Video Recording
-------------------------------
The deprecated arguments `videoSize` and `videosPath` are now removed.

The docs of `New Context` mentioned that if no `size` in `recordVideo` argument was given,
it would record in the viewports dimensions.
That was not working correctly, which is now fixed. (`#2530`)

Also is the `path` value of `recordVideo` was behaving inconsistent.
It is now always relative to ${OUTPUT_DIR}/browser/video except if it is an absolute path.
Also empty strings can be used as `path` attribute.

New Persistent Context
----------------------

The `New Persistent Context` keyword does actially opens a new browser, a new context
and a new page. It howevery only returned the `contextID` of the currently opened context.
The Id of the browser or page could only be fetched from the browser catalog.
This has changed and `New Persistent Context` now returns nowthe `browserID`,
`contextID` and dictionary of `NewPageDetails` as well.
`NewPageDetails` is a dictionary with the keys `'page_id': <str>` and `'video_path': <str>`.

Removed deprecated Keywords
---------------------------

`Get Element State` & `Execute Javascript` were deprecated some time ago and now removed.
(`#2524`_)

Secret handling and direct value assignment
-------------------------------------------

`Fill Secret`, `Type Secret` do not log the secret value given.
They deprecated the assignment of variables or values a while ago.
Now the direct assignment is removed. (`#2523`_)

They only accept variables in the form of `$variable` instead of `${variable}` now!

Also the `password` attribute of `httpCredentials` needs to be in this special
variable syntax now.

All three do also support cipher decryption of CryptoLibrary, if it is installed and
imported. (`#2536`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2214`_
      - bug
      - critical
      - Calling "New Page" fails after creating the context using "New Persistent Context" with recordVideo argument
    * - `#2530`_
      - bug
      - critical
      - `New Context` with `recordVideo` without size does not default to viewport.
    * - `#2513`_
      - enhancement
      - critical
      - Value of variable '@{attributes}' is not list or list-like.
    * - `#2215`_
      - bug
      - high
      - "New Context" and "New Persistent Context" keywords should always return a Path-object with full video path in recordVideo dictionary
    * - `#2522`_
      - bug
      - high
      - Reimports of Browser library cleans ${OUTPUT_DIR}/browser during the same robot run
    * - `#2523`_
      - enhancement
      - high
      - Remove support for direct value assignment for Type/Fill Secret
    * - `#2536`_
      - enhancement
      - high
      - Keyword "Fill Secret": Too tight/incomplete coupling with CryptoLibrary
    * - `#2524`_
      - bug
      - high
      - Topic/fixes & removed deprecations
    * - `#2494`_
      - bug
      - medium
      - Broken docstring links for keywords like: `New Browser`, `Wait For Request`, `Wait For Response`

Altogether 9 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av15.0.0>`__.

.. _#2214: https://github.com/MarketSquare/robotframework-browser/issues/2214
.. _#2530: https://github.com/MarketSquare/robotframework-browser/issues/2530
.. _#2513: https://github.com/MarketSquare/robotframework-browser/issues/2513
.. _#2215: https://github.com/MarketSquare/robotframework-browser/issues/2215
.. _#2522: https://github.com/MarketSquare/robotframework-browser/issues/2522
.. _#2523: https://github.com/MarketSquare/robotframework-browser/issues/2523
.. _#2536: https://github.com/MarketSquare/robotframework-browser/issues/2536
.. _#2524: https://github.com/MarketSquare/robotframework-browser/issues/2524
.. _#2494: https://github.com/MarketSquare/robotframework-browser/issues/2494
