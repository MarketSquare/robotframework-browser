======================
Browser library 18.0.0
======================


.. default-role:: code


Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library 18.0.0 is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library v18.0.0 can be found
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
install it manually. Browser library 18.0.0 was released on Tuesday November 21, 2023.
Browser supports Python 3.8+, Node 18/20 LTS and Robot Framework 5.0+.
Library was tested with Playwright 1.40.0

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/v18.0.0


.. contents::
   :depth: 2
   :local:


Thanks To Our Sponsors
======================

This is the most significant release we've had in a long time. We've implemented 31 feature
requests and bug fixes, reducing our open issues to an incredibly low number of just 11.

This would not have been possible without the financial support of our sponsors.
A special thanks to the members of the Robot Framework Foundation_ and its board.
The Foundation has once again valued our project and decided to support us financially.
This support is a huge help, and we are very grateful for it.

We also want to thank one of our user companies, which has chosen to remain unnamed,
for their financial support. Their contribution made the development of the
`Connect To Browser` via CDP keyword possible.


Most important enhancements
===========================


macOS Sonoma (14.0) fixes
-------------------------

For unknown reasons the new macOS 14 did not work properly with Browser library.
A timing issue during the library startup caused problems.
This should be fixed now, by an internal workaround.


Browser Server and Connection to running Browsers
-------------------------------------------------

It was already possible to connect to a running instance of a Playwright Browser server
via websockets with `Connect To Browser` keyword. However it was not trivial to launch
such a browser server. Now it is also possible to launch such
server via `Launch Browser Server` keyword and close it again with `Close Browser Server`
and also run it independantly of Robot Framework via CLI option with `rfbrowser launch-browser-server`.

Furthermore we have implemented the option to connect to a running chromium based browser instance
over Chrome DevTools Protocol (CDP) with `Connect To Browser` keyword and the argument `use_cdp=True`.
To open a chromium based browser with CDP enabled, you can just start it with the argument
`--remote-debugging-port=9222`. At the moment it is not yet support to set additional connection
options, but this can be added in the future.

Launching a Browser Server as a separate may be useful for distribute executions.
The command `rfbrowser launch-browser-server` accepts all the same arguments as `Launch Browser Server`/`New Browser`
keyword. See `rfbrowser launch-browser-server --help` for more information.

More Browser, Context, Page stuff
---------------------------------

Some of our users had the wish that the browser stays open after finishing the execution.
This is now possible with the new `Closing Level` `KEEP` that will never close the browser.
!!! BUT BE AWARE !!! This will let a Node process open in the background, which may cause
resource issues on your machine. So use this option with care!!!

`New Page` and `Go To` keywords got a new argument `wait_until` which allows to wait for
a specific condition before continuing. This is useful if you already want to continue with the test
once the page starts loading or once the page is fully loaded or when the network is idle for 500ms.

Some **Backwards Incompatible** changes are also included.
One is the improved handling of the Browser Catalog which leads to a more consistent
but slightly different behavior than before:

- `New Persistent Context` did already in the past reuse the same browser, however it was listed
  twice in the Browser Catalog. Now if `New Persistent Context` is called multiple times, multiple
  contexts are created, but they all reuse the same browser.
- When `New Page` keyword or `New Persistent Browser` keyword were failing due to a timeout
  during page loading, the browser, context and page were already created but due to the timeout
  removed from Browser Catalog. This made it impossible to use the browser, context or page or even close them.
  Now the newly created elements are also properly closed when a timeout happens, so that there is no
  zombies left behind.
- We removed all deprecated arguments from `New Persistent Context` and `New Context`.
  These arguments where already without any function, but now finally removed.

File Downloads
--------------

We already had the possibility to download files with the `Download` keyword and `Promise To Download File`.
These keyword did finish (promise resolved) once the actual download has been fully completed.
The timeout on the other side were just used until the download started/the file chooser opened.
This could lead to the situation where tests had to wait for a long time until the download finished
and the next download could be started.

We now added two arguments to `Download` and `Promise To Download File` keyword which allows to
return once the download has been started with a download id.
That id then can be used to poll the download `Get Download State` or even cancel it with `Cancel Download`.

