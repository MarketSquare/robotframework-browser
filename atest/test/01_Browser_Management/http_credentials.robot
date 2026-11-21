*** Settings ***
Resource         imports.resource

Test Teardown    Close Context

Test Tags        no-iframe

*** Variables ***
${USERNAME} =        robot
${PASSWORD} =        secret
${AUTH_PATH} =       api/basic-auth/robot/secret
${OTHER_USER} =      other
${OTHER_PW} =        other-pw
${OTHER_ORIGIN} =    http://127.0.0.1:${SERVER_PORT}

*** Test Cases ***
Credentials Set Mid Test Pass Basic Auth
    Open Context
    VAR    &{credential} =    username=$USERNAME    password=$PASSWORD
    Set HTTP Credentials    ${credential}
    Basic Auth Status Should Be    ${ROOT_URL}${AUTH_PATH}    200

Credentials With An Origin Are Sent Only To That Origin
    Open Context
    VAR    &{credential} =    username=$USERNAME    password=$PASSWORD    origin=http://${SERVER}
    Set HTTP Credentials    ${credential}
    Basic Auth Status Should Be    ${ROOT_URL}${AUTH_PATH}    200
    Basic Auth Status Should Be    ${OTHER_ORIGIN_ROOT_URL}${AUTH_PATH}    401

First Credential Matching The Origin Is Used
    Open Context
    VAR    &{other} =    username=$OTHER_USER    password=$OTHER_PW    origin=${OTHER_ORIGIN}
    VAR    &{credential} =    username=$USERNAME    password=$PASSWORD
    Set HTTP Credentials    ${other}    ${credential}
    Basic Auth Status Should Be    ${ROOT_URL}${AUTH_PATH}    200
    Basic Auth Status Should Be    ${OTHER_ORIGIN_ROOT_URL}api/basic-auth/other/other-pw    200

Credentials Replace The Credentials Of New Context
    Open Context    httpCredentials={'username': '$USERNAME', 'password': '$PASSWORD'}
    VAR    &{other} =    username=$OTHER_USER    password=$OTHER_PW
    Set HTTP Credentials    ${other}
    Basic Auth Status Should Be    ${ROOT_URL}${AUTH_PATH}    401

No Credentials Clear The Credentials
    Open Context    httpCredentials={'username': '$USERNAME', 'password': '$PASSWORD'}
    Set HTTP Credentials
    Basic Auth Status Should Be    ${ROOT_URL}${AUTH_PATH}    401

Credentials Given As Plain Values Are Rejected
    Open Context
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'credentials' is not allowed.*
    ...    Set HTTP Credentials    {'username': 'robot', 'password': 'secret'}

Secret Credentials Pass Basic Auth
    [Tags]    require-rf-7.4+
    Open Context
    Set Environment Variable    AUTH_PASSWORD    ${PASSWORD}
    VAR    ${password: Secret} =    %{AUTH_PASSWORD}
    VAR    &{credential} =    username=${USERNAME}    password=${password}
    Set HTTP Credentials    ${credential}
    Basic Auth Status Should Be    ${ROOT_URL}${AUTH_PATH}    200

*** Keywords ***
Open Context
    [Arguments]    &{context_options}
    New Context    &{context_options}
    New Page

Basic Auth Status Should Be
    [Arguments]    ${url}    ${expected}
    ${status} =    Go To    ${url}
    Should Be Equal    ${status}    ${${expected}}
