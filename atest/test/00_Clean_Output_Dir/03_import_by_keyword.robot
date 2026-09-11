*** Settings ***
Documentation
...              If Variable \${initial_screenshot} not found, it means 01 failed before it could
...              publish the path as global variable. Nothing is wrong in this file; look at 01.
...              If error says \${second_screenshot} is not found, then look at 02.

Library          OperatingSystem
Resource         ../variables.resource

*** Test Cases ***
Take Screenshot
    Import Library    Browser    strict=${False}
    New Page    ${TABLES_URL}
    ${third_screenshot} =    Take Screenshot    third_screenshot    fullPage=True
    File Should Exist    ${third_screenshot}
    File Should Exist    ${initial_screenshot}
    File Should Exist    ${second_screenshot}
    [Teardown]    Close Browser    ALL