Assertion Formatters
--------------------

Assertion Formatters are a pretty unknown feature of Browser library.
With this feature it is possible to configure a Getter keyword so that it always applies that "formatter"
before returning or asserting the value. This is useful if you want to assert a value that has been stripped
and converted to lowercase before. One very helpful formatter is `normalize spaces`  wich converts all
kind of whitespace (also NBSP) to a single space, which makes it easier to assert values that may contain
different kind of whitespace.

These formatters are now set to a specific keyword to a limited scope. By default the scope is within the Suite.
We also added a `LambdaFunction` possibility which allows the users to define their own formatter function.

Documentation of Assertion Formatters has also been improved and now includes proper type hinds.
This on the other hand make them backwards incompatible if they have been used from Python with string arguments.

Robot Framework 7 Support
-------------------------

Due to some changes in internal Robot Framework API, the previous version of Browser library
was not compatible with Robot Framework 7. Browser Library 18.0.0 is now compatible with Robot Framework 7.

Robot Framework 7 also introduced the possibility to document return types of keywords in the keyword
documentation. We therefore have updated some of our return types to better document the behavior of the keywords.
All Getter keywords do have a type hint of their natural return type, ignoring the possibility of manipulating
with `then` or `evaluate` assertion operator.



Backwards incompatible changes
==============================

- storageState can't use in New Persistent Context (`#2679`_)
- New Page and New Persistent Context do not close again if Go To fails (`#3242`_)
- Drop support NodeJS 16 and start stupporing NodeJS 20 (`#3180`_)
- Added functionality to trigger multiple downloads at a time and not wait for them to finish (`#3231`_)
- Remove ALL deprecated features. (`Click` etc) (`#3243`_)
- Support Playwright 1.40 (TimeoutError became Error) (`#3252`_)


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#2679`_
      - bug
      - critical
      - storageState can't use in New Persistent Context
    * - `#2968`_
      - bug
      - critical
      - stdout to logfile prevents playwright to work correctly
    * - `#3154`_
      - bug
      - critical
      - When using M1 or M2 chip and sunning macOS Sonoma Browser library might cause a hang
    * - `#3254`_
      - enhancement
      - critical
      - Robot Framework 7.0 Support and Support for Return Types
    * - `#1702`_
      - bug
      - high
      - Take screenshot filename argument failing when registered to be run on failure
    * - `#3208`_
      - bug
      - high
      - [Setting Scope is broken] "Set Browser Timeout" does not work together with "Wait for Condition"
    * - `#3219`_
      - bug
      - high
      - Permissions uses _ (underscore) instead of - (dash)
    * - `#2571`_
      - enhancement
      - high
      - Keyword "Set Assertion Formatters" should have a scope
    * - `#2676`_
      - enhancement
      - high
      - Add keyword: Attach to Running Browser (Extend `Connect To Browser`)
    * - `#3180`_
      - enhancement
      - high
      - Drop support NodeJS 16 and start stupporing NodeJS 20
    * - `#3264`_
      - enhancement
      - high
      - Create Keyword and CLI option to "launch" a Playwright "BrowserServer"
    * - `#395`_
      - enhancement
      - high
      - [Feature] Go to should return HTTP status code
    * - `#1688`_
      - bug
      - medium
      - Incorrect path and filename when Take Screenshot registered to run on failure
    * - `#2129`_
      - bug
      - medium
      - `statusText` is empty for HTTP/2 request in Chromium
    * - `#2754`_
      - bug
      - medium
      - Examples at https://robotframework-browser.org/ broken
    * - `#3006`_
      - bug
      - medium
      - Question - argument - enable_presenter_mode
    * - `#3156`_
      - bug
      - medium
      - Misleading log message
    * - `#3200`_
      - bug
      - medium
      - `Promise To` does not work with `*args`
    * - `#3242`_
      - bug
      - medium
      - New Page and New Persistent Context do not close again if `Go To` fails
    * - `#3256`_
      - bug
      - medium
      - rfbrowser init logs wrong installation path
    * - `#1098`_
      - enhancement
      - medium
      - [Feature] Promise To Wait For Download with custom timeout argument
    * - `#1263`_
      - enhancement
      - medium
      - Automatic Closing Level MANUAL: keep open after terminating the test
    * - `#1811`_
      - enhancement
      - medium
      - Add waitUntil support for New Page and Go To keywords 
    * - `#2135`_
      - enhancement
      - medium
      - Enhance entry.py to allow for an additional package.json
    * - `#3019`_
      - enhancement
      - medium
      - 'Get Element By' cannot get element locator in iframe
    * - `#3203`_
      - enhancement
      - medium
      - Need a way to define the playwright-log.txt outputdir when using Browser in python
    * - `#1734`_
      - ---
      - medium
      - Better handling of `downloadPath` and better documentation. Adding of `saveAs` argument to `Download` keyword.
    * - `#1655`_
      - enhancement
      - low
      - [Feature] Add timeout argument to Wait For Alert
    * - `#3230`_
      - enhancement
      - ---
      - Add support for custom formatters. (lambda functions)
    * - `#3231`_
      - enhancement
      - ---
      - Added functionality to trigger multiple downloads at a time and not wait for them to finish
    * - `#3243`_
      - enhancement
      - ---
      - Remove ALL deprecated features. (`Click` etc)
    * - `#3252`_
      - enhancement
      - ---
      - Support Playwright 1.40 (TimeoutError became Error)

