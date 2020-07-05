*** Settings ***
Library           Browser
Resource          keywords.resource
Test Setup        Open Browser    ${LOGIN URL}
Test Teardown     Close Browser

*** Test Cases ***
Testing hello from page
  ${result}=  Execute Javascript on Page   "hello from page "+location.href
  should be equal  ${result}  hello from page http://localhost:7272/
