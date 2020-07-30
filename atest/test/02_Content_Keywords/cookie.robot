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
    ${date_string} =    Get Current Date     increment=1 day
    Add Cookie
    ...    Foo
    ...    Bar
    ...    url=${url}
    ...    expiry=${date_string}

*** Keywords ***
Check Cookie
    [Arguments]    ${cookies}    ${len}    ${name}    ${value}
    ${cookies_len} =    Get Length    ${cookies}
    ${len} =    Convert To Integer    ${len}
    Should Be Equal    ${cookies_len}    ${len}
    Should Be Equal    ${cookies}[${len - 1}][name]    ${name}
    Should Be Equal    ${cookies}[${len - 1}][value]    ${value}
    Should Be Equal    ${cookies}[${len - 1}][domain]    localhost
