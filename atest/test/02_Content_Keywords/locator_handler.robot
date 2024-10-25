*** Settings ***
Resource            imports.resource

Suite Setup         Overlay Suite Setup
Suite Teardown      Overlay Suite Teardown
Test Setup          New Page    ${OWERLAY_URL}

*** Test Cases ***
Overlay Should Be Closed Automatically
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
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

Overlay Should Be Closed Automatically On Page Where It Is Given
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
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
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
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
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
    Click    id=CreateOverlayButton
    Click    id=textHeading
    Remove Locator Handler    id=overlay
    Remove Locator Handler    id=overlay
    Click    id=CreateOverlayButton
    TRY
        Click    id=CreateOverlayButton
    EXCEPT    TimeoutError: locator.click: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Adding Locator Handler With All Args Should Work
    Add Locator Handler Click
    ...    id=overlay
    ...    id=OverlayCloseButton
    ...    times=1
    ...    noWaitAfter=True
    ...    click_clickCount=1
    ...    click_delay=0.1
    ...    click_force=True
    Click    id=CreateOverlayButton    # Overlay is displayed
    Click    id=CreateOverlayButton    # Overlay should be closed
    TRY
        Click    id=CreateOverlayButton    # Overlay should not be closed because times=1
    EXCEPT    TimeoutError: locator.click: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Add Custom Locator Handler For Click
    VAR    &{handler_spec}    action=click    selector=id=OverlayCloseButton
    Add Locator Handler Custom    id=overlay    [${handler_spec}]
    Click    id=CreateOverlayButton    # Overlay is displayed
    Click    id=textHeading    # Overlay should be closed
    Remove Locator Handler    id=overlay
    VAR    &{handler_spec}
    ...    action=click
    ...    selector=id=OverlayCloseButton
    ...    button=left
    ...    clickCount=${1}
    ...    delay=${0.1}
    ...    force=${True}
    Add Locator Handler Custom    id=overlay    [${handler_spec}]
    Click    id=CreateOverlayButton    # Overlay is displayed
    Click    id=textHeading    # Overlay should be closed

Add Custom Locator Handler With Click Check Fill And Uncheck
    VAR    &{handler_spec_check}
    ...    action=CHECK    # Case of action does not matter
    ...    selector=id=overlayCheckbox
    ...    force=${True}
    ...    timeout=${4}
    VAR    &{handler_spec_fill}
    ...    action=Fill
    ...    selector=id=overlayInput
    ...    value=This is a value
    ...    force=${True}
    ...    timeout=${4}
    VAR    &{handler_spec_uncheck}
    ...    action=uncheck
    ...    selector=id=overlayCheckbox
    ...    force=${True}
    ...    timeout=${4}
    VAR    &{handler_spec_click}
    ...    action=click
    ...    selector=id=OverlayCloseButton
    ...    button=left
    ...    clickCount=${1}
    ...    delay=${0.1}
    ...    force=${True}
    Add Locator Handler Custom
    ...    id=overlay
    ...    [${handler_spec_check}, ${handler_spec_fill}, ${handler_spec_uncheck}, ${handler_spec_click}]
    Click    id=CreateOverlayButton    # Overlay is displayed
    Click    id=textHeading    # Overlay should be closed

Adding Custom Locator Handler With Wrong Order Does Not Fail
    [Documentation]    This test will pass because if the handler will fail whole NodeJS grpc server would close.
    VAR    &{handler_spec_click}
    ...    action=click
    ...    selector=id=OverlayCloseButton
    ...    button=left
    ...    clickCount=${1}
    ...    delay=${0.1}
    ...    force=${True}
    VAR    &{handler_spec_check}
    ...    action=CHECK
    ...    selector=id=overlayCheckbox
    ...    force=${True}
    ...    timeout=${4}
    Add Locator Handler Custom
    ...    id=overlay
    ...    [${handler_spec_click}, ${handler_spec_check} ]
    Click    id=CreateOverlayButton    # Overlay is displayed
    Click    id=textHeading    # Overlay should be closed

Adding Custom Locator Handler Fill Without Value Shuld Fail
    VAR    &{handler_spec_fill}
    ...    action=Fill
    ...    selector=id=overlayInput
    ...    force=${True}
    ...    timeout=${4}
    TRY
        Add Locator Handler Custom
        ...    id=overlay
        ...    [${handler_spec_fill}]
    EXCEPT    ValueError: Value must be defined for fill action    AS    ${error}
        Log    All OK with error ${error}
    END

Add Custom Locator Handler Which Is Not Fill But Constains Value Should Fail
    VAR    &{handler_spec_click}
    ...    action=click
    ...    selector=id=OverlayCloseButton
    ...    value=Should not be here
    ...    button=left
    ...    clickCount=${1}
    ...    delay=${0.1}
    ...    force=${True}
    TRY
        Add Locator Handler Custom
        ...    id=overlay
        ...    [${handler_spec_click}]
    EXCEPT    ValueError: Value must not be defined for action other than fill    AS    ${error}
        Log    All OK with error ${error}
    END

Adding Custom Locator Handler Without Action Should Fail
    VAR    &{handler_spec_click}
    ...    selector=id=OverlayCloseButton
    ...    value=Should not be here
    ...    button=left
    ...    clickCount=${1}
    ...    delay=${0.1}
    ...    force=${True}
    TRY
        Add Locator Handler Custom
        ...    id=overlay
        ...    [${handler_spec_click}]
    EXCEPT    ValueError: Action must be defined in the handler specification*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Adding Custom Locator Handler Without Selector Should Fail
    VAR    &{handler_spec_click}
    ...    action=click
    ...    button=left
    ...    clickCount=${1}
    ...    delay=${0.1}
    ...    force=${True}
    TRY
        Add Locator Handler Custom
        ...    id=overlay
        ...    [${handler_spec_click}]
    EXCEPT    ValueError: Selector must be defined in the handler specification*    type=GLOB    AS    ${error}
        Log    All OK with error ${error}
    END

Adding Custom Locator Handler Wiht Invalid Action Should Fail
    VAR    &{handler_spec_click}
    ...    action=INVALID
    ...    selector=id=OverlayCloseButton
    ...    button=left
    ...    clickCount=${1}
    ...    delay=${0.1}
    ...    force=${True}
    TRY
        Add Locator Handler Custom
        ...    id=overlay
        ...    [${handler_spec_click}]
    EXCEPT    ValueError: Action was INVALID, it must be one of the following: click, fill, check, uncheck    AS    ${error}
        Log    All OK with error ${error}
    END

*** Keywords ***
Overlay Suite Setup
    ${TIMEOUT} =    Set Browser Timeout    0.5s
    VAR    ${TIMEOUT}    ${TIMEOUT}    scope=SUITE

Overlay Suite Teardown
    Set Browser Timeout    ${TIMEOUT}
