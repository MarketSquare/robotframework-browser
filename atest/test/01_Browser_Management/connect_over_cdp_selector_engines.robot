*** Settings ***
Documentation    A context that exists when Connect To Browser attaches over CDP gets the
...              selector engines registered before the connection.

Library          Browser    jsextension=${CURDIR}/selector_engine.js
Resource         imports.resource

Test Teardown    Close Browser    ALL

Test Tags        no-iframe

*** Test Cases ***
An Engine Registered Before Connecting Over CDP Works In The Attached Context
    Register Tag Engine
    ${port} =    Free Port
    New Browser    chromium    headless=${HEADLESS}    args=["--remote-debugging-port=${port}"]
    Connect To Browser    http://localhost:${port}    chromium    use_cdp=True
    New Page    ${LOGIN_URL}
    Get Text    cdp-tag=h1    ==    Login Page

*** Keywords ***
Free Port
    ${port} =    Evaluate
    ...    (lambda s: (s.bind(('localhost', 0)), s.getsockname()[1], s.close())[1])(__import__('socket').socket())
    RETURN    ${port}
