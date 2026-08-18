*** Settings ***
Documentation       Tests for Show Keyword Banner

Resource            imports.resource
Library             ${CURDIR}/../../library/banner.py

Suite Setup         Ensure Open Page
Test Setup          Go To    ${FORM_URL}
Test Teardown       Show Keyword Banner    None

*** Test Cases ***
Show Keyword Banner
    [Documentation]    This test case should show the keyword banner
    ${original_settings} =    Show Keyword Banner    True
    Should Be True    $original_settings["show"] == None and $original_settings["style"] == ''
    Get Selected Options    [name="possible_channels"]    text    validate    value == ["Email", "Telephone"]
    Get Keyword Call Banner Text
    ...    ==
    ...    Get Selected Options \ \ \ [name="possible_channels"] \ \ \ text \ \ \ validate \ \ \ value == ["Email", "Telephone"]
    Show Keyword Banner    &{original_settings}
    Get Title
    Get Keyword Call Banner Text    ==    ${EMPTY}

Keyword Call Banner Content
    [Documentation]    This test case should show the keyword banner
    ${original_settings} =    Show Keyword Banner    True
    Should Be True    $original_settings["show"] == None and $original_settings["style"] == ''
    Set Viewport Size    width=1200    height=800
    Get Keyword Call Banner Text    ==    Set Viewport Size \ \ \ width=1200 \ \ \ height=800
    Get Title
    Get Keyword Call Banner Text    ==    Get Title
    Get Viewport Size    ALL    validate    value == {"width": 1200, "height": 800}
    Get Keyword Call Banner Text
    ...    ==
    ...    Get Viewport Size \ \ \ ALL \ \ \ validate \ \ \ value == {"width": 1200, "height": 800}
    Get Attribute
    ...    xpath=//input[@name="submit"]
    ...    attribute=name
    ...    assertion_operator=should be
    ...    assertion_expected=submit
    Get Keyword Call Banner Text
    ...    ==
    ...    Get Attribute \ \ \ xpath=//input[@name="submit"] \ \ \ attribute=name \ \ \ assertion_operator=should be \ \ \ assertion_expected=submit

Get Page Source And Take Screenshot Muting
    ${original_settings} =    Show Keyword Banner    True
    Get Title
    Get Keyword Call Banner Text    ==    Get Title
    Take Screenshot    ${OUTPUTDIR}/screenshot.png
    Get Keyword Call Banner Text    ==    ${EMPTY}
    Get Viewport Size
    Get Keyword Call Banner Text    ==    Get Viewport Size
    Get Page Source    not contains    I'm warning you! If you say "Jehovah" once more...
    Get Keyword Call Banner Text    ==    ${EMPTY}
    Get Wrapped Page Source    not contains    Jehovah
    Get Title    not contains    Jehovah
    Get Keyword Call Banner Text    contains    Jehovah

Change Banner CSS
    Set Viewport Size    width=1200    height=800
    ${original_settings} =    Show Keyword Banner    True
    Get Title
    ${style} =    Get Style    body    pseudo_element=::before
    Should Be Equal    ${style}[left]    5px
    Should Be Equal    ${style}[bottom]    5px
    Show Keyword Banner
    ...    show=True
    ...    style=top: 5px; bottom: auto; background-color: red; color: white; font-size: 20px; font-family: monospace; padding: 10px; border: 1px solid black; border-radius: 5px;
    Get Title
    ${style} =    Get Style    body    pseudo_element=::before
    Should Be Equal    ${style}[top]    5px
    Should Be Equal    ${style}[left]    5px
    Should Be Equal    ${style}[background-color]    rgb(255, 0, 0)
    Should Be Equal    ${style}[color]    rgb(255, 255, 255)
    Should Be Equal    ${style}[font-size]    20px
    Should Be Equal    ${style}[font-family]    monospace
    Should Be Equal    ${style}[padding-left]    10px
    Should Be Equal    ${style}[padding-right]    10px
    Should Be Equal    ${style}[padding-top]    10px
    Should Be Equal    ${style}[padding-bottom]    10px
    Should Be Equal    ${style}[border-bottom-right-radius]    5px
    Should Be Equal    ${style}[border-bottom-left-radius]    5px
    Should Be Equal    ${style}[border-top-right-radius]    5px
    Should Be Equal    ${style}[border-top-left-radius]    5px
