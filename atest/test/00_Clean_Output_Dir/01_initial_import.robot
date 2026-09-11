*** Settings ***
Library     Browser    retry_assertions_for=2 sec
Library     OperatingSystem
Resource    ../variables.resource

*** Test Cases ***
Test Lazy Playwright Loading
    [Documentation]    Tests that Playwright is not loaded until the first keyword is called
    ${browser_lib} =    Get Library Instance    Browser
    Should Be True    $browser_lib._playwright is None
    ${cat} =    Get Browser Catalog
    Should Be True    isinstance($browser_lib._playwright, Browser.playwright.Playwright)

Take Screenshot
    New Page    ${TABLES_URL}
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/initial_screenshot.png
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/second_screenshot.png
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/third_screenshot.png
    # Wait For Elements State done because without it the first capture is fail randomly on mac
    Wait For Elements State    ${SELECTOR_PREFIX_SPACED}id=table1    stable
    ${initial_screenshot} =    Take Screenshot    initial_screenshot    fullPage=True
    VAR    ${initial_screenshot} =    ${initial_screenshot}    scope=GLOBAL
    File Should Exist    ${initial_screenshot}
    [Teardown]    Close Browser    ALL