Altogether 32 issues. View on the `issue tracker <https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av18.0.0>`__.

.. _#2679: https://github.com/MarketSquare/robotframework-browser/issues/2679
.. _#2968: https://github.com/MarketSquare/robotframework-browser/issues/2968
.. _#3154: https://github.com/MarketSquare/robotframework-browser/issues/3154
.. _#3254: https://github.com/MarketSquare/robotframework-browser/issues/3254
.. _#1702: https://github.com/MarketSquare/robotframework-browser/issues/1702
.. _#3208: https://github.com/MarketSquare/robotframework-browser/issues/3208
.. _#3219: https://github.com/MarketSquare/robotframework-browser/issues/3219
.. _#2571: https://github.com/MarketSquare/robotframework-browser/issues/2571
.. _#2676: https://github.com/MarketSquare/robotframework-browser/issues/2676
.. _#3180: https://github.com/MarketSquare/robotframework-browser/issues/3180
.. _#3264: https://github.com/MarketSquare/robotframework-browser/issues/3264
.. _#395: https://github.com/MarketSquare/robotframework-browser/issues/395
.. _#1688: https://github.com/MarketSquare/robotframework-browser/issues/1688
.. _#2129: https://github.com/MarketSquare/robotframework-browser/issues/2129
.. _#2754: https://github.com/MarketSquare/robotframework-browser/issues/2754
.. _#3006: https://github.com/MarketSquare/robotframework-browser/issues/3006
.. _#3156: https://github.com/MarketSquare/robotframework-browser/issues/3156
.. _#3200: https://github.com/MarketSquare/robotframework-browser/issues/3200
.. _#3242: https://github.com/MarketSquare/robotframework-browser/issues/3242
.. _#3256: https://github.com/MarketSquare/robotframework-browser/issues/3256
.. _#1098: https://github.com/MarketSquare/robotframework-browser/issues/1098
.. _#1263: https://github.com/MarketSquare/robotframework-browser/issues/1263
.. _#1811: https://github.com/MarketSquare/robotframework-browser/issues/1811
.. _#2135: https://github.com/MarketSquare/robotframework-browser/issues/2135
.. _#3019: https://github.com/MarketSquare/robotframework-browser/issues/3019
.. _#3203: https://github.com/MarketSquare/robotframework-browser/issues/3203
.. _#1734: https://github.com/MarketSquare/robotframework-browser/issues/1734
.. _#1655: https://github.com/MarketSquare/robotframework-browser/issues/1655
.. _#3230: https://github.com/MarketSquare/robotframework-browser/issues/3230
.. _#3231: https://github.com/MarketSquare/robotframework-browser/issues/3231
.. _#3243: https://github.com/MarketSquare/robotframework-browser/issues/3243
.. _#3252: https://github.com/MarketSquare/robotframework-browser/issues/3252
.. _Foundation: https://robotframework.org/foundation/
