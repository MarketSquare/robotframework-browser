*** Settings ***
Resource          imports.resource
Test Setup        Open Browser To Form Page

*** Test Cases ***
Cookies From Closed Context
    Close All Browsers
    Run Keyword And Expect Error
    ...    Tried to get all cookie's, but not context open.
    ...    Get Cookies

Get Cookies Should Return Empty List When No Cookies Are Available
    ${cookies} =    Get Cookies
    Log    ${cookies}

Add Cookie Without Url, Path and Domain
    Run Keyword And Expect Error
    ...    ValueError: Cookie should have a url or a domain/path pair.
    ...    Add Cookie    Foo    Bar

Add Cookie Should Fail If Context Is Not Open
    ${url} =    Get Url
    Close All Browsers
    Run Keyword And Expect Error
    ...    Tried to add cookie, but not context open.
    ...    Add Cookie    Foo    Bar    url=${url}

Add Cookie With Url
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
