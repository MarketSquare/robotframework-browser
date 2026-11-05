*** Settings ***
Resource      imports.resource

Test Setup    New Page    ${LOGIN_URL}

*** Test Cases ***
Add Style
    [Tags]    no-iframe
    Add Style Tag    \#username_field:focus {background-color: aqua;}
    Focus    \#username_field
    Get Style    \#username_field    background-color    ==    rgb(0, 255, 255)

Focus With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Focus    //input
    Set Strict Mode    False    scope=Test
    Focus    //input

Blur Removes Focus From Element
    Focus    \#username_field
    Get Element States    \#username_field    contains    focused
    Blur    \#username_field
    Get Element States    \#username_field    contains    defocused

Blur Fires Blur Event
    [Setup]    New Page    ${EVENTS_URL}
    Focus    \#event_test_input
    Blur    \#event_test_input
    Get Text    \#event_log_text    *=    "type":"blur"

Blur On Element Without Focus Does Nothing
    [Setup]    New Page    ${EVENTS_URL}
    Blur    \#event_test_input
    Get Text    \#event_log_text    not contains    "type":"blur"
    Get Element States    \#event_test_input    contains    defocused

Blur On Element Without Focus Keeps Focus On Other Element
    [Setup]    New Page    ${EVENTS_URL}
    Focus    \#event_test_button
    Blur    \#event_test_input
    Get Element States    \#event_test_button    contains    focused

Blur Element Which Has Focus
    Focus    \#username_field
    Blur    css=:focus
    Get Element States    \#username_field    contains    defocused

Blur With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Blur    //input
    Set Strict Mode    False    scope=Test
    Focus    //input
    Blur    //input
    Get Element States    //input >> nth=0    contains    defocused
