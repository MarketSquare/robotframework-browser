*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Test Cases ***
GET With Waiting Json Response
    ${promise} =    Promise To    Wait For Response    matcher=**/api/get/json    timeout=3s
    &{response} =    HTTP    /api/get/json
    ${content} =    Wait For    ${promise}
    Should Contain    ${content}[headers][content-type]    application/json
    Should Contain    ${response}[headers][content-type]    application/json
    Should Be Matching    ${content}    ${response}
    Should Be Equal    ${content}[request][method]    GET

POST With Waiting Json Response
    ${promise} =    Promise To
    ...    Wait For Response
    ...    matcher= response => response.url() === '${ROOT_URL}api/post' && response.status() === 200
    ...    timeout=3s
    &{response} =    HTTP    /api/post    POST    {"name": "George"}
    ${content} =    Wait For    ${promise}
    Log To Console    ${{json.dumps($content, indent=4)}}
    Should Contain    ${content}[headers][content-type]    application/json
    Should Contain    ${response}[headers][content-type]    application/json
    Should Be Matching    ${content}    ${response}
    Should Be Equal    ${content}[request][method]    POST
    Should Be Equal    ${content}[request][postData][name]    George

GET With Text Response
    [Tags]    no-docker-pr
    ${promise} =    Promise To    Wait For Response    matcher=/http://\\w+:\\d+/api/get/text/i    timeout=3s
    &{response} =    HTTP    /api/get/text
    ${content} =    Wait For    ${promise}
    Should Contain    ${content}[headers][content-type]    text/html
    Should Contain    ${response}[headers][content-type]    text/html
    Should Be Matching    ${content}    ${response}
    Should Be Equal    ${content}[request][method]    GET

GET With Binary Response
    ${promise} =    Promise To    Wait For Response    matcher=${ROOT_URL}api/get/bad_binary    timeout=3s
    &{response} =    HTTP    /api/get/bad_binary
    ${content} =    Wait For    ${promise}
    Should Be Matching    ${content}    ${response}
    Should Be Equal    ${content}[request][method]    GET

*** Keywords ***
Should Be Matching
    [Arguments]    ${first}    ${second}
    Should Be Equal    ${first}[body]    ${second}[body]
    Should Be Equal    ${first}[status]    ${second}[status]
    Should Be Equal    ${first}[url]    ${second}[url]
