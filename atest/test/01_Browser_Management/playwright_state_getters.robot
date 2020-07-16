*** Settings ***
Resource          imports.resource
Suite Setup       No Operation
Test Setup        No Operation

*** Test Cases ***
Get Pages
    Create Page    ${FORM_URL}
    Create Page    ${LOGIN_URL}
    ${pages}    Get Pages
