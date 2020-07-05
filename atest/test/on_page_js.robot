*** Settings ***
Library           Browser
Resource          keywords.resource
Test Setup        Open Browser    ${LOGIN URL}
Test Teardown     Close Browser

*** Test Cases ***
Testing hello from page
  Execute Javascript on Page   "hello "+window.location.href;
