*** Settings ***
Resource        imports.resource

Suite Setup     Open Headless Chrome

*** Test Cases ***
Save As PDF
    ${pdf} =    Save Page As Pdf    ${OUTPUT_DIR}${/}welcome.pdf
    ${pdf} =    Save Page As Pdf    welcome.pdf
    ${pdf} =    Save Page As Pdf    foor/bar/welcome.pdf
    Should Be Equal    ${pdf}    ${OUTPUT_DIR}${/}welcome.pdf
    ${pdf} =    Save Page As Pdf    ${OUTPUT_DIR}${/}welcome.pdf
    Should Be Equal    ${pdf}    ${OUTPUT_DIR}${/}welcome.pdf

*** Keywords ***
Open Headless Chrome
    [Documentation]    Generating a pdf is currently only supported in Chromium headless.
    New Browser    Chromium    headless=True
    New Page    ${WEBCOMPONENT_PAGE}
