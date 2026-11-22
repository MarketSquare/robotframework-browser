*** Settings ***
Library        ../../library/http_test_page.py
Resource       imports.resource

Suite Setup    Open Context With Base URL

*** Test Cases ***
Relative URL Is Resolved Against The Base URL Of The Context
    ${response} =    Send API Request    /api/echo/base
    Should Be Equal    ${response.url}    ${STATIC_URL}api/echo/base
    Should Be Equal    ${response.json.path}    /api/echo/base

Absolute URL Ignores The Base URL
    ${response} =    Send API Request    ${OTHER_ORIGIN_ROOT_URL}api/echo/absolute
    Should Be Equal    ${response.url}    ${OTHER_ORIGIN_ROOT_URL}api/echo/absolute

Method Is Sent
    ${response} =    Send API Request    /api/echo/method    DELETE
    Should Be Equal    ${response.json.method}    DELETE

Response Has Status Headers And Body Views
    ${url} =    Respond Url    status=201    statusText=Made    contentType=application/json    body={"name": "robot"}
    ${response} =    Send API Request    ${url}
    Should Be Equal    ${response.status}    ${201}
    Should Be Equal    ${response.statusText}    Made
    Should Be Equal    ${response.ok}    ${True}
    Should Start With    ${response.headers['content-type']}    application/json
    Should Be Equal    ${response.text}    {"name": "robot"}
    Should Be Equal    ${response.bytes}    ${{ b'{"name": "robot"}' }}
    Should Be Equal    ${response.json}    ${{ {'name': 'robot'} }}

JSON Is None For A Body That Is Not JSON
    ${url} =    Respond Url    body=hello
    ${response} =    Send API Request    ${url}
    Should Be Equal    ${response.text}    hello
    Should Be Equal    ${response.json}    ${None}

Binary Response Arrives Byte For Byte In Bytes
    ${sha256} =    HTTP Fixture Sha256    image.png
    ${response} =    Send API Request    /api/respond/img?file=image.png
    ${received} =    Sha256 Of Bytes    ${response.bytes}
    Should Be Equal    ${received}    ${sha256}

Headers Array Has Every Header With Its Original Name
    ${url} =    Respond Url    header=X-Robot:Beep    body=ok
    ${response} =    Send API Request    ${url}
    Should Be Equal    ${response.headers['x-robot']}    Beep
    Should Contain    ${response.headersArray}    ${{ {'name': 'X-Robot', 'value': 'Beep'} }}

Error Status Does Not Fail By Default
    ${url} =    Respond Url    status=404    body=missing
    ${response} =    Send API Request    ${url}
    Should Be Equal    ${response.status}    ${404}
    Should Be Equal    ${response.ok}    ${False}
    Should Be Equal    ${response.text}    missing

Error Status Fails With Fail On Status Code
    ${url} =    Respond Url    status=404    body=missing
    Run Keyword And Expect Error    *404*
    ...    Send API Request    ${url}    failOnStatusCode=True

Request Headers Are Sent
    &{headers} =    Create Dictionary    X-Robot=Beep
    ${response} =    Send API Request    /api/echo/headers    headers=${headers}
    Should Be Equal    ${response.json.headers['x-robot']}    Beep

Headers That A Page Cannot Set Are Sent
    &{headers} =    Create Dictionary    Origin=http://example.test
    ${response} =    Send API Request    /api/echo/origin    headers=${headers}
    Should Be Equal    ${response.json.headers.origin}    http://example.test

Cross Origin Response Without CORS Is Read
    ${response} =    Send API Request    ${OTHER_ORIGIN_ROOT_URL}api/echo/no-cors?cors=off
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.json.path}    /api/echo/no-cors

Params From A Dictionary Are Added To The Query
    &{params} =    Create Dictionary    q=a&b c    n=${1}    flag=${True}
    ${response} =    Send API Request    /api/echo/params?page=2    params=${params}
    Should Be Equal    ${response.json.query}    ${{ {'page': '2', 'q': 'a&b c', 'n': '1', 'flag': 'true'} }}

