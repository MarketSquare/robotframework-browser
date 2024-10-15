*** Settings ***
Resource            imports.resource

Suite Teardown      Overlay Suite Teardown
Test Setup          Overlay Setup

*** Test Cases ***
Overlay Should Be Closed Automatically
    Add Locator Handler    id=OverlayOffButton    click_locator=id=OverlayButton
    Click    id=CreateOverlayButton
    Click    id=CreateOverlayButton
    Get Element Count    id=OverlayButton    ==    1

If Overlay Not Set Click Should Fail
    Click    id=CreateOverlayButton
    TRY
        Click    id=CreateOverlayButton
    EXCEPT    TimeoutError: locator.click: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

*** Keywords ***
Overlay Setup
    New Page    ${OWERLAY_URL}
    ${TIMEOUT} =    Set Browser Timeout    0.5s
    VAR    ${TIMEOUT}    ${TIMEOUT}    scope=SUITE

Overlay Suite Teardown
    Set Browser Timeout    ${TIMEOUT}
