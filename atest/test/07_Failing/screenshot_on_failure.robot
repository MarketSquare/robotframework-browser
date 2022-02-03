*** Settings ***
Library     Browser    timeout=3s
Library     OperatingSystem
Resource    imports.resource

*** Test Cases ***
Failing with screenshot 1
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting

Failing with screenshot 2
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting2

Failing with screenshot 3
    New Page    ${ERROR_URL}
    Run Keyword And Expect Error    STARTS: TimeoutError    Click    .nonexisting3

Check screenshots
    file should exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-1.png
    file should exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-2.png
    file should exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-3.png
    file should not exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-4.png