Params As A String Are Appended As Given
    ${response} =    Send API Request    /api/echo/params?page=2    params=q=a%20b&n=1
    Should Be Equal    ${response.json.query}    ${{ {'page': '2', 'q': 'a b', 'n': '1'} }}

Dictionary Data Is Sent As JSON
    &{data} =    Create Dictionary    name=robot    legs=${2}
    ${response} =    Send API Request    /api/echo/json    POST    data=${data}
    Should Start With    ${response.json.body.contentType}    application/json
    Should Be Equal    ${response.json.body.json}    ${{ {'name': 'robot', 'legs': 2} }}

String Data Is Sent As Given With Octet Stream Content Type
    ${response} =    Send API Request    /api/echo/text    POST    data={"name": "robot"}
    Should Be Equal    ${response.json.body.contentType}    application/octet-stream
    Should Be Equal    ${response.json.body.text}    {"name": "robot"}

String Data That Is JSON Is Sent As Given With A JSON Content Type
    &{headers} =    Create Dictionary    Content-Type=application/json
    ${response} =    Send API Request    /api/echo/json    POST    headers=${headers}    data={"name": "robot"}
    Should Be Equal    ${response.json.body.text}    {"name": "robot"}

String Data That Is Not JSON Is Encoded As JSON With A JSON Content Type
    &{headers} =    Create Dictionary    Content-Type=application/json
    ${response} =    Send API Request    /api/echo/json    POST    headers=${headers}    data=hello
    Should Be Equal    ${response.json.body.text}    "hello"

Bytes Data Arrives Byte For Byte
    ${sha256} =    HTTP Fixture Sha256    random.bin
    ${data} =    HTTP Fixture Bytes    random.bin
    ${response} =    Send API Request    /api/echo/raw    PUT    data=${data}
    Should Be Equal    ${response.json.body.sha256}    ${sha256}
    Should Be Equal    ${response.json.body.size}    ${4096}

Form Is Sent URL Encoded
    &{fields} =    Create Dictionary    q=a&b=c d    lang=en
    ${response} =    Send API Request    /api/echo/form    POST    form=${fields}
    Should Start With    ${response.json.body.contentType}    application/x-www-form-urlencoded
    Should Be Equal    ${response.json.body.text}    q=a%26b%3Dc+d&lang=en

Multipart Sends Fields And A File From Path
    ${sha256} =    HTTP Fixture Sha256    image.jpg
    ${path} =    HTTP Fixture Path    image.jpg
    &{file} =    Create Dictionary    path=${path}
    &{fields} =    Create Dictionary    description=avatar    file=${file}
    ${response} =    Send API Request    /api/echo/upload    POST    multipart=${fields}
    ${parts} =    Set Variable    ${response.json.parts}
    Should Be Equal    ${parts}[0][name]    description
    Should Be Equal    ${parts}[0][text]    avatar
    Should Be Equal    ${parts}[1][name]    file
    Should Be Equal    ${parts}[1][filename]    image.jpg
    Should Be Equal    ${parts}[1][mimeType]    image/jpeg
    Should Be Equal    ${parts}[1][sha256]    ${sha256}

Multipart Sends A File From Buffer
    &{file} =    Create Dictionary    name=notes.txt    mimeType=text/plain    buffer=häkä €
    &{fields} =    Create Dictionary    file=${file}
    ${response} =    Send API Request    /api/echo/upload    POST    multipart=${fields}
    ${part} =    Set Variable    ${response.json.parts}[0]
    Should Be Equal    ${part}[filename]    notes.txt
    Should Be Equal    ${part}[mimeType]    text/plain
    ${sha256} =    Sha256 Of Bytes    ${{ 'häkä €'.encode('utf-8') }}
    Should Be Equal    ${part}[sha256]    ${sha256}

Nested Form Value Fails Before Sending
    &{fields} =    Create Dictionary    q=${{ {'a': 1} }}
    Run Keyword And Expect Error
    ...    *cannot be converted to FormFields: Field 'q' must be a string, a number or a boolean, got a dictionary.
    ...    Send API Request    /api/echo/form    POST    form=${fields}

