*** Settings ***
Resource          imports.resource
Test Setup        Open Browser To Form Page

*** Test Cases ***
Cookies From Closed Context
    Close All Browsers
    Run Keyword And Expect Error
    ...    Tried to get all cookie's, but no context is active.
    ...    Get Cookies

Get Cookies Should Return Empty List When No Cookies Are Available
    ${empty_list}    Create List
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    ${empty_list}

Add Cookie Without Url, Path and Domain
    Run Keyword And Expect Error
    ...    ValueError: Cookie should have a url or a domain/path pair.
    ...    Add Cookie    Foo    Bar

Add Cookie Should Fail If Context Is Not Open
    ${url} =    Get Url
    Close All Browsers
    Run Keyword And Expect Error
    ...    Tried to add cookie, but no context is active.
    ...    Add Cookie    Foo    Bar    url=${url}

Add Cookie With Url
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    Should Be Equal    ${cookies}[0][path]    /

Add Cookie With Domain And Path
    ${url} =    Get Url
    ${parsed_url} =    common.Parse Url    ${url}
    Add Cookie    Foo    Bar    domain=${parsed_url.netloc}    path=${parsed_url.path}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    Should Be Equal    ${cookies}[0][path]    /prefilled_email_form.html

Add Cookie With URL And Domain Should Fail
    ${url} =    Get Url
    ${parsed_url} =    common.Parse Url    ${url}
    Run Keyword And Expect Error
    ...    Cookie should have either url or domain
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
    ...    expiry=${date_string}
    ...    http_only=True
    ...    secure=True
    ...    same_site=Lax
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    Should Be Equal    ${cookies}[0][path]    /
    Should Be Equal    ${cookies}[0][sameSite]    Lax
    ${epoch} =    Convert Date    ${date_string}    result_format=epoch    exclude_millis=True
    ${epoch} =    Convert To Integer    ${epoch}
    ${epoch} =    Convert To String    ${epoch}
    ${expires} =    Convert To String    ${cookies}[0][expires]
    Should Contain    ${expires}    ${epoch}[:-1]    # To avoid rounding error
    Should Be Equal    ${cookies}[0][httpOnly]    ${True}
    Should Be Equal    ${cookies}[0][secure]    ${False}

Add Cookie With Expiry As Epoch String
    ${url} =    Get Url
    ${date_string} =    Get Current Date    increment=1 day    result_format=epoch
    ${date_string} =    Convert To Integer    ${date_string}
    ${date_string} =    Convert To String    ${date_string}
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expiry=${date_string}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    ${epoch} =    Convert To Integer    ${date_string}
    Should Be Equal    ${cookies}[0][expires]    ${epoch}

Add Cookie With Expiry As Epoch Int
    ${url} =    Get Url
    ${date_string} =    Get Current Date    increment=1 day    result_format=epoch
    ${date_string} =    Convert To Integer    ${date_string}
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expiry=${date_string}
    ${cookies} =    Get Cookies
    Check Cookie    ${cookies}    1    Foo    Bar
    ${epoch} =    Convert To Integer    ${date_string}
    Should Be Equal    ${cookies}[0][expires]    ${epoch}

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

*** Keywords ***
Check Cookie
    [Arguments]    ${cookies}    ${len}    ${name}    ${value}
    ${cookies_len} =    Get Length    ${cookies}
    ${len} =    Convert To Integer    ${len}
    Should Be Equal    ${cookies_len}    ${len}
    Should Be Equal    ${cookies}[${len - 1}][name]    ${name}
    Should Be Equal    ${cookies}[${len - 1}][value]    ${value}
    Should Be Equal    ${cookies}[${len - 1}][domain]    localhost
