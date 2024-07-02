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
    # footerTemplate is from https://github.com/microsoft/playwright/issues/14441
    ${pdf4} =    Save Page As Pdf    welcome4.pdf    displayHeaderFooter=True    footerTemplate=<span style="font-size: 20px;color:#000000;">FOOTER</span>
    Should Be Equal    ${pdf4}    ${OUTPUT_DIR}${/}welcome4.pdf

*** Keywords ***
Open Headless Chrome
    [Documentation]    Generating a pdf is currently only supported in Chromium headless.
    New Browser    Chromium    headless=True
    New Page    ${WEBCOMPONENT_PAGE}
