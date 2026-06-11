*** Settings ***
Resource            imports.resource
Library             ../../library/presenter_mode.py

Suite Setup         Setup Get Text
Suite Teardown      Set Retry Assertions For    ${assert_timeout}
Test Setup          Ensure Location    ${LOGIN_URL}

*** Variables ***
${USERNAMELABEL} =      label[for="username_field"]
${INPUTUSERNAME} =      id=username_field

*** Test Cases ***
Get Text
    ${h1} =    Get Text    h1
    Should Be Equal    ${h1}    Login Page

Get Text Disabled
    [Setup]    Go To    ${ELEMENT_STATE_URL}
    presenter_mode.Set Presenter Mode    {"color": "red", "duration": "1s", "style": "solid"}
    ${text} =    Get Text    //input[@name="readonly_with_equals_only"]
    [Teardown]    presenter_mode.Set Presenter Mode    False

Get Text And Assert ==
    Get Text    ${USERNAMELABEL}    ==    User Name:

Get Text And Assert !=
    Get Text    ${USERNAMELABEL}    !=

Get Text No Text Type And Input Field
    Type Text    ${INPUTUSERNAME}    MyUserName
    Get Text    ${INPUTUSERNAME}    ==    MyUserName

Get Text Text Type As InputValue And Input Field
    Type Text    ${INPUTUSERNAME}    MyUserName
    Get Text    ${INPUTUSERNAME}    ==    MyUserName    text_type=inputValue

Get Text No Text Type And Select Element
    Select Options By    id=pet-select    value    dog
    Get Text    id=pet-select    ==    dog

Get Text Text Type As InputValue And Select Element
    Select Options By    id=pet-select    value    dog
    Get Text    id=pet-select    ==    dog    text_type=inputValue

Get Text Assert Validate
    Get Text    h1    validate    value.startswith('Login')

Get Text With No Matching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *TimeoutError: locator.evaluate: Timeout 50ms exceeded.*
    ...    Get Text    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Get Text With Text Type As InnerHTML
    ${text} =    Get Text    h1    ==    Login Page    text_type=innerHTML
    Should Be Equal    ${text}    Login Page
    ${text} =    Get Text    [name="login_form"]    text_type=innerHTML
    Should Contain    ${text}    <label for="username_field">User Name:</label>
    Should Contain    ${text}    <label for="password_field">Password:</label>

Get Text With Text Type As InnerText
    ${text} =    Get Text    h1    ==    Login Page    text_type=innerText
    Should Be Equal    ${text}    Login Page
    ${text} =    Get Text    ${USERNAMELABEL}    text_type=innerText
    Should Be Equal    ${text}    User Name:

Get Text With Text Type As All InnerTexts
    ${texts} =    Get Text    //option    text_type=allInnerTexts
    VAR    @{expected} =    --Please choose an option--    Dog    Cat    Hamster    Parrot    Spider    Goldfish
    Lists Should Be Equal    ${texts}    ${expected}

Get Text With Text Type As All InnerTexts On Single Element With Multiple Text
    ${texts} =    Get Text    [name="login_form"]    text_type=allInnerTexts
    Should Contain    ${texts[0]}    User Name:
    Should Contain    ${texts[0]}    Password:
    Length Should Be    ${texts}    1

Get Text With Text Type As All TextContents With Multiple Text
    ${texts} =    Get Text    //option    text_type=allTextContents
    VAR    @{expected} =    --Please choose an option--    Dog    Cat    Hamster    Parrot    Spider    Goldfish
    Lists Should Be Equal    ${texts}    ${expected}

Text Area Access And No Text Type
    Get Text    id=textarea51    ==    Some initial text
    Type Text    id=textarea51    Area 51
    Get Text    id=textarea51    ==    Area 51
    Type Text    id=textarea51    Ufo detected
    Get Text    id=textarea51    ==    Ufo detected    text_type=inputValue

Get Text With RegEx Match
    ${text} =    Get Text    h1    matches    Login Page
    Should Be Equal    ${text}    Login Page
    ${text} =    Get Text    h1    matches    \\w+ (\\w+)
    Length Should Be    ${text}    1
    Should Be Equal    ${text[0]}    Page
    ${text} =    Get Text    h1    matches    (\\w+) (\\w+)
    Length Should Be    ${text}    2
    Should Be Equal    ${text[0]}    Login
    Should Be Equal    ${text[1]}    Page
    ${text} =    Get Text    h1    matches    (?P<name1>\\w+) (?P<name2>\\w+)
    Length Should Be    ${text}    2
    Should Be Equal    ${text['name1']}    Login
    Should Be Equal    ${text['name2']}    Page
    ${text} =    Get Text    h1    matches    (\\w+) (?P<name2>\\w+)
    Length Should Be    ${text}    2
    Should Be Equal    ${text[0]}    Login
    Should Be Equal    ${text[1]}    Page

Get Text With Select Element
    Select Options By    id=pet-select    value    dog
    ${text} =    Get Text    id=pet-select
    Should Be Equal    ${text}    dog
    ${text} =    Get Text    id=pet-select    text_type=innerText
    FOR    ${item}    IN    Please choose an option    Dog    Cat    Hamster    Parrot    Spider    Goldfish
        Should Match    ${text}    *${item}*
    END

Get Text With RegEx Match And text_type
    Run Keyword And Expect Error
    ...    TypeError:*expected string or bytes-like object*
    ...    Get Text    //option    matches    Some initial text    text_type=allTextContents

*** Keywords ***
Setup Get Text
    Close Page    ALL
    Ensure Open Page    ${LOGIN_URL}
    ${assert_timeout} =    Set Retry Assertions For    2 sec
    VAR    ${assert_timeout} =    ${assert_timeout}    scope=SUITE
