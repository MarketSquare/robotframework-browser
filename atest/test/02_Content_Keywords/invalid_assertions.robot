*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Invalids will raise error directly from Robot Framework
    run keyword and expect error
    ...    *'assertion_operator' got value 'invalidOperator' that cannot be converted to AssertionOperator*
    ...    Get Title    invalidOperator    value
    run keyword and expect error
    ...    *'assertion_operator' got value 'faultyOps' that cannot be converted to AssertionOperator*    Get URL
    ...    faultyOps
    run keyword and expect error
    ...    *'assertion_operator' got value '!=!' that cannot be converted to AssertionOperator*    Get Text    h1
    ...    !=!    blaah
    run keyword and expect error
    ...    *'assertion_operator' got value 'equas' that cannot be converted to AssertionOperator*
    ...    Get Property    h1    innerText    equas    plaah
