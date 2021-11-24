*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Variables ***
&{expected get json body} =     greeting=HELLO
&{expected post json body} =    name=John    id=${1}
&{expected put json body} =     name=Jane    id=${3}

*** Test Cases ***
GET with text response
    &{response} =    HTTP    /api/get/text
    Should Be Equal    ${response.body}    HELLO
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.headers['content-type']}    text/html; charset=utf-8

GET with json response
    &{response} =    HTTP    /api/get/json
    Should Be Equal    ${response.body}    ${expected get json body}
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.headers['content-type']}    application/json; charset=utf-8

GET with error
    &{response} =    HTTP    /api/get/doesntexist
    Should Be Equal    ${response.status}    ${404}

POST
    &{response} =    HTTP    /api/post    POST    {"name": "John"}
    Should Be Equal    ${response.body}    ${expected post json body}

PUT
    &{response} =    HTTP    /api/put    PUT    {"name": "Jane"}
    Should Be Equal    ${response.body}    ${expected put json body}

PATCH
    &{response} =    HTTP    /api/patch    PATCH    {"name": "Jane"}
    Should Be Equal    ${response.body}    ${expected put json body}

DELETE
    &{response} =    HTTP    /api/delete    DELETE    {"name": "Jane"}
    Should Be Equal    ${response.status}    ${200}

HEAD
    &{response} =    HTTP    /api/get/json
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.headers['content-type']}    application/json; charset=utf-8
