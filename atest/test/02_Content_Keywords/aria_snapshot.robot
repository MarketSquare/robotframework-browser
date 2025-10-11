*** Settings ***
Resource        imports.resource

Suite Setup     Aria Snapshot Setup

*** Test Cases ***
Aria Snapshot YAML
    ${snapshot} =    Get Aria Snapshot    h1
    Should Be Equal    ${snapshot}    - heading "Login Page" [level=1]
    ${snapshot} =    Get Aria Snapshot    id=username_field    yaml    ==    - textbox "User Name:"
    ${snapshot} =    Get Aria Snapshot    id=username_field    yaml    contains    User Name

Aria Snapshot Dict
    ${snapshot} =    Get Aria Snapshot    h1    dict
    Should Be Equal    ${snapshot}    ['heading "Login Page" [level=1]']    type=list
    VAR    @{expected}    textbox "User Name:"
    ${snapshot} =    Get Aria Snapshot    id=username_field    dict    ==    ${expected}

Aria Snapshot Strict Mode
    ${strict} =    Set Strict Mode    True
    TRY
        Get Aria Snapshot    //input
    EXCEPT    *strict mode violation*    type=glob
        Log    Caught expected PlaywrightError in strict mode.
    END
    Set Strict Mode    False
    ${snapshot} =    Get Aria Snapshot    //input    yaml    ==    - textbox "User Name:"
    [Teardown]    Set Strict Mode    ${strict}

Aria Snapshot Non-existing Element
    TRY
        Get Aria Snapshot    id=non_existing_element
    EXCEPT    *locator.ariaSnapshot: Timeout*    type=glob
        Log    Caught expected PlaywrightError for non-existing element.
    END

*** Keywords ***
Aria Snapshot Setup
    Ensure Open Page    ${LOGIN_URL}
