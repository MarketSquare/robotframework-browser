*** Settings ***
Library        ../../library/http_test_page.py
Resource       imports.resource

Suite Setup    New Page    ${HTTP_URL}

Test Tags      no-iframe

*** Test Cases ***
HTTP Keyword Request Is Echoed Back
    &{response} =    HTTP    /api/echo/keyword?q=1    POST    {"name": "robot"}    headers={"X-Tenant": "a"}
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.body.method}    POST
    Should Be Equal    ${response.body.path}    /api/echo/keyword
    Should Be Equal    ${response.body.query.q}    1
    Should Be Equal    ${response.body.headers['x-tenant']}    a
    Should Be Equal    ${response.body.body.json.name}    robot

Fetch From The Page Shows The Echoed Request
    ${url} =    HTTP Page Url
    ...    ${HTTP_URL}
    ...    method=POST
    ...    url=/api/echo/page
    ...    bodyMode=json
    ...    body={"name": "robot"}
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    200
    Get Text    id=response-body    contains    "name": "robot"
    Get Text    id=history    contains    fetch POST /api/echo/page -> 200

XMLHttpRequest From The Page Sends Its Headers
    ${url} =    HTTP Page Url    ${HTTP_URL}    kind=xhr    url=/api/echo/xhr    headers={"X-Tenant": "b"}
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    200
    Get Text    id=response-body    contains    "x-tenant": "b"

Image Load Shows The Fixture Image
    ${url} =    HTTP Page Url    ${HTTP_URL}    kind=img    url=/api/respond/img?file=image.png
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    ==    image 64x48
    Get Element States    id=response-image    contains    visible

Fetched Fixture Image Arrives Byte For Byte
    ${sha256} =    HTTP Fixture Sha256    image.png
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=/api/respond/img?file=image.png
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-sha256    ==    ${sha256}
    Get Text    id=response-size    ==    6302
    Get Element States    id=response-image    contains    visible

Raw Binary Body Arrives Byte For Byte
    ${sha256} =    HTTP Fixture Sha256    random.bin
    ${url} =    HTTP Page Url
    ...    ${HTTP_URL}
    ...    method=PUT
    ...    url=/api/echo/raw
    ...    bodyMode=raw-file
    ...    fixture=random.bin
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    contains    "sha256": "${sha256}"
    Get Text    id=response-body    contains    "size": 4096

File Uploaded Through The File Input Arrives Byte For Byte
    ${sha256} =    HTTP Fixture Sha256    image.jpg
    ${path} =    HTTP Fixture Path    image.jpg
    ${url} =    HTTP Page Url    ${HTTP_URL}    send=False    method=POST    url=/api/echo/upload
    ...    bodyMode=multipart    body={"description": "avatar"}
    Go To    ${url}
    Upload File By Selector    id=file    ${path}
    Click    id=send
    Get Text    id=state    ==    done
    Get Text    id=response-body    contains    "filename": "image.jpg"
    Get Text    id=response-body    contains    "sha256": "${sha256}"
    Get Text    id=response-body    contains    "text": "avatar"

Uploaded File Keeps Its Non ASCII Name
    ${path} =    HTTP Fixture Path    image.png
    Copy File    ${path}    ${OUTPUT_DIR}/http-upload/bild-ä.png
    ${url} =    HTTP Page Url    ${HTTP_URL}    send=False    method=POST    url=/api/echo/upload
    ...    bodyMode=multipart
    Go To    ${url}
    Upload File By Selector    id=file    ${OUTPUT_DIR}/http-upload/bild-ä.png
    Click    id=send
    Get Text    id=state    ==    done
    Get Text    id=response-body    contains    "filename": "bild-ä.png"

Uploaded Buffer With Non ASCII Text Arrives As UTF-8
    VAR    ${text} =    Grüße aus Köln – ✓ 日本
    ${sha256} =    Sha256 Of Bytes    ${{ $text.encode("utf-8") }}
    ${url} =    HTTP Page Url    ${HTTP_URL}    send=False    method=POST    url=/api/echo/upload
    ...    bodyMode=multipart
    Go To    ${url}
    VAR    &{buffer} =    name=gruesse.txt    mimeType=text/plain    buffer=${text}
    Upload File By Selector    id=file    ${buffer}
    Click    id=send
    Get Text    id=state    ==    done
    Get Text    id=response-body    contains    "filename": "gruesse.txt"
    Get Text    id=response-body    contains    "sha256": "${sha256}"

