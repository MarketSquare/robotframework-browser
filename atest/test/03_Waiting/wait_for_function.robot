*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Succesful Wait For Function
    Wait For Function    function(){return true}    timeout=500ms

Failed Wait For Function
    Run Keyword and Expect Error    ""    Wait For Function    function(){return false}    timeout=100ms
