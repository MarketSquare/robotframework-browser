*** Settings ***
Library         OperatingSystem
Library         CryptoLibrary    password=cryptoPassword123    key_path=${CURDIR}/keys/
Resource        imports.resource

Suite Setup     New Page
Test Setup      Ensure Open Page    ${LOGIN_URL}

Test Tags       require-rf-7.4+

*** Test Cases ***
Type Secret And Verify
    ${secret} =    Get Secret Value
    Type Secret    input#username_field    ${secret}
    Get Text    input#username_field    ==    Joulupukki

Fill Secret And Verify
    ${secret} =    Get Secret Value
    Fill Secret    input#username_field    ${secret}
    Get Text    input#username_field    ==    Joulupukki

Type Secret And Fails With Curly Brackets
    Set Browser Timeout    500ms    scope=Test
    ${secret} =    Get Secret Value
    TRY
        Type Secret    notHere    ${secret}
    EXCEPT    *    type=GLOB    AS    ${error}
        Should Contain    ${error}    notHere
    END

Fill Secret And Fails With Curly Brackets
    Set Browser Timeout    500ms    scope=Test
    ${secret} =    Get Secret Value
    TRY
        Fill Secret    notHere    ${secret}
    EXCEPT    *    type=GLOB    AS    ${error}
        Should Contain    ${error}    notHere
    END

Type Secret And Fails Without Curly Brackets
    Set Browser Timeout    500ms    scope=Test
    ${secret} =    Get Secret Value
    TRY
        Type Secret    notHere    $secret
    EXCEPT    *    type=GLOB    AS    ${error}
        Should Contain    ${error}    notHere
    END

Fill Secret And Fails Without Curly Brackets
    Set Browser Timeout    500ms    scope=Test
    ${secret} =    Get Secret Value
    TRY
        Fill Secret    notHere    $secret
    EXCEPT    *    type=GLOB    AS    ${error}
        Should Contain    ${error}    notHere
    END

New Context With Secret As Literal In httpCredentials Is Not Supported
    ${secret} =    Get Secret Value
    TRY
        New Context    httpCredentials={'username': ${secret}, 'password': ${secret}}
    EXCEPT    ValueError:*    type=GLOB    AS    ${error}
        Log    Correct error ${error} was raised
        Should Contain    ${error}    httpCredentials
    END

New Context With Secret As Dict In httpCredentialsIs Supported
    ${secret} =    Get Secret Value
    VAR    &{httpCredentials} =    username=${secret}    password=${secret}
    New Context    httpCredentials=${httpCredentials}
    Close Context

New Context With Secret As Dict In Proxy Supported
    ${secret} =    Get Secret Value
    VAR    &{proxy} =    server=http://proxy:8080    username=${secret}    password=${secret}
    New Browser    proxy=${proxy}
    New Context    proxy=${proxy}
    Close Browser

*** Keywords ***
Get Secret Value
    Set Environment Variable    SECRET_VALUE    Joulupukki
    VAR    ${secret: Secret} =    %{SECRET_VALUE}
    RETURN    ${secret}
