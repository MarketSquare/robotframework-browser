*** Settings ***
Library           Browser
Resource          keywords.resource
Test Setup        Open Browser    ${LOGIN URL}
Test Teardown     Close Browser

*** Test Cases ***
Testing results from page
    ${result}=    Execute Javascript on Page    "hello from page "+location.href
    should be equal    ${result}    hello from page http://localhost:7272/
    ${result2}=    Execute Javascript on Page    1+2+3
    should be equal    ${result2}    ${6}
    ${result3}=    Execute Javascript on Page    1.3314*3.13432
    should be equal    ${result3}    ${4.173033648}
