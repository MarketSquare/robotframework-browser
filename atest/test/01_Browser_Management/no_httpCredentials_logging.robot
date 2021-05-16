*** Settings ***
Resource          imports.resource
Test Teardown     Close Context

*** Test Cases ***
New Context No Mask For httpCredentials When Not Defined
    [Documentation]    ...
    ...    LOG 1:2    INFO    REGEXP:    ^((?!httpCredentials).)*$
    ...    LOG 1:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 1:3    INFO    REGEXP:    ^((?!httpCredentials).)*$
    ...    LOG 1:3    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    New Context

New Context Mask For httpCredentials When Defined
    [Documentation]    ...
    ...    LOG 1:2    WARN    REGEXP:    Direct assignment of values as 'httpCredentials' is deprecated.*
    ...    LOG 1:3    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 1:3    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 1:4    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 1:4    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    New Context    httpCredentials={'username': 'name', 'password': 'pwd'}

New Context httpCredentials Resolved
    [Documentation]    ...
    ...    LOG 3:2    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 3:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 3:3    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 3:3    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ${pwd} =    Set Variable    pwd
    ${username} =    Set Variable    name
    New Context    httpCredentials={'username': '$username', 'password': '$pwd'}
