*** Settings ***
Documentation       Context B without the listener registration. Identical to context_b.robot
...                 except for the library it imports and the two tests that observe the
...                 difference: the test scoped timeout leaks and the page stays open.
...                 Started as a child process by ../python_extension.robot, which asserts the exit
...                 code and inspects this run's output directory. One test is expected to fail.

Library             MyLibraryB_no_listener.py

Suite Teardown      Close Browser Library

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
    [Documentation]    Browser never learns that a test started, so `scope=Test` is silently
    ...    downgraded to `Global` instead of failing.
    ${previous} =    Set Test Scoped Browser Timeout    3 seconds
    Should Be Equal    ${previous}    10 seconds

Test Scoped Timeout Leaks To Next Test
    ${previous} =    Set Browser Timeout And Return Previous    4 seconds
    Should Be Equal    ${previous}    3 seconds

Open Page Without Closing It
    [Documentation]    Three pages are open, not one: the pages opened by the first two tests were
    ...    never closed either. With the listener registered this count is always one.
    Open Login Page    ${LOGIN_URL}
    ${pages} =    Get Open Page Count
    Should Be Equal As Integers    ${pages}    3

Previous Page Is Still Open
    ${pages} =    Get Open Page Count
    Should Be Equal As Integers    ${pages}    3

Run On Failure Does Not Take Screenshot
    [Documentation]    Expected to fail. No screenshot is left on disk, for the same reason as in
    ...    context_b.robot.
    Open Login Page    ${LOGIN_URL}
    Click Missing Element