Uploaded Buffer Keeps Its Explicit MIME Type
    ${url} =    HTTP Page Url    ${HTTP_URL}    send=False    method=POST    url=/api/echo/upload
    ...    bodyMode=multipart
    Go To    ${url}
    VAR    &{buffer} =    name=data.bin    mimeType=application/json    buffer={"a": 1}
    Upload File By Selector    id=file    ${buffer}
    Click    id=send
    Get Text    id=state    ==    done
    Get Text    id=response-body    contains    "filename": "data.bin"
    Get Text    id=response-body    contains    "mimeType": "application/json"

Multipart Parts Are Echoed In The Order They Were Sent
    VAR    &{file} =    name=first    filename=first.txt    value=file content
    VAR    &{field} =    name=second    value=field value
    ${body} =    Multipart Body    boundary-1    ${file}    ${field}
    &{response} =    HTTP    /api/echo/order    POST    ${body}
    ...    headers={"Content-Type": "multipart/form-data; boundary=boundary-1"}
    Should Be Equal    ${response.body.parts[0].name}    first
    Should Be Equal    ${response.body.parts[0].filename}    first.txt
    Should Be Equal    ${response.body.parts[1].name}    second

Multipart Text Field Larger Than One MiB Is Echoed Whole
    ${value} =    Evaluate    "x" * 1100000
    VAR    &{field} =    name=big    value=${value}
    ${body} =    Multipart Body    boundary-2    ${field}
    &{response} =    HTTP    /api/echo/big    POST    ${body}
    ...    headers={"Content-Type": "multipart/form-data; boundary=boundary-2"}
    Should Be Equal    ${response.body.parts[0].size}    ${1100000}
    Should Be Equal    ${response.body.parts[0].truncated}    ${False}

Invalid Multipart Body Is Still Echoed
    &{response} =    HTTP    /api/echo/broken    POST    abc
    ...    headers={"Content-Type": "multipart/form-data"}
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.body.body.text}    abc
    Should Be Equal    ${response.body.parts}    ${None}
    Should Not Be Empty    ${response.body.partsError}

Multipart Body Cut Off Inside A File Is Still Echoed
    ${body} =    Catenate    SEPARATOR=\r\n
    ...    --boundary-3
    ...    Content-Disposition: form-data; name="file"; filename="cut.txt"
    ...    Content-Type: text/plain
    ...    ${EMPTY}
    ...    no closing boundary
    &{response} =    HTTP    /api/echo/cut    POST    ${body}
    ...    headers={"Content-Type": "multipart/form-data; boundary=boundary-3"}
    Should Be Equal    ${response.status}    ${200}
    Should Be Equal    ${response.body.parts}    ${None}
    Should Be Equal    ${response.body.partsError}    Unexpected end of form
    &{response} =    HTTP    /api/echo/after-cut
    Should Be Equal    ${response.status}    ${200}

Form Submit Shows The Echo In The Panel
    ${url} =    HTTP Page Url    ${HTTP_URL}    kind=form    method=POST    url=/api/echo/form
    ...    bodyMode=form-urlencoded    body={"name": "robot"}
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    contains    "text": "name=robot"
    Get Text    id=response-body    contains    application/x-www-form-urlencoded

Respond Sets Status, Status Text, Header And Body
    ${url} =    HTTP Page Url    ${HTTP_URL}
    ...    url=/api/respond/custom?status=503&statusText=Busy&header=X-Custom:yes&body=hello
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    503
    Get Text    id=status-text    ==    Busy
    Get Text    id=response-headers    contains    "x-custom": "yes"
    Get Text    id=response-body    ==    hello

Respond Serves Only Files Inside The Fixtures Folder
    &{response} =    HTTP    /api/respond/x?file=../http.html
    Should Be Equal    ${response.status}    ${404}
    Should Be Equal    ${response.body.error}    Unknown fixture: ../http.html

Respond Rejects An Invalid Status With A Clear Error
    &{response} =    HTTP    /api/respond/x?status=abc
    Should Be Equal    ${response.status}    ${400}
    Should Start With    ${response.body.error}    Invalid status: abc

Respond Rejects An Invalid Header With A Clear Error
    &{response} =    HTTP    /api/respond/x?header=bad%20name:1
    Should Be Equal    ${response.status}    ${400}
    Should Start With    ${response.body.error}    Invalid header: bad name:1

