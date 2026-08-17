*** Settings ***
Documentation       Context B: Robot Framework imports only MyLibraryB, which owns the Browser
...                 instance and registers it as a listener. Browser is deliberately not imported
...                 anywhere in this suite; importing it would turn this into context A.
...                 Started as a child process by ../python_extension.robot, which asserts the exit
...                 code and inspects this run's output directory. One test is expected to fail.
...                 Tests are ordered pairs: `Test Scoped Timeout Is Reverted` and
...                 `Previous Page Was Auto Closed` observe what the test before them left behind.

Library             MyLibraryB.py

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

Run On Failure Does Not Take Screenshot
    [Documentation]    Expected to fail. Browser's `run_on_failure` lives in the dynamic library
    ...    API, which Robot Framework only calls on the library it imported itself. Registering the
    ...    listener does not bring it back, so no screenshot is left on disk.
    Open Login Page    ${LOGIN_URL}
    Click Missing Element
