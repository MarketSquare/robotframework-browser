*** Settings ***
Resource            imports.resource

Suite Setup         New Browser
Suite Teardown      Close Browser
Test Setup          New Page    ${LOGIN_URL}

*** Test Cases ***
Localstorage
    LocalStorage Set Item    mykey    myvalue
    LocalStorage Get Item    mykey    ==    myvalue
    ${val} =    Execute Javascript    window.localStorage.getItem("mykey")
    Should Be Equal    ${val}    myvalue
    LocalStorage Remove Item    mykey
    LocalStorage Get Item    mykey    ==    ${None}

Sessionstorage
    SessionStorage Set Item    mykey2    myvalue2
    SessionStorage Get Item    mykey2    ==    myvalue2
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

Sessionstorage Clear
    SessionStorage Set Item    key1    value1
    SessionStorage Set Item    key2    value2
    ${val1} =    Execute Javascript    window.sessionStorage.getItem("key1")
    Should Be Equal    ${val1}    value1
    SessionStorage Clear
    SessionStorage Get Item    key1    ==    ${None}
    SessionStorage Get Item    key2    ==    ${None}