Cross Origin Fetch With A Custom Header Is Allowed
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${OTHER_ORIGIN_ROOT_URL}api/echo/cross
    ...    headers={"X-Tenant": "c"}
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    200
    Get Text    id=response-body    contains    "x-tenant": "c"
    Get Text    id=response-body    contains    "origin": "http://${SERVER}"

Cross Origin Fetch Is Blocked When CORS Is Off
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${OTHER_ORIGIN_ROOT_URL}api/echo/cross?cors=off
    Go To    ${url}
    Get Text    id=state    ==    error

Cross Origin Basic Auth Challenge Is Readable With Credentials
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${OTHER_ORIGIN_ROOT_URL}api/basic-auth/robot/secret
    ...    credentials=include
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    401
    Get Text    id=response-headers    contains    "www-authenticate": "Basic realm=\\"test-app\\""

Basic Auth Endpoint Rejects A Request Without Credentials
    &{response} =    HTTP    /api/basic-auth/robot/secret
    Should Be Equal    ${response.status}    ${401}
    Should Be Equal    ${response.headers['www-authenticate']}    Basic realm="test-app"

Extra HTTP Headers Of New Context Reach The Server
    [Setup]    New Context    extraHTTPHeaders={"X-Tenant": "from-context"}
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=/api/echo/context
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    contains    "x-tenant": "from-context"
    &{response} =    HTTP    /api/echo/keyword
    Should Be Equal    ${response.body.headers['x-tenant']}    from-context
    [Teardown]    Close Context

HTTP Credentials Of New Context Pass Basic Auth
    VAR    ${username} =    robot
    VAR    ${password} =    secret
    New Context    httpCredentials={'username': '$username', 'password': '$password'}
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=/api/basic-auth/robot/secret
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    200
    Get Text    id=response-body    contains    "authenticatedUser": "robot"
    [Teardown]    Close Context

Query Key Named Proto Is Echoed
    &{response} =    HTTP    /api/echo/x?__proto__=1&a=2
    Should Be Equal    ${response.body.query}[__proto__]    1
    Should Be Equal    ${response.body.query}[a]    2

GET Form Submit Keeps The Query Of Its URL
    ${url} =    HTTP Page Url    ${HTTP_URL}    kind=form    method=GET    url=/api/respond/x?body=hello
    ...    bodyMode=form-urlencoded    body={"name": "robot"}
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    ==    hello

Response Body Is Shown Exactly As Received
    ${url} =    HTTP Page Url    ${HTTP_URL}
    ...    url=/api/respond/x?contentType=application/json&body={"b":1,"2":0,"price":1.50}
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    ==    {"b":1,"2":0,"price":1.50}

Panel Shows The Latest Request When An Earlier One Answers Later
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=/api/respond/slow?delay=1000&body=first
    Go To    ${url}
    Fill Text    id=url    /api/respond/fast?body=second
    Click    id=send
    Get Element Count    css=#history li    ==    2
    Get Text    id=response-body    ==    second
    Get Text    id=request-count    ==    2

Unknown Prefill Value Is Reported Instead Of Sent
    ${url} =    HTTP Page Url    ${HTTP_URL}    method=POST    bodyMode=JSON    body={"a": 1}
    Go To    ${url}
    Get Text    id=state    ==    error
    Get Text    id=error    ==    unknown bodyMode: JSON
    Get Text    id=request-count    ==    0

Image Load Answering After A Later One Keeps Its History Entry
    ${url} =    HTTP Page Url    ${HTTP_URL}    kind=img    url=/api/respond/slow?delay=1000&file=image.png
    # The pending image would hold back the load event until it answers.
    Go To    ${url}    wait_until=domcontentloaded
    Fill Text    id=url    /api/respond/fast?file=image.png
    Click    id=send
    Get Element Count    css=#history li    ==    2
    Get Text    css=#history li >> nth=0    ==    img GET /api/respond/fast?file=image.png -> loaded 64x48
    Get Text    css=#history li >> nth=1    ==    img GET /api/respond/slow?delay=1000&file=image.png -> loaded 64x48
    Get Text    id=state    ==    done
    Get Element States    id=response-image    contains    visible

Form Fields Named Like Form Properties Are Submitted
    ${url} =    HTTP Page Url    ${HTTP_URL}    kind=form    method=POST    url=/api/echo/form
    ...    bodyMode=form-urlencoded    body={"submit": "go", "action": "x", "appendChild": "y"}
    Go To    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-url    ==    ${ROOT_URL}api/echo/form?format=html
    Get Text    id=response-body    contains    "text": "submit=go&action=x&appendChild=y"
