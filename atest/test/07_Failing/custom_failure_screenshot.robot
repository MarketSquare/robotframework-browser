*** Settings ***
Library         Browser    run_on_failure=Take Screenshot \ custom-fail
Library         OperatingSystem
Resource        imports.resource

Force Tags      slow

*** Test Cases ***
Failing With Custom Screenshot
    New Page    ${ERROR_URL}
    ${old_timeout} =    Set Browser Timeout    3s
    TRY
        Click    .nonexisting4
    EXCEPT    TimeoutError: locator.click: Timeout 3000ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    FINALLY
        Set Browser Timeout    ${old_timeout}
    END

Check Screenshot
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/custom-fail.png
