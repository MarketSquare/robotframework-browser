*** Settings ***
Resource          imports.resource
Suite Setup    Close Browser    ALL

*** Test Cases ***
Get Empty Browser IDs
    Check Return Value is Empty List    Get Browser IDs    All
    Check Return Value is Empty List    Get Browser IDs    Active

Get Empty Context IDs
    Check Return Value is Empty List    Get Context Ids    Active    Active
    Check Return Value is Empty List    Get Context Ids    Active    All
    Check Return Value is Empty List    Get Context Ids    All    Active
    Check Return Value is Empty List    Get Context Ids    All    All

Get Empty Page IDs
    Check Return Value is Empty List    Get Page Ids    Active    Active    Active
    Check Return Value is Empty List    Get Page Ids    Active    Active    All
    Check Return Value is Empty List    Get Page Ids    Active    All    Active
    Check Return Value is Empty List    Get Page Ids    Active    All    All
    Check Return Value is Empty List    Get Page Ids    All    Active    Active
    Check Return Value is Empty List    Get Page Ids    All    Active    All
    Check Return Value is Empty List    Get Page Ids    All    All    Active
    Check Return Value is Empty List    Get Page Ids    All    All    All

Get Empty Context IDs from Browser
    New Browser
    Check Return Value is Empty List    Get Context Ids    Active    Active
    Check Return Value is Empty List    Get Context Ids    Active    All
    Check Return Value is Empty List    Get Context Ids    All    Active
    Check Return Value is Empty List    Get Context Ids    All    All

Get Empty Context ID from Empty Browser
    ${browser}=    New Browser
    New Browser
    New Context
    Switch Browser    ${browser}
    Check Return Value is Empty List    Get Context Ids    Active    Active
    Check Return Value is Empty List    Get Context Ids    All    Active

Get Empty Page ID from Empty Browser and Empty Context
    ${browser}=    New Browser
    Check Return Value is Empty List    Get Page Ids    Active    Active    Active
    Check Return Value is Empty List    Get Page Ids    Active    Active    All
    Check Return Value is Empty List    Get Page Ids    Active    All    Active
    Check Return Value is Empty List    Get Page Ids    Active    All    All
    Check Return Value is Empty List    Get Page Ids    All    Active    Active
    Check Return Value is Empty List    Get Page Ids    All    Active    All
    Check Return Value is Empty List    Get Page Ids    All    All    Active
    Check Return Value is Empty List    Get Page Ids    All    All    All
    ${Context}=    New Context
    Check Return Value is Empty List    Get Page Ids    Active    Active    Active
    Check Return Value is Empty List    Get Page Ids    Active    Active    All
    Check Return Value is Empty List    Get Page Ids    Active    All    Active
    Check Return Value is Empty List    Get Page Ids    Active    All    All
    Check Return Value is Empty List    Get Page Ids    All    Active    Active
    Check Return Value is Empty List    Get Page Ids    All    Active    All
    Check Return Value is Empty List    Get Page Ids    All    All    Active
    Check Return Value is Empty List    Get Page Ids    All    All    All
    New Context
    New Page
    Switch Context    ${Context}
    Check Return Value is Empty List    Get Page Ids    Active    Active    Active
    Check Return Value is Empty List    Get Page Ids    Active    Active    All
    Check Return Value is Empty List    Get Page Ids    All    Active    Active
    Check Return Value is Empty List    Get Page Ids    All    Active    All

*** Keywords ***
Check Return Value is Empty List
    [Arguments]    ${keyword}    @{args}
    ${should_be_empty}=    Run Keyword And Continue On Failure    ${keyword}    @{args}
    Run Keyword And Continue On Failure    Should Be True    $should_be_empty == []
