*** Settings ***
Resource            imports.resource

Suite Setup         Ensure Open Browser
Suite Teardown      Close Browser
Test Setup          Ensure Location    ${DEEP_FRAMES_URL}

*** Test Cases ***
First level
    Get Text    h1    ==    A HTML

Second level
    Get Text    id=b >>> id=bb    ==    B HTML

Third level
    ${style} =    Get Style    id=b >>> id=c >>> id=cc    width
    Should Be Equal    ${style}    auto
    Get Text    id=b >>> id=c >>> id=cc    ==    This is c

Third level executing JS
    Execute Javascript    (element) => element.textContent = "foo"    id=b >>> id=c >>> id=cc
    Get Text    id=b >>> id=c >>> id=cc    ==    foo

Third level from second
    New Page    ${DEEP_FRAMES_2ND_URL}
    Get Text    id=c >>> id=cc    ==    This is c

Pierce iFrame implicit CSS, xpath and text
    [Setup]    Ensure Location    ${FRAMES_URL}
    Click    iframe[name="left"] >>> "foo"
    Get Property    \#left >>> a[href="foo.html"]    target    ==    right
    Get Text    //iframe[@id="right"] >>> p    ==    You're looking at foo.

Pierce iFrame nested selectors
    [Setup]    Ensure Location    ${FRAMES_URL}
    Click    body >> [src="left.html"] >>> body >> //input[@name="searchbutton"]
    Get Text    xpath=//body >> css=#right >>> xpath=/html >> css=body > p    ==    You're looking at search results.
