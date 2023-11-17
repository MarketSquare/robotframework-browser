*** Settings ***
Library         OperatingSystem
Resource        imports.resource

Suite Setup     Check Screenshots Before

Force Tags      slow

*** Test Cases ***
Failing With Screenshot 1
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: Error    Click    .nonexisting

Failing With Screenshot 2
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: Error    Click    .nonexisting2

Failing With Screenshot 3
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: Error    Click    .nonexisting3

Check Screenshots
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-1.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-2.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-3.png
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-4.png

*** Keywords ***
Check Screenshots Before
    Set Browser Timeout    3s    scope=Suite
    Remove File    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-1.png
    Remove File    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-2.png
    Remove File    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-3.png
    Remove File    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-4.png
