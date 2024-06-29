*** Settings ***
Resource        imports.resource

Suite Setup     Open Headless Chrome

*** Test Cases ***
Save As PDF
    ${pdf1} =    Save Page As Pdf    ${OUTPUT_DIR}${/}welcome1.pdf
    ${pdf2} =    Save Page As Pdf    welcome2.pdf
    ${pdf3} =    Save Page As Pdf    foor/bar/welcome3.pdf
    Should Be Equal    ${pdf1}    ${OUTPUT_DIR}${/}welcome1.pdf
    ${pdf4} =    Save Page As Pdf    ${OUTPUT_DIR}${/}welcome4.pdf
    Should Be Equal    ${pdf4}    ${OUTPUT_DIR}${/}welcome4.pdf

*** Keywords ***
Open Headless Chrome
    [Documentation]    Generating a pdf is currently only supported in Chromium headless.
    New Browser    Chromium    headless=True
    New Page    ${WEBCOMPONENT_PAGE}
