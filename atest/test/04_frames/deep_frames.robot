*** Settings ***
Resource            imports.resource

Suite Setup         Open Browser To Deep Frame Page
Suite Teardown      Close Browser

*** Test Cases ***
First level
    Get Text    h1    ==    A HTML

Second level
    Get Text    id=b >>> id=bb    ==    B HTML

Third level
    ${style}=    Get Style    id=b >>> id=c >>> id=cc    width
    Get Text    id=b >>> id=c >>> id=cc    ==    This is c

Third level from second
    New Page    ${DEEP_FRAMES_2ND_URL}
    Get Text    id=c >>> id=cc    ==    This is c
