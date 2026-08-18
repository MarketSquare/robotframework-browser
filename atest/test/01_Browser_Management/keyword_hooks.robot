*** Settings ***
Documentation       The keyword call banner must be decided per library keyword, not by comparing
...                 the library name against the literal string "Browser". Both imports below use
...                 exactly the same arguments, so Robot Framework reuses the very same library
...                 instance and only the reported library name differs. Every Browser keyword is
...                 called with an explicit prefix, because both names are visible in this suite.

Resource            ../variables.resource
Library             Browser
...                     timeout=${PLAYWRIGHT_TIMEOUT}
...                     enable_playwright_debug=${True}
...                     enable_presenter_mode=False
...                     selector_prefix=${SELECTOR_PREFIX}
...                     highlight_on_failure=True
Library             Browser
...                     timeout=${PLAYWRIGHT_TIMEOUT}
...                     enable_playwright_debug=${True}
...                     enable_presenter_mode=False
...                     selector_prefix=${SELECTOR_PREFIX}
...                 highlight_on_failure=True    AS    PW
Library             ${CURDIR}/../../library/banner.py

Suite Setup         Open Form Page
Test Setup          Prepare Banner Test
Test Teardown       Browser.Show Keyword Banner    None

*** Variables ***
${SECRET_VALUE} =       xyzzy-do-not-disclose

*** Test Cases ***
Alias Import Reuses The Same Library Instance
    [Documentation]    Guards the assumption this suite is built on. If the two argument lists ever
    ...    drift apart, Robot Framework creates a second Browser instance and every test below
    ...    would silently exercise two separate libraries.
    ${plain} =    Get Library Instance    Browser
    ${aliased} =    Get Library Instance    PW
    Should Be Equal    ${plain}    ${aliased}

Keyword Call Banner Is Shown For An Aliased Import
    PW.Get Title
    banner.Get Banner Style Text    ==    Get Title

Keyword Call Banner Shows Arguments For An Aliased Import
    PW.Set Viewport Size    width=1200    height=800
    banner.Get Banner Style Text    ==    Set Viewport Size \ \ \ width=1200 \ \ \ height=800

Keyword Call Banner Is Muted For Take Screenshot Of An Aliased Import
    PW.Get Title
    banner.Get Banner Style Text    ==    Get Title
    PW.Take Screenshot    ${OUTPUTDIR}/alias_screenshot.png
    banner.Get Banner Style Text    ==    none

Keyword Call Banner Masks A Secret Argument
    [Documentation]    Fill Secret rejects a plainly resolved variable, but the banner is painted
    ...    before the keyword body runs. Without masking, the secret is burned into the page, into
    ...    the video recording and into the trace before the keyword ever fails.
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    Browser.Fill Secret    css=input#username    ${SECRET_VALUE}
    banner.Get Banner Style Text    ==    Fill Secret \ \ \ css=input#username \ \ \ ***

Keyword Call Banner Masks A Secret Argument Of An Aliased Import
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    PW.Fill Secret    css=input#username    ${SECRET_VALUE}
    banner.Get Banner Style Text    ==    Fill Secret \ \ \ css=input#username \ \ \ ***

Keyword Call Banner Leaves A Dictionary Expansion Of A Secret Keyword Unresolved
    [Documentation]    Masking maps source arguments onto parameters by position and by name.
    ...    A collection expansion is a single source cell that carries both, so it cannot be
    ...    mapped. Resolving it would print the whole dictionary, secret included, into the page.
    VAR    &{arguments} =    selector=css=input#username    secret=${SECRET_VALUE}
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    Browser.Fill Secret    &{arguments}
    banner.Get Banner Style Text    ==    Fill Secret \ \ \ \&{arguments}

Keyword Call Banner Leaves A List Expansion Of A Secret Keyword Unresolved
    VAR    @{arguments} =    css=input#username    ${SECRET_VALUE}
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    Browser.Fill Secret    @{arguments}
    banner.Get Banner Style Text    ==    Fill Secret \ \ \ \@{arguments}

Keyword Call Banner Still Resolves Variables Of Keywords Without A Secret
    VAR    ${selector} =    css=input#username
    Browser.Get Element Count    ${selector}
    banner.Get Banner Style Text    ==    Get Element Count \ \ \ css=input#username

*** Keywords ***
Open Form Page
    Browser.New Browser    ${BROWSER}    headless=${HEADLESS}
    Browser.New Page    ${LOGIN_URL}

Prepare Banner Test
    Browser.Go To    ${LOGIN_URL}
    Browser.Show Keyword Banner    True
