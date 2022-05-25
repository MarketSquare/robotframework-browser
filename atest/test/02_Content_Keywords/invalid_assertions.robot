*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Invalids Will Raise Error Directly From Robot Framework
    Run Keyword And Expect Error
    ...    *'assertion_operator' got value 'invalidOperator' that cannot be converted to AssertionOperator*
    ...    Get Title    invalidOperator    value
    Run Keyword And Expect Error
    ...    *'assertion_operator' got value 'faultyOps' that cannot be converted to AssertionOperator*    Get URL
    ...    faultyOps
    Run Keyword And Expect Error
    ...    *'assertion_operator' got value '!=!' that cannot be converted to AssertionOperator*    Get Text    h1
    ...    !=!    blaah
    Run Keyword And Expect Error
    ...    *'assertion_operator' got value 'equas' that cannot be converted to AssertionOperator*
    ...    Get Property    h1    innerText    equas    plaah
