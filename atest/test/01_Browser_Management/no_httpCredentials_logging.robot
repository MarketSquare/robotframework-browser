*** Settings ***
Resource            imports.resource

Test Teardown       Close Context

*** Test Cases ***
New Context No Mask For HttpCredentials When Not Defined
    [Documentation]    ...
    ...    LOG 1:2    INFO    REGEXP:    ^((?!httpCredentials).)*$
    ...    LOG 1:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 1:4    INFO    REGEXP:    ^((?!httpCredentials).)*$
    ...    LOG 1:4    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    [Tags]    no-mac-support
    New Context

New Context Mask For HttpCredentials When Defined
    [Documentation]    ...
    ...    LOG 1:2    WARN    REGEXP:    Direct assignment of values as 'httpCredentials' is deprecated.*
    ...    LOG 1:3    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 1:3    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 1:5    INFO    REGEXP:    .*httpCredentials(\"|'):\\s(\"|')XXX(\"|').*
    ...    LOG 1:5    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    [Tags]    no-mac-support
    New Context    httpCredentials={'username': 'name', 'password': 'pwd'}

New Context HttpCredentials Resolved
    [Documentation]    ...
    ...    LOG 3:2    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 3:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 3:4    INFO    REGEXP:    .*httpCredentials(\"|'):\\s(\"|')XXX(\"|').*
    ...    LOG 3:4    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    [Tags]    no-mac-support
    ${pwd} =    Set Variable    pwd
    ${username} =    Set Variable    name
    New Context    httpCredentials={'username': '$username', 'password': '$pwd'}
