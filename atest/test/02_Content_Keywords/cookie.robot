*** Settings ***
Resource            imports.resource

Suite Setup         New Browser    ${BROWSER}    headless=${HEADLESS}
Test Setup          Open New Context To Form Page
Test Teardown       Close Context    ALL

Force Tags          no-iframe

*** Test Cases ***
Get Cookies Should Return Empty List When No Cookies Are Available
    ${empty_list} =    Create List
    ${cookies} =    Get Cookies    dictionary
    Should Be Equal    ${cookies}    ${empty_list}
    ${cookies} =    Get Cookies    dict
    Should Be Equal    ${cookies}    ${empty_list}

Get Cookies With String Type
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    ${cookies} =    Get Cookies    str
    Should Be Equal    Foo=Bar    ${cookies}
    ${cookies} =    Get Cookies    string
    Should Be Equal    Foo=Bar    ${cookies}

Add Cookie Without Url, Path And Domain
    Run Keyword And Expect Error
    ...    Error: browserContext.addCookies: Cookie should have a url or a domain/path pair
    ...    Add Cookie    Foo    Bar

Add Cookie With Url
    [Tags]    no-windows-support
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    Should Be Equal    ${cookies}[0][path]    /

Add Cookie With Domain And Path
    [Tags]    no-windows-support
    ${url} =    Get Url
    ${parsed_url} =    Common.Parse Url    ${url}
    Add Cookie    Foo    Bar    domain=${parsed_url.netloc}    path=${parsed_url.path}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    Should Be Equal    ${cookies}[0][path]    /prefilled_email_form.html

Add Cookie With URL And Domain Should Fail
    ${url} =    Get Url
    ${parsed_url} =    Common.Parse Url    ${url}
    Run Keyword And Expect Error
    ...    Error: browserContext.addCookies: Cookie should have either url or domain
    ...    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    domain=${parsed_url.netloc}
    ...    path=${parsed_url.path}

Add Cookie With All Settings
    ${url} =    Get Url
    ${date_string} =    Get Current Date    increment=1 day
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expires=${date_string}
    ...    httpOnly=True
    ...    secure=True
    ...    sameSite=Lax
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    Should Be Equal    ${cookies}[0][path]    /
    Should Be Equal    ${cookies}[0][sameSite]    Lax
    ${expires} =    Convert To String    ${cookies}[0][expires]
    Should Match Regexp    ${expires}    \\d
    Should Be Equal    ${cookies}[0][httpOnly]    ${True}
    Should Be Equal    ${cookies}[0][secure]    ${False}

Add Cookie With All Settings As String
    ${url} =    Get Url
    ${date_string} =    Get Current Date    increment=1 day
    Add Cookie
    ...    Tidii
    ...    Kala
    ...    url=${url}
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expires=${date_string}
    ...    httpOnly=True
    ...    secure=True
    ...    sameSite=Lax
    ${cookies} =    Get Cookies    string
    Should Contain    ${cookies}    Tidii=Kala; Foo=Bar

Add Cookie With Expiry As Epoch String
    ${url} =    Get Url
    ${epoch} =    Get Current Date    increment=1 day    result_format=epoch
    ${date_time} =    Convert Date    ${epoch}
    ${epoch} =    Convert To Integer    ${epoch}
    ${epoch} =    Convert To String    ${epoch}
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expires=${epoch}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    ${epoch_as_str} =    Convert To String    ${cookies}[0][expires]
    Should Match Regexp    ${epoch_as_str}    \\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d\\:\\d\\d\\:\\d\\d
    ${expires} =    Set Variable    ${cookies}[0][expires]
    Should Be Equal    ${expires.year}    ${expires.year}

Add Cookie With Expiry As Epoch Int
    ${url} =    Get Url
    ${epoch} =    Get Current Date    increment=1 day    result_format=epoch
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expires=${epoch}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    ${epoch_as_str} =    Convert To String    ${cookies}[0][expires]
    Should Match Regexp    ${epoch_as_str}    \\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d\\:\\d\\d\\:\\d\\d
    ${expires} =    Set Variable    ${cookies}[0][expires]
    ${date_time} =    Convert Date    ${epoch}
    Should Be Equal    ${expires.year}    ${expires.year}

