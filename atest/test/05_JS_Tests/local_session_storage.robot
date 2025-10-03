*** Settings ***
Resource            imports.resource

Suite Setup         New Browser    headless=${HEADLESS}
Suite Teardown      Close Browser
Test Setup          New Page    ${LOGIN_URL}

*** Test Cases ***
Localstorage
    LocalStorage Set Item    mykey    myvalue
    LocalStorage Get Item    mykey    ==    myvalue
    ${val} =    Evaluate Javascript    ${None}    window.localStorage.getItem("mykey")
    Should Be Equal    ${val}    myvalue
    LocalStorage Remove Item    mykey
    LocalStorage Get Item    mykey    ==    ${None}

Sessionstorage
    SessionStorage Set Item    mykey2    my"v'a `\${test}`lue2
    SessionStorage Get Item    mykey2    ==    my"v'a `\${test}`lue2
    SessionStorage Remove Item    mykey2
    SessionStorage Get Item    mykey2    ==    ${None}

Sessionstorage Clear
    SessionStorage Set Item    mykey2    myvalue2
    SessionStorage Set Item    mykey3    myvalue3
    SessionStorage Clear
    SessionStorage Get Item    mykey2    ==    ${None}
    SessionStorage Get Item    mykey3    ==    ${None}

Localstorage Clear
    LocalStorage Set Item    key1    value1
    LocalStorage Set Item    key2    value2
    LocalStorage Clear
    LocalStorage Get Item    key1    ==    ${None}
    LocalStorage Get Item    key2    ==    ${None}

Sessionstorage Clear 2
    SessionStorage Set Item    key1    val"ue1
    SessionStorage Set Item    key2    val'ue2
    ${val1} =    Evaluate JavaScript    ${None}    window.sessionStorage.getItem("key1")
    Should Be Equal    ${val1}    val"ue1
    SessionStorage Clear
    SessionStorage Get Item    key1    ==    ${None}
    SessionStorage Get Item    key2    ==    ${None}

LocalStorage In Frame
    [Tags]    no-docker-pr
    [Setup]    New Page    http://localhost:${SERVER_PORT}/framing.html?url=http://127.0.0.1:${SERVER_PORT}/prefilled_email_form.html
    LocalStorage Set Item    key    value_of_main_page
    LocalStorage Set Item    key_two    value_of_main_page_two
    LocalStorage Get Item    key    ==    value_of_main_page
    LocalStorage Get Item    key    ==    ${None}    LStore:    frame_selector=iframe >>> body
    LocalStorage Set Item    key    value_of_frame    iframe >>> body
    LocalStorage Set Item    key_two    value_of_frame_two    iframe >>> body
    LocalStorage Get Item    key    ==    value_of_frame    frame_selector=iframe >>> body
    LocalStorage Get Item    key_two    ==    value_of_frame_two    frame_selector=iframe >>> body
    LocalStorage Remove Item    key_two    iframe >>> body
    LocalStorage Get Item    key_two    ==    ${None}    frame_selector=iframe >>> body
    LocalStorage Get Item    key_two    ==    value_of_main_page_two
    LocalStorage Clear    iframe >>> body
    LocalStorage Get Item    key    ==    ${None}    frame_selector=iframe >>> body
    LocalStorage Get Item    key    ==    value_of_main_page

SessionStorage In Frame
    [Tags]    no-docker-pr
    [Setup]    New Page    http://localhost:${SERVER_PORT}/framing.html?url=http://127.0.0.1:${SERVER_PORT}/prefilled_email_form.html
    SessionStorage Set Item    key    value_of_main_page_session
    SessionStorage Set Item    key_two    value_of_main_page_session_two
    SessionStorage Get Item    key    ==    value_of_main_page_session
    SessionStorage Get Item    key    ==    ${None}    SStore:    frame_selector=iframe >>> body
    SessionStorage Set Item    key    value_of_frame_session    iframe >>> body
    SessionStorage Set Item    key_two    value_of_frame_session_two    iframe >>> body
    SessionStorage Get Item    key    ==    value_of_frame_session    frame_selector=iframe >>> body
    SessionStorage Get Item    key_two    ==    value_of_frame_session_two    frame_selector=iframe >>> body
    SessionStorage Remove Item    key_two    iframe >>> body
    SessionStorage Get Item    key_two    ==    ${None}    frame_selector=iframe >>> body
    SessionStorage Get Item    key_two    ==    value_of_main_page_session_two
    SessionStorage Clear    iframe >>> body
    SessionStorage Get Item    key    ==    ${None}    frame_selector=iframe >>> body
    SessionStorage Get Item    key    ==    value_of_main_page_session
