*** Settings ***
Resource      imports.resource

Test Setup    Ensure Location    ${LOGIN_URL}

Force Tags    no-iframe

*** Variables ***
${PNG_SIGNATURE} =    ${{ bytes.fromhex('89504e470d0a1a0a') }}

*** Test Cases ***
Response All Headers Contain Set-Cookie
    ${response} =    Capture Response    /api/set-cookies
    Should Contain    ${response.allHeaders}[set-cookie]    session=abc
    Should Contain    ${response.allHeaders}[set-cookie]    theme=dark
    Dictionary Should Not Contain Key    ${response.headers}    set-cookie
    ${set_cookies} =    Evaluate
    ...    [entry.value for entry in $response.headersArray if entry.name.lower() == 'set-cookie']
    Length Should Be    ${set_cookies}    2

Binary Response Body Is Returned Unchanged As Bytes
    ${response} =    Capture Response    /api/get/bad_binary
    Should Be Equal    ${response.bytes}    ${PNG_SIGNATURE}
    Should Be Equal    ${response.json}    ${None}

Response Body Is Available As Text And Json
    ${response} =    Capture Response    /api/get/json
    Should Be Equal    ${response.text}    {"greeting":"HELLO"}
    Should Be Equal    ${response.json}    ${{ {'greeting': 'HELLO'} }}
    Should Be Equal    ${response.bytes}    ${{ b'{"greeting":"HELLO"}' }}

Empty JSON Object And List Bodies Are Kept
    ${object} =    Capture Response    /api/get/empty-object
    Should Be Equal    ${object.body}    ${{ {} }}
    ${list} =    Capture Response    /api/get/empty-list
    Should Be Equal    ${list.body}    ${{ [] }}

Response Body Is Skipped When Excluded
    ${promise} =    Promise To    Wait For Response    **/api/get/json    include_body=False
    HTTP    /api/get/json
    ${response} =    Wait For    ${promise}
    Should Be Equal As Integers    ${response.status}    200
    Should Be Equal    ${response.body}    ${None}
    Should Be Equal    ${response.bytes}    ${None}
    Should Be Equal    ${response.text}    ${None}

Redirected Response Knows The Original Request
    ${promise} =    Promise To    Wait For Response    **/api/get/json
    HTTP    /api/redirect
    ${response} =    Wait For    ${promise}
    Should End With    ${response.request.redirectedFrom}    /api/redirect
    Should End With    ${response.request.url}    /api/get/json

Response Reports Connection Details
    ${response} =    Capture Response    /api/get/json
    Should Not Be Empty    ${response.httpVersion}
    Should Be Equal    ${response.fromServiceWorker}    ${False}

Captured Response Can Be Serialized As JSON
    ${response} =    Capture Response    /api/get/bad_binary
    ${serialized} =    Evaluate    json.loads(json.dumps($response))
    Should Be Equal    ${serialized}[bytes]    iVBORw0KGgo=

Fetch Request Details Are Returned
    ${promise} =    Promise To    Wait For Request    **/api/get/json
    HTTP    /api/get/json
    ${request} =    Wait For    ${promise}
    Should Be Equal    ${request.resourceType}    fetch
    Should Be Equal    ${request.isNavigationRequest}    ${False}
    Should Be Equal    ${request.redirectedTo}    ${None}
    Should Contain    ${request.frame.url}    /dist/
    Should Not Be Empty    ${request.allHeaders}

Navigation Request Is Marked As Navigation
    ${promise} =    Promise To    Wait For Request    **/redirector2.html
    Go To    ${ROOT_URL}redirector.html
    ${request} =    Wait For    ${promise}
    Should Be Equal    ${request.resourceType}    document
    Should Be Equal    ${request.isNavigationRequest}    ${True}

Form Post Data Is Parsed Like Playwright
    ${promise} =    Promise To    Wait For Request    **/api/form
    Evaluate JavaScript
    ...    ${None}
    ...    () => fetch('/api/form', {method: 'POST', headers: {'content-type': 'application/x-www-form-urlencoded'}, body: 'name=George&city=Helsinki'})
    ${request} =    Wait For    ${promise}
    Should Be Equal    ${request.postDataJSON}    ${{ {'name': 'George', 'city': 'Helsinki'} }}
    Should Be Equal    ${request.postDataBuffer}    ${{ b'name=George&city=Helsinki' }}
    Should Be Equal    ${request.postData}    name=George&city=Helsinki

Wait For Request Returns Before The Response Arrives
    ${promise} =    Promise To    Wait For Request    **/api/stalled-image    timeout=3s
    Evaluate JavaScript    ${None}    () => { fetch('/api/stalled-image'); }
    ${request} =    Wait For    ${promise}
    Should End With    ${request.url}    /api/stalled-image

*** Keywords ***
Capture Response
    [Arguments]    ${path}
    ${promise} =    Promise To    Wait For Response    **${path}
    HTTP    ${path}
    ${response} =    Wait For    ${promise}
    RETURN    ${response}
