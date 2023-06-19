*** Settings ***
Library         Browser    run_on_failure=Take Screenshot \ custom-fail    timeout=3s
Library         OperatingSystem
Resource        imports.resource

Force Tags      slow

*** Test Cases ***
Failing With Custom Screenshot
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting4

Check Screenshot
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/custom-fail.png
