*** Settings ***
Library     Browser    retry_assertions_for=4 sec
Library     OperatingSystem
Resource    ../variables.resource

*** Test Cases ***
Take Screenshot
    New Page    ${TABLES_URL}
    ${second_screenshot} =    Take Screenshot    second_screenshot    fullPage=True
    Set Global Variable    ${second_screenshot}
    File Should Exist    ${second_screenshot}
    File Should Exist    ${initial_screenshot}
    [Teardown]    Close Browser    ALL
