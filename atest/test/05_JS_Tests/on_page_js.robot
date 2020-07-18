*** Settings ***
Resource          imports.resource
Suite Setup       New Browser
Test Setup        New Page    ${LOGIN_URL}
Suite Teardown    Close Browser

*** Test Cases ***
Results from page
    ${result}=    Execute Javascript on Page    "hello from page "+location.href
    should be equal    ${result}    hello from page http://localhost:7272/dist/
    ${result2}=    Execute Javascript on Page    1+2+3
    should be equal    ${result2}    ${6}
    ${result3}=    Execute Javascript on Page    1.3314*3.13432
    should be equal    ${result3}    ${4.173033648}

Page state
    Get page state    validate    value['a'] == 'HELLO FROM PAGE!' and value['b'] == 123

Localstorage
    Set To LocalStorage    mykey    myvalue
    Get From LocalStorage    mykey    ==    myvalue
    ${val}=    Execute Javascript on Page    window.localStorage.getItem("mykey")
    should be equal    ${val}    myvalue
    Remove From LocalStorage    mykey
    Get From LocalStorage    mykey    ==    ${None}

Sessionstorage
    Set To SessionStorage    mykey2    myvalue2
    Get From SessionStorage    mykey2    ==    myvalue2
    Remove From SessionStorage    mykey2
    Get From SessionStorage    mykey2    ==    ${None}

Localstorage clear
    Set To LocalStorage    key1    value1
    Set To LocalStorage    key2    value2
    Clear LocalStorage
    Get From LocalStorage    key1    ==    ${None}
    Get From LocalStorage    key2    ==    ${None}

Sessionstorage clear
    Set To SessionStorage    key1    value1
    Set To SessionStorage    key2    value2
    ${val1}=    Execute Javascript on Page    window.sessionStorage.getItem("key1")
    should be equal    ${val1}    value1
    Clear SessionStorage
    Get From SessionStorage    key1    ==    ${None}
    Get From SessionStorage    key2    ==    ${None}
