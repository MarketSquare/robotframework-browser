*** Settings ***
Resource          imports.resource
Suite Setup       New Page    ${LOGIN_URL}

*** Test Cases ***
GET with waiting json response
    ${promise}=     Promise To    Wait For Response    matcher=/api/get/json    timeout=3s
    &{response}=    HTTP    /api/get/json
    ${content}=     Wait For    ${promise}
    Should be equal  ${content}  ${response}[body]

POST with waiting json response
    ${promise}=     Promise To    Wait For Response    matcher=/api/post    timeout=3s
    &{response}=    HTTP    /api/post    POST    {"name": "George"}
    ${content}=     Wait For    ${promise}
    Should be equal  ${content}  ${response}[body]