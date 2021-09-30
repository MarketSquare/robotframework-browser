*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}


*** Test Cases ***
Reject changes promise state
    ${promise}=  Promise To  Get Text  Elem
    ${state}=  Get Promise State  ${promise}

    Reject  ${promise}
    ${rejected_state}=  Get Promise State  ${promise}
    
    Should Not Be Equal    ${state}    ${rejected_state}


Rejected promise does not fail test
    ${promise}=  Promise To  Get Text  Elem
    Reject  ${promise}

