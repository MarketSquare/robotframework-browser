*** Settings ***
Resource          imports.resource

*** Variables ***
${FRAMES URL}     ${ROOT URL}/frames/iframes.html

*** Test Cases ***
Assert content inside iframe
    [Setup]    Open Browser    ${FRAMES URL}
    Get Text    css=#left >>> .link
