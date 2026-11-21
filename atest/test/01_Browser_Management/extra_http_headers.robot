*** Settings ***
Resource         imports.resource

Test Setup       Open HTTP Test Page
Test Teardown    Close Context

Test Tags        no-iframe

*** Test Cases ***
Context Headers Set Mid Test Reach The Server
    Set Extra HTTP Headers    X-Tenant=b    Authorization=Bearer token
    Echoed Header Should Be    x-tenant    b
    Echoed Header Should Be    authorization    Bearer token

Context Headers Replace The Headers Of New Context
    [Setup]    Open HTTP Test Page    extraHTTPHeaders={"X-Tenant": "a"}
    Set Extra HTTP Headers    X-Other=1
    Echoed Header Should Be    x-other    1
    Header Should Not Be Echoed    x-tenant

Empty Header Value Is Sent
    Set Extra HTTP Headers    X-Empty=${EMPTY}
    Echoed Header Should Be    x-empty    ${EMPTY}

No Headers Clear The Context Headers
    [Setup]    Open HTTP Test Page    extraHTTPHeaders={"X-Tenant": "a"}
    Set Extra HTTP Headers
    Header Should Not Be Echoed    x-tenant

Context Headers Reach A Page Opened Later
    Set Extra HTTP Headers    X-Tenant=b
    New Page    ${HTTP_URL}
    Echoed Header Should Be    x-tenant    b

Page Headers Reach Only The Active Page
    Set Extra HTTP Headers    X-Page=1    target=Page
    Echoed Header Should Be    x-page    1
    New Page    ${HTTP_URL}
    Header Should Not Be Echoed    x-page

Page Header Wins Over A Context Header Of The Same Name
    Set Extra HTTP Headers    X-Tenant=context    X-Context=1
    Set Extra HTTP Headers    X-Tenant=page    target=Page
    Echoed Header Should Be    x-tenant    page
    Echoed Header Should Be    x-context    1

Secret Header Value Reaches The Server
    [Tags]    require-rf-7.4+
    Set Environment Variable    HEADER_TOKEN    Bearer secret-token
    VAR    ${token: Secret} =    %{HEADER_TOKEN}
    Set Extra HTTP Headers    Authorization=${token}
    Echoed Header Should Be    authorization    Bearer secret-token

*** Keywords ***
Open HTTP Test Page
    [Arguments]    &{context_options}
    New Context    &{context_options}
    New Page    ${HTTP_URL}

Echoed Header Should Be
    [Arguments]    ${name}    ${expected}
    &{response} =    HTTP    /api/echo/headers
    Should Be Equal    ${response.body.headers}[${name}]    ${expected}

Header Should Not Be Echoed
    [Arguments]    ${name}
    &{response} =    HTTP    /api/echo/headers
    Dictionary Should Not Contain Key    ${response.body.headers}    ${name}
