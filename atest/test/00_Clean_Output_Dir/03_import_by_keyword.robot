*** Settings ***
Library     OperatingSystem
Resource    ../variables.resource

*** Test Cases ***
Take Screenshot
    Import Library    Browser    strict=${False}
    New Page    ${TABLES_URL}
    ${third_screenshot} =    Take Screenshot    third_screenshot    fullPage=True
    File Should Exist    ${third_screenshot}
    File Should Exist    ${initial_screenshot}
    File Should Exist    ${second_screenshot}
    [Teardown]    Close Browser    ALL
