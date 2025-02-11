*** Settings ***
Library         OperatingSystem
Library         CryptoLibrary    password=cryptoPassword123    key_path=${CURDIR}/keys/
Resource        imports.resource

Suite Setup     New Page
Test Setup      Ensure Open Page    ${LOGIN_URL}

*** Test Cases ***
Type Text With Clearing
    Type Text    input#username_field    Wrong Text
    Type Text    input#username_field    user
    Type Text    input#username_field    name    clear=No
    Get Text    css=input#username_field    ==    username

Type Text With Nonmatching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *    Error: locator.fill: Timeout 50ms exceeded.*waiting For Locator('notamatch')*
    ...    Type Text    notamatch    text
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Clear Text
    Fill Text    input#username_field    Wrong Text
    Get Text    css=input#username_field    ==    Wrong Text
    Clear Text    input#username_field
    Get Text    css=input#username_field    ==    ${EMPTY}
    Type Text    input#username_field    username    clear=No
    Get Text    css=input#username_field    ==    username

Clear Text With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements:*
    ...    Clear Text    //input
    Set Strict Mode    False
    Clear Text    //input
    [Teardown]    Set Strict Mode    True

Clear Text With Nonmatching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *Error: locator.fill: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Clear Text    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Fill With Css Selector
    Fill Text    css=input#username_field    username
    Get Text    css=input#username_field    ==    username

Fill Text With Force
    Fill Text    css=input#username_field    username    force=True
    Get Text    css=input#username_field    ==    username

Fill Text With Nonmatching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *Error: locator.fill: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Fill Text    notamatch    text
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Fill Text With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements:*
    ...    Fill Text    //input    something
    Set Strict Mode    False
    Fill Text    //input    something
    [Teardown]    Set Strict Mode    True

Fill Secret Direct Value
    TRY
        Type Secret    css=input#username_field    Direct Value 1    10 ms    True
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Get Text    css=input#username_field    ==    ${EMPTY}
    TRY
        Fill Secret    css=input#password_field    Direct Value 2
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Get Text    css=input#password_field    ==    ${EMPTY}

Fill Secret With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements:*
    ...    Fill Secret    //input    $LOGIN_URL
    Set Strict Mode    False
    Fill Secret    //input    $LOGIN_URL
    [Teardown]    Set Strict Mode    True

Type Secret With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements:*
    ...    Type Secret    //input    $LOGIN_URL
    Set Strict Mode    False
    Type Secret    //input    $LOGIN_URL
    [Teardown]    Set Strict Mode    True

Fill Secret Placeholder-env-var
    [Documentation]    ...
    ...    LOG 3:2    NONE
    ...    LOG 5:2    NONE
    [Tags]    no-iframe
    Set Environment Variable    PH_ENV_VAR    password11
    Type Secret    css=input#username_field    %PH_ENV_VAR    ${0.02}    ${TRUE}
    Get Text    css=input#username_field    ==    password11
    Fill Secret    css=input#password_field    %PH_ENV_VAR
    Get Text    css=input#password_field    ==    password11

Fill Secret Robot-env-var
    Set Environment Variable    WAITTIMER    10 ms
    Set Environment Variable    ENV_VAR    password12
    TRY
        Type Secret    css=input#username_field    %{ENV_VAR}    %{WAITTIMER}    clear=True
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Type Secret    css=input#username_field    %ENV_VAR    %{WAITTIMER}    clear=True
    Get Text    css=input#username_field    ==    password12
    TRY
        Fill Secret    css=input#password_field    %{ENV_VAR}
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Fill Secret    css=input#password_field    %ENV_VAR
    Get Text    css=input#password_field    ==    password12

Fill Secret Robot-env-var Mixed
    Set Environment Variable    ENV_VAR    password13
    TRY
        Type Secret    css=input#username_field    %{ENV_VAR}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    TRY
        Fill Secret    css=input#password_field    %{ENV_VAR}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END

Fill Secret Robot-env-var Mixed2
    Set Environment Variable    ENV_VAR    password13
    TRY
        Type Secret    css=input#username_field    XXX%{ENV_VAR}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Get Text    css=input#username_field    ==    ${EMPTY}
    TRY
        Fill Secret    css=input#password_field    XXX%{ENV_VAR}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Get Text    css=input#password_field    ==    ${EMPTY}

Fill Secret Placeholder-robot-var
    [Documentation]
    ...    LOG 3:2    NONE
    ...    LOG 5:2    NONE
    [Tags]    no-iframe
    ${var} =    Set Variable    password123
    Type Secret    css=input#username_field    $var
    Get Text    css=input#username_field    ==    password123
    Fill Secret    css=input#password_field    $var
    Get Text    css=input#password_field    ==    password123

Fill Secret Robot Var
    ${var} =    Set Variable    password321
    TRY
        Type Secret    css=input#username_field    ${var}
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    TRY
        Fill Secret    css=input#password_field    ${var}
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END

Fill Secret Robot Var Mixed
    ${var} =    Set Variable    password321
    TRY
        Type Secret    css=input#username_field    ${var}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    TRY
        Fill Secret    css=input#password_field    ${var}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END

Fill Secret Robot Var Mixed2
    ${var} =    Set Variable    password321
    TRY
        Type Secret    css=input#username_field    xxx${var}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    TRY
        Fill Secret    css=input#password_field    xxx${var}XXX
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END

Fill Secret Placeholder In Robot Var
    Set Global Variable    ${global}    password666
    ${var} =    Set Variable    $global
    TRY
        Type Secret    css=input#username_field    ${var}
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    TRY
        Fill Secret    css=input#password_field    ${var}
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END

