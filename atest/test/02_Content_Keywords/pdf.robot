*** Settings ***
Resource        imports.resource

Suite Setup     Open Headless Chrome

*** Test Cases ***
Save As PDF With Default Options
    ${pdf1} =    Save Page As Pdf    ${OUTPUT_DIR}${/}welcome1.pdf
    ${pdf2} =    Save Page As Pdf    welcome2.pdf
    ${pdf3} =    Save Page As Pdf    foor/bar/welcome3.pdf
    Should Be Equal    ${pdf1}    ${OUTPUT_DIR}${/}welcome1.pdf
    Should Be Equal    ${pdf2}    ${OUTPUT_DIR}${/}welcome2.pdf
    ${expected_pdf3} =    Normalize Path    ${OUTPUT_DIR}${/}foor/bar/welcome3.pdf
    Should Be Equal    ${pdf3}    ${expected_pdf3}

Save As PDF With All Options
    ${marging} =    Create Dictionary    top=10px    right=20px    bottom=30px    left=40px
    # footerTemplate and headerTemplate are from https://github.com/microsoft/playwright/issues/14441
    ${pdf4} =    Save Page As Pdf
    ...    welcome4.pdf
    ...    displayHeaderFooter=True
    ...    footerTemplate=<span style="font-size: 20px;color:#000000;">FOOTER</span>
    ...    format=A4
    ...    headerTemplate=<span style="font-size: 20px;color:#000000;">HEADER</span>
    ...    height=10pix
    ...    landscape=True
    ...    margin=${marging}
    ...    outline=True
    ...    pageRanges=1-2
    ...    preferCSSPageSize=True
    ...    printBackground=True
    ...    scale=0.5
    ...    tagged=True
    ...    width=20px
    Should Be Equal    ${pdf4}    ${OUTPUT_DIR}${/}welcome4.pdf
    ${marging} =    Create Dictionary    top=10px    bottom=30px
    # footerTemplate and headerTemplate are from https://github.com/microsoft/playwright/issues/14441
    ${pdf5} =    Save Page As Pdf
    ...    welcome5.pdf
    ...    margin={"top": "10px", "bottom": "30px"}
    Should Be Equal    ${pdf5}    ${OUTPUT_DIR}${/}welcome5.pdf

Save PDF With Invalid Margin
    TRY
        Save Page As Pdf
        ...    welcome5.pdf
        ...    margin={"foo": "10px", "bottom": "other"}
    EXCEPT    *    type=glob    AS    ${err}
        Should Contain    ${err}    page.pdf: Failed to parse parameter value: other
    END

Save PDF With Emulate Media
    ${media} =    Emulate Media    dark    active    print    no-preference
    Log    ${media}
    ${expected_media} =    Create Dictionary
    ...    colorScheme=dark
    ...    forcedColors=active
    ...    media=print
    ...    reducedMotion=no-preference
    Dictionaries Should Be Equal    ${media}    ${expected_media}
    ${media} =    Emulate Media    None    not_set    print
    ${expected_media} =    Create Dictionary    media=print
    Dictionaries Should Be Equal    ${media}    ${expected_media}
    ${pdf6} =    Save Page As Pdf
    ...    welcome6.pdf
    Should Be Equal    ${pdf6}    ${OUTPUT_DIR}${/}welcome6.pdf
    ${media} =    Emulate Media    null    None    null    null
    ${expected_media} =    Create Dictionary
    ...    colorScheme=${None}
    ...    forcedColors=none
    ...    media=${None}
    ...    reducedMotion=${None}
    Dictionaries Should Be Equal    ${media}    ${expected_media}

Save PDF With Firefox Should Not Work
    [Documentation]    Generating a pdf is currently only supported in Chromium headless.
    New Browser    Firefox    headless=True
    New Page    ${WEBCOMPONENT_PAGE}
    TRY
        Save Page As Pdf    welcome7.pdf
    EXCEPT    Error: page.pdf*    type=GLOB
        No Operation
    FINALLY
        Close Browser    CURRENT
    END

*** Keywords ***
Open Headless Chrome
    [Documentation]    Generating a pdf is currently only supported in Chromium headless.
    New Browser    Chromium    headless=True
    New Page    ${WEBCOMPONENT_PAGE}
