*** Settings ***
Resource            imports.resource

Suite Setup         New Browser
Suite Teardown      Close Browser
Test Setup          New Page    ${LOGIN_URL}

*** Test Cases ***
Localstorage
    localStorage set Item    mykey    myvalue
    localStorage get Item    mykey    ==    myvalue
    ${val}=    Execute Javascript    window.localStorage.getItem("mykey")
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
    ${val1}=    Execute Javascript    window.sessionStorage.getItem("key1")
    should be equal    ${val1}    value1
    sessionStorage clear
    sessionStorage get Item    key1    ==    ${None}
    sessionStorage get Item    key2    ==    ${None}
