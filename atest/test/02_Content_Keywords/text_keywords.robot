*** Settings ***
Resource          imports.resource
Library           OperatingSystem
Test Setup        Go To    ${LOGIN_URL}

*** Test Cases ***
Type Text with Clearing
    Type Text    input#username_field    Wrong Text
    Type Text    input#username_field    user
    Type Text    input#username_field    name    clear=No
    Get Text    css=input#username_field    ==    username

Type Text With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Type Text    notamatch    text
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Clear Text
    Fill Text    input#username_field    Wrong Text
    Get Text    css=input#username_field    ==    Wrong Text
    Clear Text    input#username_field
    Get Text    css=input#username_field    ==    ${EMPTY}
    Type Text    input#username_field    username    clear=No
    Get Text    css=input#username_field    ==    username

Clear Text With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Clear Text    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Fill with css selector
    Fill Text    css=input#username_field    username
    Get Text    css=input#username_field    ==    username

Fill Text With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Fill Text    notamatch    text
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Fill Secret Direct Value
    Type Secret    css=input#username_field    Direct Value    200 ms    True
    Get Text    css=input#username_field    ==    Direct Value
    Fill Secret    css=input#password_field    Direct Value
    Get Text    css=input#password_field    ==    Direct Value

Fill Secret placeholder-env-var
    Set Environment Variable    PH_ENV_VAR    password11
    Type Secret    css=input#username_field    %PH_ENV_VAR    ${0.2}    ${TRUE}
    Get Text    css=input#username_field    ==    password11
    Fill Secret    css=input#password_field    %PH_ENV_VAR
    Get Text    css=input#password_field    ==    password11

Fill Secret robot-env-var
    Set Environment Variable    WAITTIMER    100 ms
    Set Environment Variable    ENV_VAR    password12
    Type Secret    css=input#username_field    %{ENV_VAR}    %{WAITTIMER}    clear=True
    Get Text    css=input#username_field    ==    password12
    Fill Secret    css=input#password_field    %{ENV_VAR}
    Get Text    css=input#password_field    ==    password12

Fill Secret robot-env-var mixed
    Set Environment Variable    ENV_VAR    password13
    Type Secret    css=input#username_field    %{ENV_VAR}XXX
    Get Text    css=input#username_field    ==    password13XXX
    Fill Secret    css=input#password_field    %{ENV_VAR}XXX
    Get Text    css=input#password_field    ==    password13XXX

Fill Secret robot-env-var mixed2
    Set Environment Variable    ENV_VAR    password13
    Type Secret    css=input#username_field    XXX%{ENV_VAR}XXX
    Get Text    css=input#username_field    ==    XXXpassword13XXX
    Fill Secret    css=input#password_field    XXX%{ENV_VAR}XXX
    Get Text    css=input#password_field    ==    XXXpassword13XXX

Fill Secret placeholder-robot-var
    ${var}=    Set Variable    password123
    Type Secret    css=input#username_field    $var
    Get Text    css=input#username_field    ==    password123
    Fill Secret    css=input#password_field    $var
    Get Text    css=input#password_field    ==    password123

Fill Secret robot var
    ${var}=    Set Variable    password321
    Type Secret    css=input#username_field    ${var}
    Get Text    css=input#username_field    ==    password321
    Fill Secret    css=input#password_field    ${var}
    Get Text    css=input#password_field    ==    password321

Fill Secret robot var mixed
    ${var}=    Set Variable    password321
    Type Secret    css=input#username_field    ${var}XXX
    Get Text    css=input#username_field    ==    password321XXX
    Fill Secret    css=input#password_field    ${var}XXX
    Get Text    css=input#password_field    ==    password321XXX

Fill Secret robot var mixed2
    ${var}=    Set Variable    password321
    Type Secret    css=input#username_field    xxx${var}XXX
    Get Text    css=input#username_field    ==    xxxpassword321XXX
    Fill Secret    css=input#password_field    xxx${var}XXX
    Get Text    css=input#password_field    ==    xxxpassword321XXX

Fill Secret placeholder in robot var
    Set Global Variable    ${global}    password666
    ${var}=    Set Variable    $global
    Type Secret    css=input#username_field    ${var}
    Get Text    css=input#username_field    ==    password666
    Fill Secret    css=input#password_field    ${var}
    Get Text    css=input#password_field    ==    password666

Fill Secret env placeholder in robot var
    Set Environment Variable    pwd_TWO    ENV_password123
    ${var}=    Set Variable    %pwd_TWO
    Type Secret    css=input#username_field    ${var}
    Get Text    css=input#username_field    ==    ENV_password123
    Fill Secret    css=input#password_field    ${var}
    Get Text    css=input#password_field    ==    ENV_password123

Fill Secret with direct $value not resolvable
    Type Secret    css=input#username_field    $Direct Value
    Get Text    css=input#username_field    ==    $Direct Value
    Fill Secret    css=input#password_field    $Direct Value
    Get Text    css=input#password_field    ==    $Direct Value

Fill Secret fails when variable is not set
    Run Keyword And Expect Error    Variable '\${NONE_EXISTING_ENV_VARIABLE}' not found.    Type Secret    css=input#username_field    ${NONE_EXISTING_ENV_VARIABLE}
    Run Keyword And Expect Error    Variable '\${NONE_EXISTING_ENV_VARIABLE}' not found.    Fill Secret    css=input#password_field    ${NONE_EXISTING_ENV_VARIABLE}

Fill Secret fails when env variable is not set
    Run Keyword And Expect Error    Environment variable '\%{NONE_EXISTING_ENV_VARIABLE}' not found.    Type Secret    css=input#username_field    %{NONE_EXISTING_ENV_VARIABLE}
    Run Keyword And Expect Error    Environment variable '\%{NONE_EXISTING_ENV_VARIABLE}' not found.    Fill Secret    css=input#password_field    %{NONE_EXISTING_ENV_VARIABLE}

Type Secret env
    Set Environment Variable    TYPE_SECRET    password22
    Type Secret    css=input#password_field    %TYPE_SECRET
    Get Text    css=input#password_field    ==    password22

Type Secret local
    ${var}=    Set Variable    password321
    Type Secret    css=input#password_field    $var
    Get Text    css=input#password_field    ==    password321

Fill Secret With Nonmatching Selector
    Set Environment Variable    MY_RFBROWSER_SECRET    secret
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Fill Secret    notamatch    %MY_RFBROWSER_SECRET
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Type Text with Delay
    Type Text    input#username_field    username    delay=10 ms
    Get Text    css=input#username_field    ==    username

Fill Text with Clearing
    Fill Text    input#username_field    Wrong Text
    Fill Text    input#username_field    username
    Get Text    css=input#username_field    ==    username

Get Text Default Error
    Type Text    input#username_field    Wrong Text
    Run Keyword And Expect Error
    ...    Text 'Wrong Text' (str) should be 'username' (str)
    ...    Get Text    css=input#username_field    ==    username

Get Text Custom Error
    Type Text    input#username_field    Wrong Text
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Text    css=input#username_field    ==    username    Tidii

Text Area access
    Get Text  id=textarea51  ==  Some initial text
    Type Text   id=textarea51   Area 51
    Get Text  id=textarea51  ==  Area 51
    Type Text   id=textarea51   Ufo detected
    Get Text  id=textarea51  ==  Ufo detected
