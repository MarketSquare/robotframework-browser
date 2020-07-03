*** Settings ***
Resource          keywords.resource

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    demo
    Input Pwd    mode
    Submit Credentials
    Welcome Page Should Be Open
    [Teardown]    Close Browser
