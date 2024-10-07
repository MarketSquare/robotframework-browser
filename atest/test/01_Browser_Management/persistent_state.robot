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
    ${browser_1}    ${context_1}    ${page_1} =    New Persistent Context    url=${LOGIN_URL}
    Get Browser Catalog
    ${url_1} =    Get Url
    ${title_1} =    Get Title

    ${browser_2}    ${context_2}    ${page_2} =    New Persistent Context    url=${FORM_URL}
    Get Browser Catalog
    ${url_2} =    Get Url
    ${title_2} =    Get Title

    Should Be Equal    ${browser_1}    ${browser_2}

    Switch Context    ${context_1}
    Get URL    ==    ${url_1}
    Get Title    ==    ${title_1}
    ${switch_id} =    Switch Context    CURRENT
    Should Be Equal    ${context_1}    ${switch_id}

    Switch Context    ${context_2}
    Get URL    ==    ${url_2}
    Get Title    ==    ${title_2}
    ${switch_id} =    Switch Context    CURRENT
    Should Be Equal    ${context_2}    ${switch_id}

    Close Context
    Close Context

New Context Fails With Persistent Context
    New Persistent Context
    Run Keyword And Expect Error
    ...    Error: Trying to create a new context when a persistentContext is active
    ...    New Context

New Persistent Context Can Use An URL
    Close Browser    ALL
    New Persistent Context    url=${WELCOME_URL}
    Get Url    ==    ${WELCOME_URL}

New Persistent Context Creates An Empty Page
    Close Browser    ALL
    New Persistent Context
    ${catalog} =    Get Browser Catalog
    Get Title    ==    ${EMPTY}
    Get Url    ==    about:blank

New Persistent Context Open New Pages
    ${old} =    Set Retry Assertions For    5s
    Close Browser    ALL
    New Persistent Context    url=${WELCOME_URL}
    Click    "Open html"
    Get Browser Catalog    validate    len(value[0]['contexts'][0]['pages']) == 2
    Get Url    ==    ${WELCOME_URL}
    Switch Page    NEW
    Get Url    ==    ${ERROR_URL}
    [Teardown]    Set Retry Assertions For    ${old}

New Persistent Context Cleaned Up After Timeout
    [Tags]    slow
    [Setup]    Close Browser    ALL
    Set Browser Timeout    1s    Test
    ${catalog_1} =    Get Browser Catalog
    TRY
        New Persistent Context    url=${SLOW_PAGE}    timeout=1s
    EXCEPT    *Timeout*    type=GLOB
        ${catalog_2} =    Get Browser Catalog
        Should Be Equal    ${catalog_1}    ${catalog_2}
    END
    New Browser
    New Page    url=${ERROR_URL}
    Get Title    ==    Error Page
    New Persistent Context    url=${WELCOME_URL}
    Get Title    ==    Welcome Page
    ${catalog_3} =    Get Browser Catalog
    TRY
        New Persistent Context    url=${SLOW_PAGE}    timeout=1s
    EXCEPT    type=GLOB
        ${catalog_4} =    Get Browser Catalog
        Should Be Equal    ${catalog_3}    ${catalog_4}
    END
    Get Title    ==    Welcome Page
