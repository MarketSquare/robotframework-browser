*** Settings ***
Library        ../../library/http_test_page.py
Resource       imports.resource

Suite Setup    New Page    ${HTTP_URL}

Test Tags      no-iframe

*** Test Cases ***
HEAD Request Returns Headers Without Body
    ${response} =    HTTP    /api/echo/head    HEAD
    Should Be Equal    ${response.status}    ${200}
    Should Contain    ${response.headers['content-type']}    application/json
    Should Be Equal    ${response.bytes}    ${{ b'' }}

Body Of GET Request Is Not Sent
    ${response} =    HTTP    /api/echo/get    GET    {"name": "robot"}
    Should Be Equal    ${response.json.method}    GET
    Should Be Equal    ${response.json.body.size}    ${0}

OPTIONS Request Reaches The Server
    ${response} =    HTTP    /api/echo/options    OPTIONS
    Should Be Equal    ${response.json.method}    OPTIONS

Binary Response Arrives Byte For Byte In Bytes
    ${sha256} =    HTTP Fixture Sha256    image.png
    ${response} =    HTTP    /api/respond/img?file=image.png
    ${received} =    Sha256 Of Bytes    ${response.bytes}
    Should Be Equal    ${received}    ${sha256}

Text Decodes Invalid UTF-8 With Replacement Characters
    ${response} =    HTTP    /api/get/bad_binary
    Should Be Equal    ${response.text}    ${{ bytes.fromhex('89504e470d0a1a0a').decode('utf-8', 'replace') }}

JSON Is Parsed Regardless Of Content Type While Legacy Body Stays Text
    ${url} =    Respond Url    contentType=text/plain    body={"name": "robot"}
    ${response} =    HTTP    ${url}
    Should Be Equal    ${response.json}    ${{ {'name': 'robot'} }}
    Should Be Equal    ${response.body}    {"name": "robot"}
    Should Be Equal    ${response.text}    {"name": "robot"}

JSON Is None For A Body That Is Not JSON
    ${url} =    Respond Url    body=hello
    ${response} =    HTTP    ${url}
    Should Be Equal    ${response.text}    hello
    Should Be Equal    ${response.json}    ${None}

Empty Response Body Gives Empty Views
    ${url} =    Respond Url    body=${EMPTY}
    ${response} =    HTTP    ${url}
    Should Be Equal    ${response.bytes}    ${{ b'' }}
    Should Be Equal    ${response.text}    ${EMPTY}
    Should Be Equal    ${response.json}    ${None}

Same Origin Response Has Type Basic
    ${response} =    HTTP    /api/echo/basic
    Should Be Equal    ${response.type}    basic
    Should Be Equal    ${response.redirected}    ${False}

Cross Origin Response Has Type Cors
    ${response} =    HTTP    ${OTHER_ORIGIN_ROOT_URL}api/echo/cross
    Should Be Equal    ${response.type}    cors

Bytes Body Arrives Byte For Byte
    ${sha256} =    HTTP Fixture Sha256    random.bin
    ${data} =    HTTP Fixture Bytes    random.bin
    ${response} =    HTTP    /api/echo/raw    PUT    ${data}
    Should Be Equal    ${response.json.body.sha256}    ${sha256}
    Should Be Equal    ${response.json.body.size}    ${4096}

Form Is Sent URL Encoded
    &{fields} =    Create Dictionary    q=a&b=c d    lang=en
    ${response} =    HTTP    /api/echo/form    POST    form=${fields}
    Should Start With    ${response.json.body.contentType}    application/x-www-form-urlencoded
    Should Be Equal    ${response.json.body.text}    q=a%26b%3Dc+d&lang=en

Multipart Sends Fields And A File From Path
    ${sha256} =    HTTP Fixture Sha256    image.jpg
    ${path} =    HTTP Fixture Path    image.jpg
    &{file} =    Create Dictionary    path=${path}
    &{fields} =    Create Dictionary    description=avatar    file=${file}
    ${response} =    HTTP    /api/echo/upload    POST    multipart=${fields}
    ${parts} =    Set Variable    ${response.json.parts}
    Should Be Equal    ${parts}[0][name]    description
    Should Be Equal    ${parts}[0][text]    avatar
    Should Be Equal    ${parts}[1][name]    file
    Should Be Equal    ${parts}[1][filename]    image.jpg
    Should Be Equal    ${parts}[1][mimeType]    image/jpeg
    Should Be Equal    ${parts}[1][sha256]    ${sha256}

Multipart Sends A File From Buffer
    &{file} =    Create Dictionary    name=notes.txt    mimeType=text/plain    buffer=${{ b'hello' }}
    &{fields} =    Create Dictionary    file=${file}
    ${response} =    HTTP    /api/echo/upload    POST    multipart=${fields}
    ${part} =    Set Variable    ${response.json.parts}[0]
    Should Be Equal    ${part}[filename]    notes.txt
    Should Be Equal    ${part}[mimeType]    text/plain
    Should Be Equal    ${part}[size]    ${5}
    ${sha256} =    Sha256 Of Bytes    ${{ b'hello' }}
    Should Be Equal    ${part}[sha256]    ${sha256}