Fill Secret Env Placeholder In Robot Var
    Set Environment Variable    pwd_TWO    ENV_password123
    ${var} =    Set Variable    %pwd_TWO
    Type Secret    css=input#username_field    ${var}
    Get Text    css=input#username_field    ==    ENV_password123
    Fill Secret    css=input#password_field    ${var}
    Get Text    css=input#password_field    ==    ENV_password123

Fill Secret With Direct $Value Not Resolvable
    TRY
        Type Secret    css=input#username_field    $Direct Value
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Get Text    css=input#username_field    ==    ${EMPTY}
    TRY
        Fill Secret    css=input#password_field    $Direct Value
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed. Use special variable syntax ($var instead of \${var}) to prevent variable values from being spoiled.
        Log    correct error
    END
    Get Text    css=input#password_field    ==    ${EMPTY}

Fill Secret Fails When Variable Is Not Set
    Run Keyword And Expect Error    Variable '\${NONE_EXISTING_ENV_VARIABLE}' not found.    Type Secret
    ...    css=input#username_field    ${NONE_EXISTING_ENV_VARIABLE}
    Run Keyword And Expect Error    Variable '\${NONE_EXISTING_ENV_VARIABLE}' not found.    Fill Secret
    ...    css=input#password_field    ${NONE_EXISTING_ENV_VARIABLE}

Fill Secret Fails When Env Variable Is Not Set
    Run Keyword And Expect Error    Environment variable '\%{NONE_EXISTING_ENV_VARIABLE}' not found.    Type Secret
    ...    css=input#username_field    %{NONE_EXISTING_ENV_VARIABLE}
    Run Keyword And Expect Error    Environment variable '\%{NONE_EXISTING_ENV_VARIABLE}' not found.    Fill Secret
    ...    css=input#password_field    %{NONE_EXISTING_ENV_VARIABLE}

Type Secret Env
    [Tags]    no-iframe    log 2:2    none
    Set Environment Variable    TYPE_SECRET    password22
    Type Secret    css=input#password_field    %TYPE_SECRET
    Get Text    css=input#password_field    ==    password22

Type Secret Local
    [Documentation]
    ...    LOG 3:2    NONE
    [Tags]    no-iframe
    ${var} =    Set Variable    password321
    Type Secret    css=input#password_field    $var
    Get Text    css=input#password_field    ==    password321

Fill Secret With Nonmatching Selector
    [Tags]    no-iframe
    Set Environment Variable    MY_RFBROWSER_SECRET    secret
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *Error: locator.fill: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Fill Secret    notamatch    %MY_RFBROWSER_SECRET
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Type Text With Delay
    Type Text    input#username_field    username    delay=10 ms
    Get Text    css=input#username_field    ==    username

Type Text With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation:*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements:*
    ...    Type Text    //input    username
    Set Strict Mode    False
    Type Text    //input    username
    [Teardown]    Set Strict Mode    True

Type And Fill Text With Text Selector
    Type Text    input#username_field    Text field
    Type Text    text=User Name:    txt=some text
    Get Text    input#username_field    ==    some text
    Fill Text    text=User Name:    txt=another text
    Get Text    input#username_field    ==    another text

Type And Fill Secret With Text Selector
    ${var} =    Set Variable    pwfield
    Type Secret    input#password_field    $var
    ${var} =    Set Variable    some text
    Type Secret    text=Password:    $var
    Get Text    input#password_field    ==    some text
    ${var} =    Set Variable    another text
    Fill Secret    text=Password:    $var
    Get Text    input#password_field    ==    another text

Secret With Empty Value
    Type Secret    css=input#password_field    $EMPTY
    Fill Secret    css=input#password_field    $EMPTY

Fill Text With Clearing
    Fill Text    input#username_field    Wrong Text
    Fill Text    input#username_field    username
    Get Text    css=input#username_field    ==    username

Get Text Default Error
    Set Retry Assertions For    100ms
    Type Text    input#username_field    Wrong Text
    Run Keyword And Expect Error
    ...    Text 'Wrong Text' (str) should be 'username' (str)
    ...    Get Text    css=input#username_field    ==    username
    [Teardown]    Set Retry Assertions For    1s

Get Text Custom Error
    Set Retry Assertions For    100ms
    Type Text    input#username_field    Wrong Text
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Text    css=input#username_field    ==    username    Tidii
    [Teardown]    Set Retry Assertions For    1s

Text Area Access
    Get Text    id=textarea51    ==    Some initial text
    Type Text    id=textarea51    Area 51
    Get Text    id=textarea51    ==    Area 51
    Type Text    id=textarea51    Ufo detected
    Get Text    id=textarea51    ==    Ufo detected

Type Secret With CryptoLibrary
    Type Secret
    ...    input#username_field
    ...    crypt:/kfGGEGSwlcPsxBzVjMsnBWsYPXfFDF8BPj3APzN6AKS2W0mjOuh4coJljnb+MqZOmB5BG1oGpON7QC7nQ==
    ...    delay=10 ms
    Get Text    css=input#username_field    ==    FunkyPassword

Fill Secret With CryptoLibrary
    Fill Secret
    ...    input#username_field
    ...    crypt:1hYdLAcm9cANzOCussOyLS2wX4Nem6DAEGDacu8p9DCHHwZ0i+9MUkkeBHnf6UrrQLMcTQMbHoYoTH8f0do9fyk5itHBBjr91n4=
    Get Text    css=input#username_field    ==    AnotherFunkySecretPassword
