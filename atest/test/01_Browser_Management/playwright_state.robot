*** Settings ***
Resource            imports.resource
Library             Process

Test Teardown       Close Browser    ALL

*** Test Cases ***
Open Firefox
    Open Browser And Assert Login Page    firefox

Open Chrome
    Open Browser And Assert Login Page    chromium

New Browser Does Not Open A Page
    New Browser    headless=${HEADLESS}    reuse_existing=False
    Run Keyword And Expect Error
    ...    Error: No page open.    Go To    ${LOGIN_URL}

New Browser Does Not Create A Context
    New Browser    headless=${HEADLESS}    reuse_existing=False
    # Use Switch context to test that no context exists here
    ${no_context_id} =    Switch Context    CURRENT
    Should Be Equal    ${no_context_id}    NO CONTEXT OPEN

New Context Does Not Open A Page
    New Context
    ${no_page_id} =    Switch Page    CURRENT
    Should Be Equal    ${no_page_id}    NO PAGE OPEN

Open Browser Opens Everything
    [Tags]    slow
    ${old_timeout} =    Set Browser Timeout    30 seconds
    Open Browser    url=${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    Set Browser Timeout    ${old_timeout}

Open Browser With Invalid Browser Fails On RF Side
    Run Keyword And Expect Error
    ...    *Argument 'browser' got value 'netscape' that cannot be converted to SupportedBrowsers*    Open Browser
    ...    url=${FORM_URL}    browser=netscape
    [Teardown]    No Operation

New Browser With Invalid Browser Fails On RF Side
    Run Keyword And Expect Error
    ...    *Argument 'browser' got value 'netscape' that cannot be converted to SupportedBrowsers*    New Browser
    ...    netscape
    [Teardown]    No Operation

Create Chain Works
    [Tags]    slow
    New Browser    headless=${HEADLESS}    reuse_existing=False
    New Context
    ${first} =    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    Switch Page    ${first}
    Get Title    matches    (?i)login

Close Browser Switches Active Page
    [Tags]    slow
    New Browser    headless=${HEADLESS}    reuse_existing=False
    New Page Login
    New Browser    headless=${HEADLESS}    reuse_existing=False
    New Page Form
    Close Browser
    Get Title    matches    (?i)login

Close Context Switches Active Page
    [Tags]    slow
    New Context
    New Page Login
    New Context
    New Page Form
    Close Context
    Get Title    matches    (?i)login

Close Page Switches Active Page
    [Tags]    slow
    New Page Login
    New Page Form
    Close Page
    Get Title    matches    (?i)login

Close Page With runBeforeUnload
    New Page Login
    New Page Form
    Close Page    runBeforeUnload=True
    Get Title    matches    (?i)login

Set Default Run Before Unload
    ${old_value} =    Set Default Run Before Unload    True
    Should Not Be True    ${old_value}
    ${old_value} =    Set Default Run Before Unload    False
    Should Be True    ${old_value}

Browser, Context And Page UUIDs
    [Tags]    slow
    ${browser} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${context} =    New Context
    ${page} =    New Page
    Should Start With    ${browser}    browser=
    Should Start With    ${context}    context=
    Should Start With    ${page}[page_id]    page=
    Should Be Empty    ${page}[video_path]
    [Teardown]    Close Browser

Switch Context
    [Tags]    slow
    ${first_context} =    New Context
    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    ${second_context} =    New Context
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    Switch Context    ${first_context}
    Get Title    matches    (?i)login

New Page Can New Context And Browser
    [Tags]    slow
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page

Switch Page After Popup
    [Tags]    slow    no-iframe
    Open Browser And Assert Login Page    chromium
    Click    button#pops_up
    ${previous} =    Switch Page    NEW
    Wait For Elements State    "Popped Up!"
    Switch Page    ${previous}
    Wait For Elements State    button#pops_up

Switch New Page Fails When No New Pages
    [Tags]    slow
    New Page    ${LOGIN_URL}
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    ${timeout} =    Set Browser Timeout    0.1s
    Run Keyword And Expect Error
    ...    Error: Tried to activate a new page but no new pages were detected in context.    Switch Page    NEW
    Get Title    ==    prefilled_email_form.html
    [Teardown]    Set Browser Timeout    ${timeout}

Set Viewport Size
    New Page
    ${size} =    Get Viewport Size
    ${desired_first} =    Evaluate    {"height": 720, "width": 1280}
    Should Be Equal    ${size}    ${desired_first}
    Set Viewport Size    height=600    width=800
    ${desired_second} =    Evaluate    {"height": 600, "width": 800}
    ${second_size} =    Get Viewport Size
    Should Be Equal    ${desired_second}    ${second_size}

Page Index Is Stable When Other Pages Closed
    [Tags]    slow
    ${first} =    New Page
    ${second} =    New Page
    ${third} =    New Page
    Close Page
    Close Page
    ${last} =    Switch Page    ${first}
    Should Be Equal    ${first}[page_id]    ${last}

Context Index Is Stable When Other Contexts Closed
    [Tags]    slow
    ${first} =    New Context
    ${second} =    New Context
    ${third} =    New Context
    Close Context
    Close Context
    ${last} =    Switch Context    ${first}
    Should Be Equal    ${first}    ${last}

Page Indices Are Unique
    [Tags]    slow
    ${first} =    New Page
    Close Page
    ${second} =    New Page
    Should Not Be Equal    ${first}    ${second}

Close Page Gets Errors And Console Log
    [Tags]    slow
    ${page} =    New Page    ${ERROR_URL}
    Click    "Crash click"
    ${response} =    Close Page
    Log    ${response}
    Should Be Equal    ${response}[0][console][0][text]    Hello from warning
    Should Match    ${response}[0][errors][0]    *Error: a is not defined*
    Should Be Equal    ${response}[0][id]    ${page}[page_id]

Context Indices Are Unique
    [Tags]    slow
    ${first} =    New Context
    Close Context
    ${second} =    New Context
    Should Not Be Equal    ${first}    ${second}

Browser Indices Are Unique
    [Tags]    slow
    ${first} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    Close Browser
    ${second} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    Should Not Be Equal    ${first}    ${second}

Close All Contexts
    [Tags]    slow
    New Context
    New Context
    New Context
    Close Context    ALL
    ${current} =    Switch Context    CURRENT
    Should Be Equal    ${current}    NO CONTEXT OPEN

Close All Pages
    [Tags]    slow
    New Page
    New Page
    New Page
    ${closes} =    Close Page    ALL
    Length Should Be    ${closes}    3
    ${current} =    Switch Page    CURRENT
    Should Be Equal    ${current}    NO PAGE OPEN

Closing Page/Contex/Browser Multiple Times Should Not Cause Errors
    [Tags]    slow
    New Context
    New Page
    Close Page
    Close Context
    Close Context
    Close Browser
    Close Browser

Closing Page/Contex/Browser Multiple Times With All Should Not Cause Errors
    [Tags]    slow
    New Context
    New Page
    Close Page    ALL
    Close Page    ALL
    Close Context    ALL    ALL
    Close Context    ALL    ALL
    Close Browser    ALL
    Close Browser    ALL

New Context With DefaultBrowserType Ff
    [Tags]    slow
    [Timeout]    80s    # Because FF is just slow sometimes
    ${old_timeout} =    Set Browser Timeout    80s
    New Context    defaultBrowserType=firefox
    Verify Browser Type    firefox
    Set Browser Timeout    ${old_timeout}

New Context With baseURL
    New Context    baseURL=${ROOT_URL}
    New Page    dist/#/
    Get Url    ==    ${LOGIN_URL}
    Go To    prefilled_email_form.html
    Get Url    ==    ${FORM_URL}
    Go To    http://127.0.0.1:${SERVER_PORT}/frames/iframes.html
    Get Url    ==    http://127.0.0.1:${SERVER_PORT}/frames/iframes.html

New Context With DefaultBrowserType Chromium
    [Tags]    slow
    New Context    defaultBrowserType=chromium
    Verify Browser Type    chromium

When Context Without Browser Is Created This Is Logged For User
    [Documentation]
    ...    LOG    1:5    INFO    No browser was open. New browser was automatically opened when this context is created.
    ...    LOG    1:7    NONE
    ...    LOG    2:6    NONE
    [Tags]    slow
    [Setup]    Close Browser    ALL
    New Context
    New Context

When Page Without Browser Is Created This Is Logged For User
    [Documentation]
    ...    LOG    1:3    INFO    No browser and context was open. New browser and context was automatically opened when page is created.
    ...    LOG    1:4    DEBUG    Video is not enabled.
    ...    LOG    1:5    NONE
    ...    LOG    2:3    DEBUG    Video is not enabled.
    ...    LOG    2:4    NONE
    [Tags]    slow
    [Setup]    Close Browser    ALL
    New Page
    New Page

When Page Without Context Is Created This Is Logged For User
    [Documentation]
    ...    LOG    2:3    INFO    No context was open. New context was automatically opened when this page is created.
    ...    LOG    2:4    DEBUG    Video is not enabled.
    ...    LOG    2:5    NONE
    ...    LOG    3:3    DEBUG    Video is not enabled.
    ...    LOG    3:4    NONE
    [Tags]    slow
    [Setup]    Close Browser    ALL
    New Browser    headless=${HEADLESS}    reuse_existing=False
    New Page
    New Page

Switch Page With ALL Browsers
    [Tags]    slow
    [Timeout]    60s
    ${browser1} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${context11} =    New Context
    ${page111} =    New Page
    ${page112} =    New Page
    ${context12} =    New Context
    ${page121} =    New Page
    ${page122} =    New Page
    ${browser2} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${context21} =    New Context
    ${page211} =    New Page
    ${page212} =    New Page
    ${context22} =    New Context
    ${page221} =    New Page
    ${page222} =    New Page

    ${cat} =    Get Browser Catalog
    Log    ${cat}
    ${cur_page} =    Get Page Ids    ACTIVE    ACTIVE    ACTIVE
    Assert Equal    ${cur_page}[0]    ${page222}[page_id]

    Switch Page    ${page111}    ALL    ALL
    ${cur_page} =    Get Page Ids    ACTIVE    ACTIVE    ACTIVE
    Assert Equal    ${cur_page}[0]    ${page111}[page_id]

    Switch Page    ${page212}[page_id]    ALL    ALL
    ${cur_page} =    Get Page Ids    ACTIVE    ACTIVE    ACTIVE
    Assert Equal    ${cur_page}[0]    ${page212}[page_id]

    Switch Page    ${page221}    ALL    CURRENT
    ${cur_page} =    Get Page Ids    ACTIVE    ACTIVE    ACTIVE
    Assert Equal    ${cur_page}[0]    ${page221}[page_id]

    Switch Page    ${page111}    CURRENT    ALL
    ${cur_page} =    Get Page Ids    ACTIVE    ACTIVE    ACTIVE
    Assert Equal    ${cur_page}[0]    ${page111}[page_id]

Switch Context With ALL Browsers
    ${browser1} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${context11} =    New Context
    ${page111} =    New Page
    ${page112} =    New Page
    ${context12} =    New Context
    ${page121} =    New Page
    ${page122} =    New Page
    ${browser2} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${context21} =    New Context
    ${page211} =    New Page
    ${page212} =    New Page
    ${context22} =    New Context
    ${page221} =    New Page
    ${page222} =    New Page

    ${cat} =    Get Browser Catalog
    Log    ${cat}
    ${cur_context} =    Get Context Ids    ACTIVE    ACTIVE
    Assert Equal    ${cur_context}[0]    ${context22}

    Switch Context    ${context12}    ALL
    ${cur_context} =    Get Context Ids    ACTIVE    ACTIVE
    Assert Equal    ${cur_context}[0]    ${context12}

    Switch Context    ${context11}    CURRENT
    ${cur_context} =    Get Context Ids    ACTIVE    ACTIVE
    Assert Equal    ${cur_context}[0]    ${context11}

Switch Page With ALL Browsers Failing
    ${browser1} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${context11} =    New Context
    ${page111} =    New Page
    ${page112} =    New Page
    ${context12} =    New Context
    ${page121} =    New Page
    ${page122} =    New Page
    ${browser2} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${context21} =    New Context
    ${page211} =    New Page
    ${page212} =    New Page
    ${context22} =    New Context
    ${page221} =    New Page
    ${page222} =    New Page

    ${cat} =    Get Browser Catalog
    Log    ${cat}
    ${cur_page} =    Get Page Ids    ACTIVE    ACTIVE    ACTIVE
    Assert Equal    ${cur_page}[0]    ${page222}[page_id]

    Run Keyword And Expect Error    EQUALS:ValueError: No page with requested id 'page=123' found.
    ...    Run Keyword And Continue On Failure
    ...    Switch Page    page=123    ALL    ALL

    Run Keyword And Expect Error
    ...    EQUALS:Error: No page for id ${page211}[page_id]. Open pages: { id: ${page221}[page_id], url: about:blank },{ id: ${page222}[page_id], url: about:blank }
    ...    Run Keyword And Continue On Failure
    ...    Switch Page
    ...    ${page211}
    ...    CURRENT
    ...    CURRENT

    Run Keyword And Expect Error    EQUALS:ValueError: Malformed page `id`: 1
    ...    Run Keyword And Continue On Failure
    ...    Switch Page    1    ALL    ALL

Launch Browser Server CLI
    ${wsEndpoint} =    Launch Browser Server    chromium    headless=${HEADLESS}    port=8270    wsPath=server1
    Should Be Equal    ${wsEndpoint}    ws://localhost:8270/server1
    ${browser} =    Connect To Browser    ws://localhost:8270/server1
    New Page    ${LOGIN_URL}
    Get Title    ==    Login Page
    [Teardown]    Close Browser Server    ${wsEndpoint}

Launch Browser Server CLI With Video
    [Documentation]
    ...    LOG 5:3    DEBUG    Video is not enabled.
    ${wsEndpoint} =    Launch Browser Server    chromium    headless=${HEADLESS}    port=8271    wsPath=server1
    Should Be Equal    ${wsEndpoint}    ws://localhost:8271/server1
    ${browser} =    Connect To Browser    ws://localhost:8271/server1
    New Context
    ...    tracing=path/is/not/here/trace_999.zip
    ...    recordVideo={'dir':'videos', 'size':{'width':1080, 'height':720}}
    New Page    ${LOGIN_URL}
    Get Title    ==    Login Page
    [Teardown]    Close Browser Server    ${wsEndpoint}

Launch Browser Server Generated wsEndpoint
    ${wsEndpoint} =    Launch Browser Server    chromium    headless=${HEADLESS}
    ${browser} =    Connect To Browser    ${wsEndpoint}
    New Page    ${LOGIN_URL}
    Get Title    ==    Login Page
    [Teardown]    Close Browser Server    ${wsEndpoint}

Launch Browser Server Via CLI
    ${python} =    Get Python Binary Path
    ${process1} =    Start Process
    ...    ${python}
    ...    -m
    ...    Browser.entry
    ...    launch-browser-server
    ...    chromium
    ...    headless\=${HEADLESS}
    ...    port\=8277
    ...    wsPath\=server2
    ${process2} =    Start Process
    ...    ${python}
    ...    -m
    ...    Browser.entry
    ...    launch-browser-server
    ...    chromium
    ...    headless\=${HEADLESS}
    ...    port\=8273
    ...    wsPath\=server3
    Sleep    10s
    Connect To Browser    wsEndpoint=ws://localhost:8277/server2    browser=chromium
    New Page    ${LOGIN_URL}
    Get Title    ==    Login Page
    Close Browser    ALL
    Connect To Browser    wsEndpoint=ws://localhost:8277/server2    browser=chromium
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    Connect To Browser    wsEndpoint=ws://localhost:8273/server3    browser=chromium
    New Context    viewport={"width": 100, "height": 100}
    New Page    ${LOGIN_URL}
    Get Viewport Size    width    ==    100
    Get Viewport Size    height    ==    100
    [Teardown]    Terminate All Processes

*** Keywords ***
Open Browser And Assert Login Page
    [Arguments]    ${local_browser}
    Open Browser To Login Page
    Get Text    h1    ==    Login Page

New Page Form
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html

New Page Login
    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login

Assert Equal
    [Arguments]    ${one}    ${two}
    Run Keyword And Continue On Failure    Should Be Equal    ${one}    ${two}
