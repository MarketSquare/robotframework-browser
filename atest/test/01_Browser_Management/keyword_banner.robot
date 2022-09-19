*** Settings ***
Documentation       Tests for Show Keyword Banner

Resource            imports.resource
Library             ${CURDIR}/keyword_banner.py

Suite Setup         Ensure Open Page
Test Setup          Go To    ${FORM_URL}
Test Teardown       Show Keyword Banner    None

*** Test Cases ***
Show Keyword Banner
    [Documentation]    This test case should show the keyword banner
    ${original_settings} =    Show Keyword Banner    True
    Should Be True    $original_settings["show"] == None and $original_settings["style"] == ''
    Get Selected Options    [name="possible_channels"]    text    validate    value == ["Email", "Telephone"]
    ${style} =    keyword_banner.Get Computed Banner Style
    Should Be Equal
    ...    ${style}[content]
    ...    "Get Selected Options \ \ \ [name=\\"possible_channels\\"] \ \ \ text \ \ \ validate \ \ \ value == [\\"Email\\", \\"Telephone\\"]"
    Show Keyword Banner    &{original_settings}
    Get Title
    ${style} =    keyword_banner.Get Computed Banner Style
    Should Be Equal    ${style}[content]    none

Keyword Call Banner Content
    [Documentation]    This test case should show the keyword banner
    ${original_settings} =    Show Keyword Banner    True
    Should Be True    $original_settings["show"] == None and $original_settings["style"] == ''
    Set Viewport Size    width=1200    height=800
    keyword_banner.Get Banner Content    ==    Set Viewport Size \ \ \ width=1200 \ \ \ height=800
    Get Title
    keyword_banner.Get Banner Content    ==    Get Title
    Get Viewport Size    ALL    validate    value == {'width': 1200, 'height': 800}
    keyword_banner.Get Banner Content
    ...    ==
    ...    Get Viewport Size \ \ \ ALL \ \ \ validate \ \ \ value == {'width': 1200, 'height': 800}
    Get Attribute
    ...    xpath=//input[@name="submit"]
    ...    attribute=name
    ...    assertion_operator=should be
    ...    assertion_expected=submit
    keyword_banner.Get Banner Content
    ...    ==
    ...    Get Attribute \ \ \ xpath=//input[@name="submit"] \ \ \ attribute=name \ \ \ assertion_operator=should be \ \ \ assertion_expected=submit

Get Page Source And Take Screenshot Muting
    ${original_settings} =    Show Keyword Banner    True
    Get Title
    keyword_banner.Get Banner Content    ==    Get Title
    Take Screenshot    ${OUTPUTDIR}/screenshot.png
    keyword_banner.Get Banner Content    ==    none
    Get Viewport Size
    keyword_banner.Get Banner Content    ==    Get Viewport Size
    Get Page Source    not contains    I'm warning you! If you say "Jehovah" once more...
    keyword_banner.Get Banner Content    ==    none
    keyword_banner.Get Real Page Source    not contains    Jehovah
    Get Title    not contains    Jehovah
    keyword_banner.Get Real Page Source    contains    Jehovah

Change Banner CSS
    Set Viewport Size    width=1200    height=800
    ${original_settings} =    Show Keyword Banner    True
    Get Title
    ${style} =    keyword_banner.Get Computed Banner Style
    Should Be Equal    ${style}[left]    5px
    Should Be Equal    ${style}[bottom]    5px
    Show Keyword Banner
    ...    show=True
    ...    style=top: 5px; bottom: auto; background-color: red; color: white; font-size: 20px; font-family: monospace; padding: 10px; border: 1px solid black; border-radius: 5px;
    Get Title
    ${style} =    keyword_banner.Get Computed Banner Style
    Should Be Equal    ${style}[top]    5px
    Should Be Equal    ${style}[left]    5px
    Should Be Equal    ${style}[backgroundColor]    rgb(255, 0, 0)
    Should Be Equal    ${style}[color]    rgb(255, 255, 255)
    Should Be Equal    ${style}[fontSize]    20px
    Should Be Equal    ${style}[fontFamily]    monospace
    Should Be Equal    ${style}[paddingLeft]    10px
    Should Be Equal    ${style}[paddingRight]    10px
    Should Be Equal    ${style}[paddingTop]    10px
    Should Be Equal    ${style}[paddingBottom]    10px
    Should Be Equal    ${style}[borderRadius]    5px
