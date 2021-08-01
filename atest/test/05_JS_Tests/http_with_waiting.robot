*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Test Cases ***
GET with waiting json response
    ${promise} =    Promise To    Wait For Response    matcher=/api/get/json    timeout=3s
    &{response} =    HTTP    /api/get/json
    ${content} =    Wait For    ${promise}
    Should contain    ${content}[headers][content-type]    application/json
    Should contain    ${response}[headers][content-type]    application/json
    Should be matching    ${content}    ${response}
    Should be equal    ${content}[request][method]    GET

POST with waiting json response
    ${promise} =    Promise To    Wait For Response    matcher=/api/post    timeout=3s
    &{response} =    HTTP    /api/post    POST    {"name": "George"}
    ${content} =    Wait For    ${promise}
    Should contain    ${content}[headers][content-type]    application/json
    Should contain    ${response}[headers][content-type]    application/json
    Should be matching    ${content}    ${response}
    Should be equal    ${content}[request][method]    POST
    Should be equal    ${content}[request][postData][name]    George

GET with text response
    ${promise} =    Promise To    Wait For Response    matcher=/api/get/text    timeout=3s
    &{response} =    HTTP    /api/get/text
    ${content} =    Wait For    ${promise}
    Should contain    ${content}[headers][content-type]    text/html
    Should contain    ${response}[headers][content-type]    text/html
    Should be matching    ${content}    ${response}
    Should be equal    ${content}[request][method]    GET

*** Keywords ***
Should be matching
    [Arguments]    ${first}    ${second}
    Should be equal    ${first}[body]    ${second}[body]
    Should be equal    ${first}[status]    ${second}[status]
    Should be equal    ${first}[url]    ${second}[url]
