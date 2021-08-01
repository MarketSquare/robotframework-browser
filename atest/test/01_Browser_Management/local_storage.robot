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
    Run Keyword And Expect Error
    ...    localStorage 'None' (nonetype) should be 'Tidii' (str)
    ...    Local Storage Get Item    Kala    ==    Tidii

Local Storage Get Item Custom Error
    Run Keyword And Expect Error
    ...    My error
    ...    Local Storage Get Item    Kala    ==    Tidii    My error
