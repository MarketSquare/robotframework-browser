*** Settings ***
Documentation    Both imports below use exactly the same arguments, so Robot Framework reuses
...              the very same library instance and only the reported library name differs.

Resource         ../variables.resource
Library          Browser    &{BROWSER_CONFIG}
Library          Browser    &{BROWSER_CONFIG}    AS    PW
Library          ${CURDIR}/../../library/banner.py

Suite Setup      Open Form Page
Test Setup       Prepare Banner Test
Test Teardown    Browser.Show Keyword Banner    None

*** Variables ***
${SECRET_VALUE} =      xyzzy-do-not-disclose
&{BROWSER_CONFIG} =    timeout=${PLAYWRIGHT_TIMEOUT}
...                    enable_playwright_debug=${True}
...                    enable_presenter_mode=False
...                    selector_prefix=${SELECTOR_PREFIX}
...                    highlight_on_failure=True

*** Test Cases ***
Alias Import Reuses The Same Library Instance
    ${plain} =    Get Library Instance    Browser
    ${aliased} =    Get Library Instance    PW
    Should Be Equal    ${plain}    ${aliased}

Keyword Call Banner Is Shown For An Aliased Import
    PW.Get Title
    Get Keyword Call Banner Text    ==    Get Title

Keyword Call Banner Shows Arguments For An Aliased Import
    PW.Set Viewport Size    width=1200    height=800
    Get Keyword Call Banner Text    ==    Set Viewport Size \ \ \ width=1200 \ \ \ height=800

Keyword Call Banner Is Muted For Take Screenshot Of An Aliased Import
    PW.Get Title
    Get Keyword Call Banner Text    ==    Get Title
    PW.Take Screenshot    ${OUTPUTDIR}/alias_screenshot.png
    Get Keyword Call Banner Text    ==    ${EMPTY}

Keyword Call Banner Masks A Secret Argument
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    Browser.Fill Secret    css=input#username    ${SECRET_VALUE}
    Get Keyword Call Banner Text    ==    Fill Secret \ \ \ css=input#username \ \ \ ***

Keyword Call Banner Masks A Secret Argument Of An Aliased Import
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    PW.Fill Secret    css=input#username    ${SECRET_VALUE}
    Get Keyword Call Banner Text    ==    Fill Secret \ \ \ css=input#username \ \ \ ***

Keyword Call Banner Leaves A Dictionary Expansion Of A Secret Keyword Unresolved
    VAR    &{arguments} =    selector=css=input#username    secret=${SECRET_VALUE}
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    Browser.Fill Secret    &{arguments}
    Get Keyword Call Banner Text    ==    Fill Secret \ \ \ \&{arguments}

Keyword Call Banner Leaves A List Expansion Of A Secret Keyword Unresolved
    VAR    @{arguments} =    css=input#username    ${SECRET_VALUE}
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*
    ...    Browser.Fill Secret    @{arguments}
    Get Keyword Call Banner Text    ==    Fill Secret \ \ \ \@{arguments}

Keyword Call Banner Masks Secret Typed Arguments Of Create Credential
    VAR    ${private_key} =    MIIEvQIBADANBgkq-private-key-do-not-disclose
    Run Keyword And Expect Error
    ...    ValueError: Direct assignment of values or variables as 'privateKey' is not allowed.*
    ...    Browser.Create Credential    rpId=example.com    privateKey=${private_key}
    Get Keyword Call Banner Text    ==    Create Credential \ \ \ rpId=example.com \ \ \ privateKey=***

Keyword Call Banner Still Resolves Variables Of Keywords Without A Secret
    VAR    ${selector} =    css=input#username
    Browser.Get Element Count    ${selector}
    Get Keyword Call Banner Text    ==    Get Element Count \ \ \ css=input#username

*** Keywords ***
Open Form Page
    Browser.New Browser    ${BROWSER}    headless=${HEADLESS}
    Browser.New Page    ${LOGIN_URL}

Prepare Banner Test
    Browser.Go To    ${LOGIN_URL}
    Browser.Show Keyword Banner    True
