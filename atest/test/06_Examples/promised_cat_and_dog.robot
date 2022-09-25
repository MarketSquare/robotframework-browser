*** Settings ***
Resource    imports.resource

*** Test Cases ***
Shows A Cat And A Dog
    [Tags]    no-mac-support    slow
    Set Browser Timeout    5s    scope=Test
    Set Retry Assertions For    3s    scope=Test
    New Page    ${DOG_AND_CAT_URL}
    Get Text    id=texts    ==    Beginning
    ${cat_promise} =    Promise To    Get Text    id=texts    ==    Cat
    ${dog_promise} =    Promise To    Get Text    id=texts    ==    Dog
    Click    id=clicker
    Wait For    ${cat_promise}    ${dog_promise}
    Get Text    id=texts    ==    The End
