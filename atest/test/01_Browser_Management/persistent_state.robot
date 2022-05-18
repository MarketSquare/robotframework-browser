*** Settings ***
Resource    imports.resource

*** Test Cases ***
New Persistent Context creates a browser and a context
    New Persistent Context

    ${browser_id} =    Switch Browser    CURRENT
    Should Not Be Equal    ${browser_id}    NO CONTEXT OPEN
    ${context_id} =    Switch Context    CURRENT
    Should Not Be Equal    ${context_id}    NO CONTEXT OPEN

Switching Between Two persistent contexts works
    Get Browser Catalog
    ${context_1}  New Persistent Context
    Get Browser Catalog
    ${context_2}  New Persistent Context
    Get Browser Catalog

    ${switch_id} =    Switch Context    ${context_1}
    Should Be Equal    ${context_2}  ${switch_id}
    ${switch_id} =    Switch Context    ${context_2}
    Should Be Equal    ${context_1}  ${switch_id}

# Close Page switches active page
#     [Tags]    slow
#     New Page Login
#     New Page Form
#     Close Page
#     Get Title    matches    (?i)login

New Context fails with persistent context
    New Persistent Context
    Run Keyword And Expect Error    WRONG_ERROR  New Context  
