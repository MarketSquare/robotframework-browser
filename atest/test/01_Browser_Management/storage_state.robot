*** Settings ***
Resource          imports.resource
Suite Setup       New Browser

*** Test Cases ***
Save storage state
    New Context
    New Page    ${LOGIN_URL}
    Add Cookies For Storage
    ${state_file} =    Save Storage State
    File Should Not Be Empty    ${state_file}

*** Keywords ***
Add Cookies For Storage
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    Add Cookie    Key    Value    url=${url}
    Execute JavaScript    localStorage.setItem('bgcolor', 'red');
