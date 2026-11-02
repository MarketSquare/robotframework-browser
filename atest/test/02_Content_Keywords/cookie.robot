*** Settings ***
Resource         imports.resource

Suite Setup      New Browser    ${BROWSER}    headless=${HEADLESS}
Test Setup       Open New Context To Form Page
Test Teardown    Close Context    ALL

Test Tags        no-iframe

*** Test Cases ***
Get Cookies Should Return Empty List When No Cookies Are Available
    VAR    @{empty_list} =    @{EMPTY}
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
    [Tags]    no-windows-support    no-docker-pr
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    Should Be Equal    ${cookies}[0][path]    /

Add Cookie With Domain And Path
    [Tags]    no-windows-support    no-docker-pr
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
    [Tags]    no-docker-pr
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
    [Tags]    no-docker-pr
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
    VAR    ${expires} =    ${cookies}[0][expires]
    Should Be Equal    ${expires.year}    ${expires.year}

Add Cookie With Expiry As Epoch Int
    [Tags]    no-docker-pr
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
    VAR    ${expires} =    ${cookies}[0][expires]
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
    [Tags]    no-docker-pr
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

Delete All Cookies With Name Keeps Other Cookies
    Add Cookie    session    1    domain=a.example    path=/
    Add Cookie    consent    2    domain=a.example    path=/
    Delete All Cookies    name=session
    Cookie Names Should Be    consent

Delete All Cookies With Domain Keeps Other Cookies
    Add Cookie    first    1    domain=a.example    path=/
    Add Cookie    second    2    domain=b.example    path=/
    Delete All Cookies    domain=a.example
    Cookie Names Should Be    second

Delete All Cookies With Path Keeps Other Cookies
    Add Cookie    first    1    domain=a.example    path=/app
    Add Cookie    second    2    domain=a.example    path=/other
    Delete All Cookies    path=/app
    Cookie Names Should Be    second

Delete All Cookies Requires All Filters To Match
    Add Cookie    session    1    domain=a.example    path=/
    Add Cookie    session    2    domain=b.example    path=/
    Add Cookie    consent    3    domain=a.example    path=/
    Delete All Cookies    name=session    domain=a.example
    ${cookies} =    Get Cookies
    Length Should Be    ${cookies}    2
    ${remaining} =    Get Cookies    string    urls=https://a.example
    Should Be Equal    ${remaining}    consent=3

Delete All Cookies With Filter Matching Nothing Keeps Cookies
    Add Cookie    session    1    domain=a.example    path=/
    Delete All Cookies    name=missing
    Cookie Names Should Be    session

Get Cookies With Url Returns Only Cookies Of That Url
    Add Cookie    match    1    domain=a.example    path=/app
    Add Cookie    other_path    2    domain=a.example    path=/other
    Add Cookie    other_domain    3    domain=b.example    path=/
    ${cookies} =    Get Cookies    urls=https://a.example/app/page
    Length Should Be    ${cookies}    1
    Should Be Equal    ${cookies}[0][name]    match

Get Cookies With Url List Returns Cookies Of Every Url
    Add Cookie    first    1    domain=a.example    path=/
    Add Cookie    second    2    domain=b.example    path=/
    Add Cookie    third    3    domain=c.example    path=/
    VAR    @{urls} =    https://a.example    https://b.example
    ${cookies} =    Get Cookies    string    urls=${urls}
    Should Be Equal    first\=1; second\=2    ${cookies}

Get Cookies With Url Leaves Secure Cookies Out Of Http Urls
    Add Cookie    secured    1    domain=a.example    path=/    secure=True
    ${cookies} =    Get Cookies    urls=http://a.example
    Should Be Empty    ${cookies}
    ${cookies} =    Get Cookies    urls=https://a.example
    Length Should Be    ${cookies}    1

Get Cookies With Empty Urls Returns All Cookies
    Add Cookie    first    1    domain=a.example    path=/
    Cookie Names For Urls Should Be    ${EMPTY}    first
    VAR    @{no_urls} =    @{EMPTY}
    Cookie Names For Urls Should Be    ${no_urls}    first

Add Partitioned Cookie With Domain And Path
    Add Cookie
    ...    tracker
    ...    1
    ...    domain=third-party.example
    ...    path=/
    ...    secure=True
    ...    partitionKey=https://site.example
    ${cookie} =    Get Cookie    tracker
    Should Be Equal    ${cookie}[partitionKey]    https://site.example

Get Cookies With Invalid Url Fails
    Run Keyword And Expect Error
    ...    *Invalid URL*
    ...    Get Cookies    urls=not a url

Partitioned Cookie Round Trip
    Add Cookie    tracker    abc123    url=https://third-party.example    partitionKey=https://site.example
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}[0][partitionKey]    https://site.example
    ${cookie} =    Get Cookie    tracker
    Should Be Equal    ${cookie}[partitionKey]    https://site.example

Unpartitioned Cookie Has No Partition Key
    Add Cookie    plain    1    url=https://third-party.example
    ${cookie} =    Get Cookie    plain
    Dictionary Should Not Contain Key    ${cookie}    partitionKey

Delete All Cookies With Name Deletes Every Partition
    Add Cookie    tracker    1    url=https://third-party.example    partitionKey=https://site.example
    Add Cookie    tracker    2    url=https://third-party.example    partitionKey=https://other.example
    Add Cookie    plain    3    url=https://third-party.example
    Delete All Cookies    name=tracker
    Cookie Names Should Be    plain

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

Cookie Names For Urls Should Be
    [Arguments]    ${urls}    ${expected}
    ${cookies} =    Get Cookies    string    urls=${urls}
    Should Be Equal    ${cookies}    ${expected}\=1

Cookie Names Should Be
    [Arguments]    @{expected}
    ${cookies} =    Get Cookies
    VAR    @{names} =    @{{[cookie.name for cookie in $cookies]}}
    Lists Should Be Equal    ${names}    ${expected}    ignore_order=True

Check Cookie
    [Arguments]    ${cookies}    ${len}    ${name}    ${value}
    ${cookies_len} =    Get Length    ${cookies}
    ${len} =    Convert To Integer    ${len}
    Should Be Equal    ${cookies_len}    ${len}
    Should Be Equal    ${cookies}[${len - 1}][name]    ${name}
    Should Be Equal    ${cookies}[${len - 1}][value]    ${value}
    Should Be Equal    ${cookies}[${len - 1}][domain]    localhost