Add Cookie With Expiry As Epoch In Different Format
    ${url} =    Get Url
    Add Cookie
    ...    Foo22
    ...    Bar22
    ...    url=${url}
    ...    expires=3 155 760 000,195223
    ${cookie} =    Get Cookie    Foo22
    ${epoch_as_str} =    Convert To String    ${cookie}[expires]
    Should Match Regexp    ${epoch_as_str}    \\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d\\:\\d\\d\\:\\d\\d
    Add Cookie
    ...    Foo333
    ...    Bar333
    ...    url=${url}
    ...    expires=3 155 760 000
    ${cookie} =    Get Cookie    Foo333
    ${epoch_as_str} =    Convert To String    ${cookie}[expires]
    Should Match Regexp    ${epoch_as_str}    \\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d\\:\\d\\d\\:\\d\\d

Add Cookie With Expiry As Datetime Object
    ${url} =    Get Url
    ${datetime} =    Evaluate    datetime.datetime.now() + datetime.timedelta(hours=1)    # local time
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expires=${datetime}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    ${expires_str} =    Convert To String    ${cookies}[0][expires]
    Should Match Regexp    ${expires_str}    \\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d\\:\\d\\d\\:\\d\\d
    ${local_time_expires} =    Evaluate    $cookies[0]['expires'].astimezone()
    Should Be Equal    ${datetime.year}    ${local_time_expires.year}
    Should Be Equal    ${datetime.month}    ${local_time_expires.month}
    Should Be Equal    ${datetime.day}    ${local_time_expires.day}
    Should Be Equal    ${datetime.hour}    ${local_time_expires.hour}
    Should Be Equal    ${datetime.minute}    ${local_time_expires.minute}
    Should Be Equal    ${datetime.second}    ${local_time_expires.second}

Add Cookie With Expiry From Other Cookie
    ${url} =    Get Url
    ${date_string} =    Get Current Date    increment=1 day
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expires=${date_string}
    ${cookies} =    Get Cookies
    Add Cookie
    ...    Baz
    ...    Qux
    ...    url=${url}
    ...    expires=${cookies}[0][expires]
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}[0][expires]    ${cookies}[1][expires]

Delete All Cookies
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    Delete All Cookies
    ${cookies} =    Get Cookies
    Should Be Empty    ${cookies}

Delete All Cookies When Cookies Does Not Exist
    Delete All Cookies
    ${cookies} =    Get Cookies
    Should Be Empty    ${cookies}

Eat All Cookies
    Eat All Cookies

Get Cookie
    [Tags]    no-windows-support
    ${url} =    Get Url
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    httpOnly=True
    ...    secure=True
    ...    sameSite=Lax
    Add Cookie
    ...    Tidii
    ...    kala
    ...    url=${url}
    ...    httpOnly=True
    ...    secure=True
    ...    sameSite=Lax
    ${cookie} =    Get Cookie    Tidii
    Should Be Equal    ${cookie}[name]    Tidii
    Should Be Equal    ${cookie}[value]    kala
    Should Be Equal    ${cookie.name}    Tidii
    Should Be Equal    ${cookie.value}    kala

Get Cookie As String
    ${url} =    Get Url
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    httpOnly=True
    ...    secure=True
    ...    sameSite=Lax
    Add Cookie
    ...    Tidii
    ...    kala
    ...    url=${url}
    ...    httpOnly=True
    ...    secure=True
    ...    sameSite=Lax
    ${cookie} =    Get Cookie    Tidii    string
    Should Be Equal    ${cookie}    Tidii=kala

Get Cookie Should Fail If Cookie Is Not Found
    ${url} =    Get Url
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    httpOnly=True
    ...    secure=True
    ...    sameSite=Lax
    Run Keyword And Expect Error
    ...    ValueError: Cookie with name FOO is not found.
    ...    Get Cookie
    ...    FOO

Get Cookie Should Fail With Invalid Return_type
    Run Keyword And Expect Error
    ...    ValueError: Argument 'return_type' got value 'invalid_type' that cannot be converted to CookieType*
    ...    Get Cookie
    ...    FOO
    ...    invalid_type

Get Cookie And No Expiry
    New Browser    chromium    headless=True
    New Context
    New Page    about:blank
    Add Cookie    tidii    kala    http://address.com/to/site
    Get Cookie    tidii    return_type=dict

*** Keywords ***
Open New Context To Form Page
    New Context
    New Page    ${FORM_URL}

Check Cookie
    [Arguments]    ${cookies}    ${len}    ${name}    ${value}
    ${cookies_len} =    Get Length    ${cookies}
    ${len} =    Convert To Integer    ${len}
    Should Be Equal    ${cookies_len}    ${len}
    Should Be Equal    ${cookies}[${len - 1}][name]    ${name}
    Should Be Equal    ${cookies}[${len - 1}][value]    ${value}
    Should Be Equal    ${cookies}[${len - 1}][domain]    localhost
