*** Settings ***
Library     Browser    timeout=3s
Library     OperatingSystem
Resource    imports.resource

*** Test Cases ***
Failing with screenshot 1
    [Documentation]    FAIL STARTS: TimeoutError
    New Page    ${ERROR_URL}
    Click    .nonexisting

Failing with screenshot 2
    [Documentation]    FAIL STARTS: TimeoutError
    New Page    ${ERROR_URL}
    Click    .nonexisting2

Failing with screenshot 3
    [Documentation]    FAIL STARTS: TimeoutError
    New Page    ${ERROR_URL}
    Click    .nonexisting3

Check screenshots
    file should exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-1.png
    file should exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-2.png
    file should exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-3.png
    file should not exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-4.png
