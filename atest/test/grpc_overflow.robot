*** Settings ***
Resource          keywords.resource

*** Test Cases ***
GRPC Message Overflow Should Not Happen Event The Message Exceeds Default Size
    ${aabbcc}    Set Variable    AABBCC
    New Context
    New Page    ${ROOT_URL}/enabled_disabled_fields_form.html
    ${timeout} =    Set Browser Timeout    2s
    Run Keyword And Expect Error
    ...    TimeoutError: page.waitForSelector: Timeout 2000ms exceeded.${\n}=========================== logs ===========================${\n}waiting for selector "//${aabbcc * 100}*
    ...    Get Attribute    //${aabbcc * 1500}    foo    equal    tidii
    [Teardown]    Set Browser Timeout    ${timeout}
