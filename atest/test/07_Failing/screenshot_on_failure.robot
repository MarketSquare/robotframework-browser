*** Settings ***
Library         Browser    timeout=3s
Library         OperatingSystem
Resource        imports.resource

Force Tags      slow

*** Test Cases ***
Failing With Screenshot 1
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting

Failing With Screenshot 2
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting2

Failing With Screenshot 3
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting3

Check Screenshots
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-1.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-2.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-3.png
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-4.png
