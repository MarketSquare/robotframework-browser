*** Settings ***
Documentation    Context A: Robot Framework imports Browser and MyLibraryA sits alongside it.
...              Started as a child process by ../python_extension.robot, which asserts the exit
...              code and inspects this run's output directory. Three tests are expected to fail.
...              Tests are ordered pairs: `Test Scoped Timeout Is Reverted` and
...              `Previous Page Was Auto Closed` observe what the test before them left behind.

Library          Browser    enable_playwright_debug=${True}
Library          MyLibraryA.py

*** Test Cases ***
Call Browser From Python
    Open Login Page    ${LOGIN_URL}
    ${result} =    Click Heading With Middle Mouse Button
    Should Be Equal    ${result}    evaluated

Outputdir And Validate Work
    Open Login Page    ${LOGIN_URL}
    ${outputdir} =    Get Browser Output Directory
    Should Be Equal    ${outputdir}    ${OUTPUT_DIR}
    ${texts} =    Get Heading With Validate And Then
    Should Be Equal    ${texts}[0]    Login Page
    Should Be Equal    ${texts}[1]    LOGIN PAGE

Set Test Scoped Timeout
    ${previous} =    Set Test Scoped Browser Timeout    3 seconds
    Should Be Equal    ${previous}    10 seconds

Test Scoped Timeout Is Reverted
    ${previous} =    Set Browser Timeout And Return Previous    4 seconds
    Should Be Equal    ${previous}    10 seconds

Open Page Without Closing It
    Open Login Page    ${LOGIN_URL}
    ${pages} =    Get Open Page Count
    Should Be Equal As Integers    ${pages}    1

Previous Page Was Auto Closed
    ${pages} =    Get Open Page Count
    Should Be Equal As Integers    ${pages}    0

Run On Failure Takes Screenshot
    [Documentation]    Expected to fail. The keyword is called by Robot Framework, so Browser
    ...    runs its `run_on_failure` keyword and leaves a screenshot on disk.
    Open Login Page    ${LOGIN_URL}
    Click    id=this_element_does_not_exist

Python Call Failure Takes No Screenshot
    [Documentation]    Expected to fail. The very same Browser keyword, called from Python by
    ...    MyLibraryA, never enters Browser's `run_on_failure` and leaves no screenshot.
    Open Login Page    ${LOGIN_URL}
    Click Missing Element

Decorated Python Call Takes Screenshot
    [Documentation]    Expected to fail. MyLibraryA takes the screenshot itself with a decorator,
    ...    which is how a small library recovers what the previous test lost.
    Open Login Page    ${LOGIN_URL}
    Click Missing Element With Screenshot
