*** Settings ***
Library           Browser
Resource          keywords.resource
Test Setup        Open Browser    ${LOGIN URL}
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
    Localstorage set    mykey    myvalue
    Localstorage get    mykey    ==    myvalue
    ${val}=    Execute Javascript on Page    window.localStorage.getItem("mykey")
    should be equal    ${val}    myvalue
    Localstorage remove    mykey
    Localstorage get    mykey    ==    ${None}

Sessionstorage
    Sessionstorage set    mykey2    myvalue2
    Sessionstorage get    mykey2    ==    myvalue2
    Sessionstorage remove    mykey2
    Sessionstorage get    mykey2    ==    ${None}

Localstorage clear
    Localstorage set    key1    value1
    Localstorage set    key2    value2
    Localstorage clear
    Localstorage get    key1    ==    ${None}
    Localstorage get    key2    ==    ${None}

Sessionstorage clear
    Sessionstorage set    key1    value1
    Sessionstorage set    key2    value2
    ${val1}=    Execute Javascript on Page    window.sessionStorage.getItem("key1")
    should be equal    ${val1}    value1
    Sessionstorage clear
    Sessionstorage get    key1    ==    ${None}
    Sessionstorage get    key2    ==    ${None}
