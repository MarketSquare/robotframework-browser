*** Settings ***
Resource          imports.resource
Test Setup        Create Page    ${LOGIN_URL}
Test Teardown     Close Browser

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
    Local Storage Set    mykey    myvalue
    Local Storage Get    mykey    ==    myvalue
    ${val}=    Execute Javascript on Page    window.localStorage.getItem("mykey")
    should be equal    ${val}    myvalue
    Local Storage Remove    mykey
    Local Storage Get    mykey    ==    ${None}

Sessionstorage
    Session Storage Set    mykey2    myvalue2
    Session Storage Get    mykey2    ==    myvalue2
    Session Storage Remove    mykey2
    Session Storage Get    mykey2    ==    ${None}

Localstorage clear
    Local Storage Set    key1    value1
    Local Storage Set    key2    value2
    Local Storage Clear
    Local Storage Get    key1    ==    ${None}
    Local Storage Get    key2    ==    ${None}

Sessionstorage clear
    Session Storage Set    key1    value1
    Session Storage Set    key2    value2
    ${val1}=    Execute Javascript on Page    window.sessionStorage.getItem("key1")
    should be equal    ${val1}    value1
    Session Storage Clear
    Session Storage Get    key1    ==    ${None}
    Session Storage Get    key2    ==    ${None}
