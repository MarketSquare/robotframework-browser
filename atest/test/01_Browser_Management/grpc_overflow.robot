*** Settings ***
Resource        imports.resource

Test Timeout    1000s

*** Test Cases ***
GRPC Message Overflow Should Not Happen Event The Message Exceeds Default Size
    [Tags]    slow
    ${aabbcc} =    Set Variable    AABBCC
    New Context
    New Page    ${ROOT_URL}enabled_disabled_fields_form.html
    ${timeout} =    Set Browser Timeout    2s
    ${msg} =    Run Keyword And Expect Error
    ...    *
    ...    Get Attribute    //${aabbcc * 1500}    foo    equal    tidii
    Should Contain    ${msg}    Error: locator.elementHandle: Timeout 2000ms exceeded.
    Should Contain    ${msg}    waiting for locator('//${aabbcc * 80}
    [Teardown]    Set Browser Timeout    ${timeout}