Data Together With Form Fails
    &{fields} =    Create Dictionary    q=1
    Run Keyword And Expect Error    *Only one of 'data', 'form' or 'multipart' can be specified*
    ...    Send API Request    /api/echo/form    POST    data=x    form=${fields}

Data Together With An Empty Form Fails
    Run Keyword And Expect Error    *Only one of 'data', 'form' or 'multipart' can be specified*
    ...    Send API Request    /api/echo/form    POST    data=x    form=${{ {} }}

Empty Form Is Sent As An Empty URL Encoded Body
    ${response} =    Send API Request    /api/echo/form    POST    form=${{ {} }}
    Should Start With    ${response.json.body.contentType}    application/x-www-form-urlencoded
    Should Be Equal    ${response.json.body.size}    ${0}

Cookies Of The Context Are Sent
    Add Cookie    flavour    oat    url=${STATIC_URL}
    ${response} =    Send API Request    /api/echo/cookie
    Should Contain    ${response.json.headers.cookie}    flavour=oat
    [Teardown]    Delete All Cookies

Cookie Set By An API Response Is Shared With The Page
    ${url} =    Respond Url    header=Set-Cookie:flavour=rye; Path=/    body=ok
    Send API Request    ${url}
    ${cookie} =    Get Cookie    flavour
    Should Be Equal    ${cookie.value}    rye
    ${response} =    HTTP    /api/echo/cookie
    Should Contain    ${response.json.headers.cookie}    flavour=rye
    [Teardown]    Delete All Cookies

Redirect Is Followed By Default
    ${url} =    Respond Url    status=302    header=Location:/api/echo/target
    ${response} =    Send API Request    ${url}
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.url}    ${STATIC_URL}api/echo/target

Max Redirects Zero Returns The Redirect Response
    ${url} =    Respond Url    status=302    header=Location:/api/echo/target
    ${response} =    Send API Request    ${url}    maxRedirects=0
    Should Be Equal    ${response.status}    ${302}
    Should Be Equal    ${response.headers.location}    /api/echo/target

Negative Max Retries Fails
    Run Keyword And Expect Error    *'maxRetries' must be greater than or equal to '0'*
    ...    Send API Request    /api/echo/retries    maxRetries=-1

Request Slower Than Timeout Fails
    ${url} =    Respond Url    delay=2000    body=late
    Run Keyword And Expect Error    *Timeout 500ms exceeded*
    ...    Send API Request    ${url}    timeout=500ms

Library Timeout Applies Without Timeout Argument
    Set Browser Timeout    500ms    scope=Test
    ${url} =    Respond Url    delay=2000    body=late
    Run Keyword And Expect Error    *Timeout 500ms exceeded*
    ...    Send API Request    ${url}

Timeout Zero Waits Without Limit
    Set Browser Timeout    500ms    scope=Test
    ${url} =    Respond Url    delay=1000    body=late
    ${response} =    Send API Request    ${url}    timeout=0
    Should Be Equal    ${response.text}    late

Wait For Response Does Not See An API Request
    ${promise} =    Promise To    Wait For Response    **/api/echo/unseen    timeout=1s
    Send API Request    /api/echo/unseen
    Run Keyword And Expect Error    *Timeout 1000ms exceeded*    Wait For    ${promise}

Route Rule Does Not Abort An API Request
    ${rule} =    Abort Requests    **/api/echo/not-routed
    ${response} =    Send API Request    /api/echo/not-routed
    Should Be Equal    ${response.status}    ${200}
    [Teardown]    Remove Route Rule    ${rule}

Works Without An Open Page
    Close Page    ALL
    ${response} =    Send API Request    /api/echo/no-page
    Should Be Equal    ${response.status}    ${200}
    [Teardown]    New Page    ${HTTP_URL}

Fails Without An Open Context
    Close Context    ALL
    Run Keyword And Expect Error    *no context was open*
    ...    Send API Request    /api/echo/no-context
    [Teardown]    Open Context With Base URL    new_browser=False

*** Keywords ***
Open Context With Base URL
    [Arguments]    ${new_browser}=${True}
    IF    ${new_browser}    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Context    baseURL=${STATIC_URL}
    New Page    ${HTTP_URL}
