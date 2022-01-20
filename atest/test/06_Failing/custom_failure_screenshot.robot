*** Settings ***
Library     Browser    run_on_failure=Take Screenshot \ custom-fail    timeout=3s
Library     OperatingSystem
Resource    imports.resource

*** Test Cases ***
Failing with custom screenshot
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting4

Check screenshot
    file should exist    ${OUTPUT DIR}/browser/screenshot/custom-fail.png
