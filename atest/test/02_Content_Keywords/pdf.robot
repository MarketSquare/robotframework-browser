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
    Should Be Equal    ${pdf3}    ${OUTPUT_DIR}${/}foor/bar/welcome3.pdf

Save As PDF With All Options
    ${pdf4} =    Save Page As Pdf    welcome4.pdf    displayHeaderFooter=True

*** Keywords ***
Open Headless Chrome
    [Documentation]    Generating a pdf is currently only supported in Chromium headless.
    New Browser    Chromium    headless=True
    New Page    ${WEBCOMPONENT_PAGE}
