*** Settings ***
Library         Browser    run_on_failure=Take Screenshot \ custom-fail    timeout=3s
Library         OperatingSystem
Resource        imports.resource

Force Tags      slow

*** Test Cases ***
Failing With Custom Screenshot
    New Page    ${ERROR_URL}
    TRY
        Click    .nonexisting4
    EXCEPT    TimeoutError: locator.click: Timeout 3000ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END

Check Screenshot
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/custom-fail.png
