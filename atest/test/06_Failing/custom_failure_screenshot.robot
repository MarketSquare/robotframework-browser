*** Settings ***
Library     Browser    run_on_failure=Take Screenshot \ custom-fail    timeout=3s
Library     OperatingSystem
Resource    imports.resource
Suite Teardown    Register Keyword To Run On Failure    None

*** Test Cases ***
Failing with custom screenshot
    [Documentation]    FAIL STARTS: TimeoutError
    New Page    ${ERROR_URL}
    Click    .nonexisting4

Check screenshot
    file should exist    ${OUTPUT DIR}/browser/screenshot/custom-fail.png
