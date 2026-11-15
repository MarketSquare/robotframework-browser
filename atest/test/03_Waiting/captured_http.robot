*** Settings ***
Library       ../../library/http_headers.py
Resource      imports.resource

Test Setup    Ensure Location    ${LOGIN_URL}

Test Tags    no-iframe

*** Variables ***
${PNG_SIGNATURE} =     ${{ bytes.fromhex('89504e470d0a1a0a') }}
# The body ends long after the limit, so a wait for the whole body fails the limit
# instead of hanging, while a normal return stays far below it.
${SLOW_BODY_MS} =      20000
${RETURN_LIMIT_S} =    10

*** Test Cases ***
Response All Headers Contain Set-Cookie
    ${response} =    Capture Response    /api/set-cookies
    Should Contain    ${response.allHeaders}[set-cookie]    session=abc
    Should Contain    ${response.allHeaders}[set-cookie]    theme=dark
    ${set_cookies} =    Header Values    ${response.headersArray}    set-cookie
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
    Should Be Equal    ${response.httpVersion}    ${None}
    Should Be Equal    ${response.serverAddr}    ${None}

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
    ${promise} =    Promise To    Wait For Request    **/api/get/json    wait_for_all_fields=True
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
    ${promise} =    Promise To    Wait For Request    **/posted.html
    Evaluate JavaScript
    ...    ${None}
    ...    () => fetch('/posted.html', {method: 'POST', headers: {'content-type': 'application/x-www-form-urlencoded'}, body: 'name=George&city=Helsinki'})
    ${request} =    Wait For    ${promise}
    Should Be Equal    ${request.postDataJSON}    ${{ {'name': 'George', 'city': 'Helsinki'} }}
    Should Be Equal    ${request.postDataBuffer}    ${{ b'name=George&city=Helsinki' }}
    Should Be Equal    ${request.postData}    name=George&city=Helsinki

Wait For Request Returns Before The Response Arrives
    ${promise} =    Promise To    Wait For Request    **/api/stalled-image    timeout=3s
    Evaluate JavaScript    ${None}    () => { fetch('/api/stalled-image'); }
    ${request} =    Wait For    ${promise}
    Should End With    ${request.url}    /api/stalled-image
    Should Be Equal    ${request.allHeaders}    ${None}
    Should Be Equal    ${request.headersArray}    ${None}

Waiting For All Request Fields Is Limited By The Timeout
    ${promise} =    Promise To    Wait For Request
    ...    **/api/stalled-image    timeout=1s    wait_for_all_fields=True
    Evaluate JavaScript    ${None}    () => { fetch('/api/stalled-image'); }
    IF    '${BROWSER}' == 'firefox'
        ${request} =    Wait For    ${promise}
        Should Not Be Empty    ${request.allHeaders}
    ELSE
        Run Keyword And Expect Error
        ...    *Timeout 1000ms exceeded while waiting for all fields of the request.*
        ...    Wait For    ${promise}
    END

Response Without Body Returns Before A Slow Body Arrives
    ${started} =    Evaluate    time.monotonic()    modules=time
    ${promise} =    Promise To    Wait For Response
    ...    **/api/slow-body*    timeout=15s    include_body=False
    Evaluate JavaScript    ${None}    () => { fetch('/api/slow-body?bodyMs=${SLOW_BODY_MS}'); }
    ${response} =    Wait For    ${promise}
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.bytes}    ${None}
    Should Be Equal    ${response.securityDetails}    ${None}
    Seconds Since Should Be Below    ${started}    ${RETURN_LIMIT_S}

Reading A Slow Body Is Limited By The Timeout
    ${started} =    Evaluate    time.monotonic()    modules=time
    ${promise} =    Promise To    Wait For Response    **/api/slow-body*    timeout=3s
    Evaluate JavaScript    ${None}    () => { fetch('/api/slow-body?bodyMs=${SLOW_BODY_MS}'); }
    Run Keyword And Expect Error
    ...    *Timeout 3000ms exceeded while waiting for all fields of the response.*
    ...    Wait For    ${promise}
    Seconds Since Should Be Below    ${started}    ${RETURN_LIMIT_S}

*** Keywords ***
Capture Response
    [Arguments]    ${path}
    ${promise} =    Promise To    Wait For Response    **${path}
    HTTP    ${path}
    ${response} =    Wait For    ${promise}
    RETURN    ${response}

Seconds Since Should Be Below
    [Arguments]    ${started}    ${limit}
    ${elapsed} =    Evaluate    time.monotonic() - ${started}    modules=time
    Should Be True    ${elapsed} < ${limit}
    ...    Returned after ${elapsed}s, expected below ${limit}s.
