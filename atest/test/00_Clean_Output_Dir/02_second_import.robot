*** Settings ***
Documentation
...              If Variable \${initial_screenshot} not found, it means 01 failed before it could
...              publish the path as global variable. Nothing is wrong in this file; look at 01.

Library          Browser    retry_assertions_for=4 sec
Library          OperatingSystem
Resource         ../variables.resource

*** Test Cases ***
Take Screenshot
    New Page    ${TABLES_URL}
    ${second_screenshot} =    Take Screenshot    second_screenshot    fullPage=True
    VAR    ${second_screenshot} =    ${second_screenshot}    scope=GLOBAL
    File Should Exist    ${second_screenshot}
    File Should Exist    ${initial_screenshot}
    [Teardown]    Close Browser    ALL
