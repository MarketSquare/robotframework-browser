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
    localStorage set    mykey    myvalue
    localStorage get    mykey    ==    myvalue
    ${val}=    Execute Javascript on Page    window.localStorage.getItem("mykey")
    should be equal    ${val}    myvalue
    localStorage remove    mykey
    localStorage get   mykey    ==    ${None}

Sessionstorage
    sessionStorage set    mykey2    myvalue2
    sessionStorage get    mykey2    ==    myvalue2
    sessionStorage remove    mykey2
    sessionStorage get    mykey2    ==    ${None}

Localstorage clear
    localStorage set    key1    value1
    localStorage set    key2    value2
    localStorage clear
    localStorage get    key1    ==    ${None}
    localStorage get    key2    ==    ${None}

Sessionstorage clear
    sessionStorage set    key1    value1
    sessionStorage set    key2    value2
    ${val1}=    Execute Javascript on Page    window.sessionStorage.getItem("key1")
    should be equal    ${val1}    value1
    sessionStorage clear
    sessionStorage get    key1    ==    ${None}
    sessionStorage get    key2    ==    ${None}
