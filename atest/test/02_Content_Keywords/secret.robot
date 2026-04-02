*** Settings ***
Library         OperatingSystem
Library         CryptoLibrary    password=cryptoPassword123    key_path=${CURDIR}/keys/
Resource        imports.resource

Suite Setup     New Page
Test Setup      Ensure Open Page    ${LOGIN_URL}

Test Tags       require-rf-7.4+

*** Test Cases ***
Type Secret
    ${secret} =    Get Secret Value
    Type Secret    input#username_field    ${secret}
    Get Text    input#username_field    ==    Joulupukki

Fill Secret
    ${secret} =    Get Secret Value
    Fill Secret    input#username_field    ${secret}
    Get Text    input#username_field    ==    Joulupukki

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
