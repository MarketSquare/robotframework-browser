*** Settings ***
Resource            imports.resource

Suite Setup         New Page    ${LOGIN_URL}
Suite Teardown      Close Browser    ALL

*** Test Cases ***
Set And Get Local Storage
    Local Storage Set Item    Tidii    Kala
    ${item} =    Local Storage Get Item    Tidii
    Should Be Equal    ${item}    Kala

Local Storage Get Item Should Fail If Item Does Not Exist
    ${item} =    Local Storage Get Item    Kala
    Should Be Equal    ${item}    ${None}

Local Storage Get Item Default Error
    [Tags]    slow
    Run Keyword And Expect Error
    ...    localStorage 'None' (nonetype) should be 'Tidii' (str)
    ...    Local Storage Get Item    Kala    ==    Tidii

Local Storage Get Item Custom Error
    [Tags]    slow
    Run Keyword And Expect Error
    ...    My error
    ...    Local Storage Get Item    Kala    ==    Tidii    My error

Remove Local Storage Item
    Local Storage Set Item    Foo    bar
    ${item} =    Local Storage Get Item    Foo
    Should Be Equal    ${item}    bar
    LocalStorage Remove Item    Foo
    ${item} =    Local Storage Get Item    Foo
    Should Be Equal    ${item}    ${None}

Clear Local Storage
    Local Storage Set Item    Foo    bar
    ${item} =    Local Storage Get Item    Foo
    Should Be Equal    ${item}    bar
    LocalStorage Clear
    ${item} =    Local Storage Get Item    Foo
    Should Be Equal    ${item}    ${None}
