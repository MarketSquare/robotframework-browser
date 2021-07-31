*** Settings ***
Library     Browser    timeout=5s    retry_assertions_for=3s
Resource    imports.resource

*** Test Cases ***
Shows a cat and a dog
    New Page    ${DOG_AND_CAT_URL}
    Get Text    id=texts    ==    Beginning
    ${cat_promise} =    Promise To    Get Text    id=texts    ==    Cat
    ${dog_promise} =    Promise To    Get Text    id=texts    ==    Dog
    Click    id=clicker
    Wait For    ${cat_promise}    ${dog_promise}
    Get Text    id=texts    ==    The End
