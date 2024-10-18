*** Settings ***
Resource            imports.resource

Suite Setup         Overlay Suite Setup
Suite Teardown      Overlay Suite Teardown
Test Setup          Overlay Setup

*** Test Cases ***
Overlay Should Be Closed Automatically
    Add Locator Handler    id=overlay    id=OverlayCloseButton
    Click    id=CreateOverlayButton
    Click    id=CreateOverlayButton
    Click    id=textHeading
    Get Element States    id=overlay    validate    value & hidden
    Get Element Count    id=overlay    ==    1

If Overlay Not Set Click Should Fail
    Click    id=CreateOverlayButton
    TRY
        Click    id=CreateOverlayButton
    EXCEPT    TimeoutError: locator.click: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Both Position X And Position Y Must Be Given
    TRY
        Add Locator Handler    id=OverlayOffButton    click_locator=id=OverlayButton    position_x=3    position_y=None
    EXCEPT    ValueError: Both position_x and position_y must be given*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Overlay Should Be Closed Automatically On Page Where It Is Given
    Add Locator Handler    id=overlay    id=OverlayCloseButton
    Click    id=CreateOverlayButton
    Click    id=textHeading
    Get Element States    id=overlay    validate    value & hidden
    Get Element Count    id=overlay    ==    1
    New Page    ${OWERLAY_URL}
    Click    id=CreateOverlayButton
    TRY
        Click    id=CreateOverlayButton
    EXCEPT    TimeoutError: locator.click: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Removing Locator Handler Should Not Fail If It Does Not Exist
    Remove Locator Handler    id=DoesNotExist

Removing Locator Handler Should Leave Overlay Open
    Add Locator Handler    id=overlay    id=OverlayCloseButton
    Click    id=CreateOverlayButton
    Click    id=textHeading
    Remove Locator Handler    id=overlay
    Click    id=CreateOverlayButton
    TRY
        Click    id=CreateOverlayButton
    EXCEPT    TimeoutError: locator.click: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Adding Same Locator Handler Should Work
    Add Locator Handler    id=overlay    id=OverlayCloseButton
    Add Locator Handler    id=overlay    id=OverlayCloseButton
    Add Locator Handler    id=overlay    id=OverlayCloseButton
    Click    id=CreateOverlayButton
    Click    id=textHeading
    Remove Locator Handler    id=overlay
    Click    id=CreateOverlayButton
    TRY
        Click    id=CreateOverlayButton
    EXCEPT    TimeoutError: locator.click: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

*** Keywords ***
Overlay Suite Setup
    ${TIMEOUT} =    Set Browser Timeout    0.5s
    VAR    ${TIMEOUT}    ${TIMEOUT}    scope=SUITE

Overlay Setup
    New Page    ${OWERLAY_URL}

Overlay Suite Teardown
    Set Browser Timeout    ${TIMEOUT}
