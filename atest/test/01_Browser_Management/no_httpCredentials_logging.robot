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
    ...    LOG 1:2    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 1:2    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    ...    LOG 1:3    INFO    REGEXP:    .*"httpCredentials": "XXX".*
    ...    LOG 1:3    INFO    REGEXP:    .*ignoreHTTPSErrors.*
    New Context    httpCredentials={'username': 'name', 'password': 'pwd'}
