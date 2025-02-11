*** Settings ***
Resource            imports.resource

Suite Setup         New Browser
Test Teardown       Close Context

*** Test Cases ***
New Context No Mask For HttpCredentials When Not Defined
    [Documentation]    ...
    ...    LOG 2:2    INFO    REGEXP:    ^((?!httpCredentials).)*$
    ...    LOG 2:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 2:4    INFO    REGEXP:    ^((?!httpCredentials).)*$
    ...    LOG 2:4    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    [Tags]    no-mac-support
    New Context

New Context Mask For HttpCredentials When Defined
    [Tags]    no-mac-support
    TRY
        New Context    httpCredentials={'username': 'name', 'password': 'pwd'}
    EXCEPT    ValueError: Direct assignment of values or variables as 'httpCredentials' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    Correct Error Message
    END

New Context HttpCredentials Resolved
    [Documentation]    ...
    ...    LOG 4:2    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 4:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 4:4    INFO    REGEXP:    .*httpCredentials(\"|'):\\s(\"|')XXX(\"|').*
    ...    LOG 4:4    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    [Tags]    no-mac-support
    ${pwd} =    Set Variable    pwd
    ${username} =    Set Variable    name
    New Context    httpCredentials={'username': '$username', 'password': '$pwd'}

New Context HttpCredentials Resolved As Dict
    [Documentation]    ...
    ...    LOG 5:2    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 5:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 5:4    INFO    REGEXP:    .*httpCredentials(\"|'):\\s(\"|')XXX(\"|').*
    ...    LOG 5:4    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    [Tags]    no-mac-support
    ${pwd} =    Set Variable    pwd
    ${username} =    Set Variable    name
    ${credentials} =    Create Dictionary    username=$username    password=$pwd
    New Context    httpCredentials=${credentials}
