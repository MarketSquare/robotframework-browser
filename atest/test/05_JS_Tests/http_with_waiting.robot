*** Settings ***
Resource          imports.resource
Suite Setup       New Page    ${LOGIN_URL}

*** Test Cases ***
GET with waiting json response
    ${promise}=    Promise To    Wait For Response    matcher=/api/get/json    timeout=3s
    &{response}=    HTTP    /api/get/json
    ${content}=    Wait For    ${promise}
    Should be equal    ${content}[body]    ${response}[body]
    Should be equal    ${content}[status]    ${response}[status]
    Should be equal    ${content}[url]    ${response}[url]
    Should be equal    ${content}[request][method]    GET

POST with waiting json response
    ${promise}=    Promise To    Wait For Response    matcher=/api/post    timeout=3s
    &{response}=    HTTP    /api/post    POST    {"name": "George"}
    ${content}=    Wait For    ${promise}
    Should be equal    ${content}[body]    ${response}[body]
    Should be equal    ${content}[status]    ${response}[status]
    Should be equal    ${content}[url]    ${response}[url]
    Should be equal    ${content}[request][method]    POST
    Should be equal    ${content}[request][postData][name]    George

GET with text response
    ${promise}=    Promise To    Wait For Response    matcher=/api/get/text    timeout=3s
    &{response}=    HTTP    /api/get/text
    ${content}=    Wait For    ${promise}
    Should be equal    ${content}[body]    ${response}[body]
    Should be equal    ${content}[status]    ${response}[status]
    Should be equal    ${content}[url]    ${response}[url]
    Should be equal    ${content}[request][method]    GET
