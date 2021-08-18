*** Settings ***
Resource    imports.resource

*** Test Cases ***
GRPC Message Overflow Should Not Happen Event The Message Exceeds Default Size
    ${aabbcc} =    Set Variable    AABBCC
    New Context
    New Page    ${ROOT_URL}/enabled_disabled_fields_form.html
    ${timeout} =    Set Browser Timeout    2s
    ${msg} =    Run Keyword And Expect Error
    ...    *
    ...    Get Attribute    //${aabbcc * 1500}    foo    equal    tidii
    Should Contain    ${msg}    TimeoutError: page.waitForSelector: Timeout 2000ms exceeded.
    Should Contain    ${msg}    =========================== logs ===========================
    Should Contain    ${msg}    waiting for selector "//${aabbcc * 100}
    [Teardown]    Set Browser Timeout    ${timeout}
