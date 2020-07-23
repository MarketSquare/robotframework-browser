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
    localStorage set Item    mykey    myvalue
    localStorage get Item    mykey    ==    myvalue
    ${val}=    Execute Javascript on Page    window.localStorage.getItem("mykey")
    should be equal    ${val}    myvalue
    localStorage remove Item    mykey
    localStorage get Item    mykey    ==    ${None}

Sessionstorage
    sessionStorage set Item    mykey2    myvalue2
    sessionStorage get Item    mykey2    ==    myvalue2
    sessionStorage remove Item    mykey2
    sessionStorage get Item    mykey2    ==    ${None}

Localstorage clear
    localStorage set Item    key1    value1
    localStorage set Item    key2    value2
    localStorage clear
    localStorage get Item    key1    ==    ${None}
    localStorage get Item    key2    ==    ${None}

Sessionstorage clear
    sessionStorage set Item    key1    value1
    sessionStorage set Item    key2    value2
    ${val1}=    Execute Javascript on Page    window.sessionStorage.getItem("key1")
    should be equal    ${val1}    value1
    sessionStorage clear
    sessionStorage get Item    key1    ==    ${None}
    sessionStorage get Item    key2    ==    ${None}
