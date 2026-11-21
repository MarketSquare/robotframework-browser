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

Respond Rejects An Unknown Fixture
    &{response} =    HTTP    /api/respond/x?file=../server.js
    Should Be Equal    ${response.status}    ${404}

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
