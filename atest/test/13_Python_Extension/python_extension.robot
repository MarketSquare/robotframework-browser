*** Settings ***
Documentation       Demonstrates the two ways a user's own Python library uses Browser, and pins
...                 what each one gets from Robot Framework. The demonstrations themselves are the
...                 suites and libraries in _child/, which run as child processes because Browser
...                 keeps class level state that every instance in a process shares. The leading
...                 underscore keeps _child/ out of the normal `inv atest` run.

Resource            ../variables.resource
Library             Process
Library             ../../library/child_result.py
Library             ../../library/os_wrapper.py

*** Variables ***
${CHILD_DIR} =      ${CURDIR}/_child

*** Test Cases ***
Context A Robot Framework Owns Browser
    [Documentation]    Robot Framework imports Browser and MyLibraryA sits alongside it. Everything
    ...    works, except that Browser keywords called from Python do not run `run_on_failure`.
    ${output} =    Run Child Suite    context_a    3
    ${result} =    Get Child Result    ${output}/output.xml
    Child Test Status Should Be    ${result}    Call Browser From Python    PASS
    Child Test Status Should Be    ${result}    Outputdir And Validate Work    PASS
    Child Test Status Should Be    ${result}    Set Test Scoped Timeout    PASS
    Child Test Status Should Be    ${result}    Test Scoped Timeout Is Reverted    PASS
    Child Test Status Should Be    ${result}    Open Page Without Closing It    PASS
    Child Test Status Should Be    ${result}    Previous Page Was Auto Closed    PASS
    Child Test Status Should Be
    ...    ${result}
    ...    Run On Failure Takes Screenshot
    ...    FAIL
    ...    this_element_does_not_exist
    Child Test Status Should Be
    ...    ${result}
    ...    Python Call Failure Takes No Screenshot
    ...    FAIL
    ...    this_element_does_not_exist
    Child Test Status Should Be
    ...    ${result}
    ...    Decorated Python Call Takes Screenshot
    ...    FAIL
    ...    this_element_does_not_exist
    Child Keyword Should Log
    ...    ${result}
    ...    Call Browser From Python
    ...    MyLibraryA
    ...    Clicks the element
    Screenshot Count Should Be    ${output}    fail-screenshot-*    1
    Screenshot Count Should Be    ${output}    my-library-failure-*    1
    Playwright Log Should Have Rf Context    ${output}/playwright-log.txt    Open Page Without Closing It

Context B Your Library Owns Browser
    [Documentation]    Robot Framework imports only MyLibraryB, which owns the Browser instance and
    ...    registers it as a listener. Automatic closing and scope settings come back with it,
    ...    `run_on_failure` does not.
    ${output} =    Run Child Suite    context_b    1
    ${result} =    Get Child Result    ${output}/output.xml
    Child Should Not Use Library    ${result}    Browser
    Child Test Status Should Be    ${result}    Call Browser From Python    PASS
    Child Test Status Should Be    ${result}    Outputdir And Validate Work    PASS
    Child Test Status Should Be    ${result}    Set Test Scoped Timeout    PASS
    Child Test Status Should Be    ${result}    Test Scoped Timeout Is Reverted    PASS
    Child Test Status Should Be    ${result}    Open Page Without Closing It    PASS
    Child Test Status Should Be    ${result}    Previous Page Was Auto Closed    PASS
    Child Test Status Should Be
    ...    ${result}
    ...    Run On Failure Does Not Take Screenshot
    ...    FAIL
    ...    this_element_does_not_exist
    Child Keyword Should Log
    ...    ${result}
    ...    Call Browser From Python
    ...    MyLibraryB
    ...    Clicks the element
    Screenshot Count Should Be    ${output}    fail-screenshot-*    0
    Playwright Log Should Have Rf Context    ${output}/playwright-log.txt    Open Page Without Closing It

Context B Without The Listener Registration
    [Documentation]    The same library with the `ROBOT_LIBRARY_LISTENER` line removed. Argument
    ...    conversion, `outputdir` and `validate` still work, because they only need a Robot
    ...    Framework run to exist. Automatic closing, scope settings and the Robot Framework
    ...    context on the node side are gone.
    ${output} =    Run Child Suite    context_b_no_listener    1
    ${result} =    Get Child Result    ${output}/output.xml
    Child Should Not Use Library    ${result}    Browser
    Child Test Status Should Be    ${result}    Call Browser From Python    PASS
    Child Test Status Should Be    ${result}    Outputdir And Validate Work    PASS
    Child Test Status Should Be    ${result}    Set Test Scoped Timeout    PASS
    Child Test Status Should Be    ${result}    Test Scoped Timeout Leaks To Next Test    PASS
    Child Test Status Should Be    ${result}    Open Page Without Closing It    PASS
    Child Test Status Should Be    ${result}    Previous Page Is Still Open    PASS
    Child Test Status Should Be
    ...    ${result}
    ...    Run On Failure Does Not Take Screenshot
    ...    FAIL
    ...    this_element_does_not_exist
    Child Keyword Should Log
    ...    ${result}
    ...    Call Browser From Python
    ...    MyLibraryB_no_listener
    ...    Clicks the element
    Screenshot Count Should Be    ${output}    fail-screenshot-*    0
    Playwright Log Should Not Have Rf Context    ${output}/playwright-log.txt

*** Keywords ***
Run Child Suite
    [Documentation]    Runs one suite from _child/ as its own process, with its own output
    ...    directory, and verifies the exit code. Robot Framework returns the number of failed
    ...    tests, so the expected code is not always zero.
    [Arguments]    ${suite}    ${expected_rc}
    VAR    ${output} =    ${OUTPUT_DIR}/${suite}
    ${robot_cmd} =    Get Robot Command
    ${env} =    Get Child Robot Environment
    ${process} =    Run Process
    ...    ${robot_cmd} --outputdir ${output} --loglevel DEBUG --report NONE --log NONE --variable LOGIN_URL:${LOGIN_URL} ${CHILD_DIR}/${suite}.robot
    ...    shell=True
    ...    env=${env}
    ...    timeout=150s
    ...    on_timeout=terminate
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    ${expected_rc}
    RETURN    ${output}

Screenshot Count Should Be
    [Arguments]    ${output}    ${pattern}    ${expected}
    ${count} =    Count Files    ${output}/browser/screenshot    ${pattern}
    Should Be Equal As Integers    ${count}    ${expected}
