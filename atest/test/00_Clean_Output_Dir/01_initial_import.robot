*** Settings ***
Library     Browser    retry_assertions_for=2 sec
Library     OperatingSystem
Resource    ../variables.resource

*** Test Cases ***
Take Screenshot
    New Page    ${TABLES_URL}
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/initial_screenshot.png
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/second_screenshot.png
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/third_screenshot.png
    ${initial_screenshot} =    Take Screenshot    initial_screenshot    fullPage=True
    Set Global Variable    ${initial_screenshot}
    File Should Exist    ${initial_screenshot}
    [Teardown]    Close Browser    ALL
