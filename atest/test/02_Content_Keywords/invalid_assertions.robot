*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Invalids will raise error directly from Robot Framework
    run keyword and expect error    *'assertion_operator' got value 'invalidOperator' that cannot be converted to AssertionOperator*    Get Title    invalidOperator    value
    run keyword and expect error    *'assertion_operator' got value 'sHouLd BE' that cannot be converted to AssertionOperator*    Get Title    sHouLd BE    value
    run keyword and expect error    *'assertion_operator' got value 'faultyOps' that cannot be converted to AssertionOperator*    Get URL    faultyOps
    run keyword and expect error    *'assertion_operator' got value '!=!' that cannot be converted to AssertionOperator*    get_text    h1    !=!    blaah
    run keyword and expect error    *'assertion_operator' got value 'huh' that cannot be converted to AssertionOperator*    Get Textfield Value    css=input#username_field    huh    hah
    run keyword and expect error    *'assertion_operator' got value 'equas' that cannot be converted to AssertionOperator*    Get Property    h1    innerText    equas    plaah