Multipart Sends A Text Buffer As UTF-8
    &{file} =    Create Dictionary    name=notes.txt    mimeType=text/plain    buffer=häkä €
    &{fields} =    Create Dictionary    file=${file}
    ${response} =    HTTP    /api/echo/upload    POST    multipart=${fields}
    ${part} =    Set Variable    ${response.json.parts}[0]
    Should Be Equal    ${part}[filename]    notes.txt
    ${sha256} =    Sha256 Of Bytes    ${{ 'häkä €'.encode('utf-8') }}
    Should Be Equal    ${part}[sha256]    ${sha256}

Own Content Type In Lower Case Is Kept For A JSON Body
    &{headers} =    Create Dictionary    content-type=text/plain
    ${response} =    HTTP    /api/echo/json    POST    {"name": "robot"}    ${headers}
    Should Be Equal    ${response.json.headers['content-type']}    text/plain

Bytes Body With GET Fails
    Run Keyword And Expect Error    *GET request cannot have a body, got bytes*
    ...    HTTP    /api/echo/get    GET    ${{ b'raw' }}

Body Together With Form Fails
    &{fields} =    Create Dictionary    q=1
    Run Keyword And Expect Error    *Only one of*
    ...    HTTP    /api/echo/form    POST    {"q": 1}    form=${fields}

Body Together With Multipart Fails
    &{fields} =    Create Dictionary    q=1
    Run Keyword And Expect Error    *Only one of*
    ...    HTTP    /api/echo/upload    POST    {"q": 1}    multipart=${fields}

Form With GET Fails
    &{fields} =    Create Dictionary    q=1
    Run Keyword And Expect Error    *GET request cannot have a body, got form*
    ...    HTTP    /api/echo/form    GET    form=${fields}

Multipart With HEAD Fails
    &{fields} =    Create Dictionary    q=1
    Run Keyword And Expect Error    *HEAD request cannot have a body, got multipart*
    ...    HTTP    /api/echo/upload    HEAD    multipart=${fields}

Cookies Of The Context Are Sent By Default
    Add Cookie    flavour    oat    url=${ROOT_URL}
    ${response} =    HTTP    /api/echo/cookie
    Should Contain    ${response.json.headers.cookie}    flavour=oat
    [Teardown]    Delete All Cookies

Credentials Omit Sends No Cookies
    Add Cookie    flavour    oat    url=${ROOT_URL}
    ${response} =    HTTP    /api/echo/cookie    credentials=omit
    Dictionary Should Not Contain Key    ${response.json.headers}    cookie
    [Teardown]    Delete All Cookies

Redirect Is Followed By Default
    ${url} =    Respond Url    status=302    header=Location:/api/echo/target
    ${response} =    HTTP    ${url}
    Should Be Equal    ${response.redirected}    ${True}
    Should End With    ${response.url}    /api/echo/target

Redirect Manual Returns An Opaque Redirect
    ${url} =    Respond Url    status=302    header=Location:/api/echo/target
    ${response} =    HTTP    ${url}    redirect=manual
    Should Be Equal    ${response.type}    opaqueredirect
    Should Be Equal    ${response.status}    ${0}

Redirect Error Fails On A Redirect
    ${url} =    Respond Url    status=302    header=Location:/api/echo/target
    Run Keyword And Expect Error    *TypeError*
    ...    HTTP    ${url}    redirect=error

Mode No Cors Returns An Opaque Response
    ${response} =    HTTP    ${OTHER_ORIGIN_ROOT_URL}api/echo/opaque    mode=no-cors
    Should Be Equal    ${response.type}    opaque
    Should Be Equal    ${response.status}    ${0}
    Should Be Equal    ${response.bytes}    ${{ b'' }}

Cache Reload Asks The Server For A Fresh Response
    ${response} =    HTTP    /api/echo/cache    cache=reload
    Should Be Equal    ${response.json.headers['cache-control']}    no-cache

Referrer Is Sent
    ${response} =    HTTP    /api/echo/referrer    referrer=${ROOT_URL}referrer-source
    Should Be Equal    ${response.json.headers.referer}    ${ROOT_URL}referrer-source

Referrer Policy No Referrer Sends No Referer
    ${response} =    HTTP    /api/echo/referrer    referrerPolicy=no-referrer
    Dictionary Should Not Contain Key    ${response.json.headers}    referer

Matching Integrity Is Accepted
    ${integrity} =    HTTP Fixture Integrity    random.bin
    ${response} =    HTTP    /api/respond/raw?file=random.bin    integrity=${integrity}
    Should Be Equal    ${response.status}    ${200}

Wrong Integrity Fails
    Run Keyword And Expect Error    *TypeError*
    ...    HTTP    /api/respond/raw?file=random.bin    integrity=sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=

Keepalive And Priority Are Accepted
    ${response} =    HTTP    /api/echo/hints    keepalive=True    priority=high
    Should Be Equal    ${response.status}    ${200}

Request Slower Than Timeout Fails
    ${url} =    Respond Url    delay=2000    body=late
    Run Keyword And Expect Error    *Timeout 500ms exceeded*
    ...    HTTP    ${url}    timeout=500ms

Library Timeout Applies Without Timeout Argument
    Set Browser Timeout    500ms    scope=Test
    ${url} =    Respond Url    delay=2000    body=late
    Run Keyword And Expect Error    *Timeout 500ms exceeded*
    ...    HTTP    ${url}

Timeout Zero Waits Without Limit
    Set Browser Timeout    500ms    scope=Test
    ${url} =    Respond Url    delay=1000    body=late
    ${response} =    HTTP    ${url}    timeout=0
    Should Be Equal    ${response.text}    late
