*** Settings ***
Resource            imports.resource

Suite Teardown      Close Browser    ALL

*** Test Cases ***
New Persistent Context Creates A Browser And A Context
    New Persistent Context

    ${browser_id} =    Switch Browser    CURRENT
    Should Not Be Equal    ${browser_id}    NO CONTEXT OPEN
    ${context_id} =    Switch Context    CURRENT
    Should Not Be Equal    ${context_id}    NO CONTEXT OPEN

    Close Context

Switching Between Two Persistent Contexts Works
    Get Browser Catalog
    ${context_1} =    New Persistent Context
    New Page    ${LOGIN_URL}
    Click    id=login_button

    ${browser_1} =    Switch Browser    CURRENT
    Get Browser Catalog
    ${context_2} =    New Persistent Context
    ${browser_2} =    Switch Browser    CURRENT
    Get Browser Catalog

    Switch Browser    ${browser_1}
    ${switch_id} =    Switch Context    CURRENT
    Should Be Equal    ${context_1}    ${switch_id}
    Switch Browser    ${browser_2}
    ${switch_id} =    Switch Context    CURRENT
    Should Be Equal    ${context_2}    ${switch_id}

    Close Context
    Close Context

New Context Fails With Persistent Context
    New Persistent Context
    Run Keyword And Expect Error
    ...    Error: Trying to create a new context when a persistentContext is active
    ...    New Context
