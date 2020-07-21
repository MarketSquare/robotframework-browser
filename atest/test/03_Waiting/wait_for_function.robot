*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Wait For Function
    Wait For Function    function(){return true}  timeout=500ms
