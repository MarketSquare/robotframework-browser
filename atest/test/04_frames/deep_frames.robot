*** Settings ***
Resource          imports.resource

Suite Setup       New Browser    ${BROWSER}    headless=${HEADLESS}
Suite Teardown    Close Browser
Test Setup        Ensure Location    ${DEEP_FRAMES_URL}

*** Test Cases ***
First Level
    Get Text    h1    ==    A HTML

Second Level
    Get Text    id=b >>> id=bb    ==    B HTML

Third Level
    ${style} =    Get Style    id=b >>> id=c >>> id=cc    width
    Should Be Equal    ${style}    auto
    Get Text    id=b >>> id=c >>> id=cc    ==    This is c

Third Level Executing JS
    Evaluate JavaScript    id=b >>> id=c >>> id=cc    (element) => element.textContent = "foo"
    Get Text    id=b >>> id=c >>> id=cc    ==    foo

Third Level From Second
    New Page    ${DEEP_FRAMES_2ND_URL}
    Get Text    id=c >>> id=cc    ==    This is c

Pierce IFrame Implicit CSS, Xpath And Text
    [Setup]    Ensure Location    ${FRAMES_URL}
    Click    iframe[name="left"] >>> "foo"
    Get Property    \#left >>> a[href="foo.html"]    target    ==    right
    Get Text    //iframe[@id="right"] >>> p    ==    You're looking at foo.

Pierce IFrame Nested Selectors
    [Setup]    Ensure Location    ${FRAMES_URL}
    Click    body >> [src="left.html"] >>> body >> //input[@name="searchbutton"]
    Get Text    xpath=//body >> css=#right >>> xpath=/html >> css=body > p    ==    You're looking at search results.

A Leading Frame Piercing Separator Searches Every Frame
    Get Text    >>> id=cc    ==    This is c
    Get Text    >>> id=bb    ==    B HTML
    Get Text    >>> h1    ==    A HTML

A Leading Frame Piercing Separator Continues Into Frames
    Get Text    >>> id=c >>> id=cc    ==    This is c
    Click    >>> id=c >>> id=cc

A Leading Frame Piercing Separator Also Searches The Main Frame
    Get Element Count    >>> id=b    ==    1

A Leading Frame Piercing Separator Fails When Several Frames Match
    Run Keyword And Expect Error    *    Get Text    >>> body

A Leading Frame Piercing Separator Works Without Strict Mode
    ${old} =    Set Strict Mode    False
    TRY
        Get Text    >>> id=cc    ==    This is c
    FINALLY
        Set Strict Mode    ${old}
    END

A Selector Prefix Still Comes First
    ${old} =    Set Selector Prefix    id=b
    TRY
        Get Text    >>> id=bb    ==    B HTML
    FINALLY
        Set Selector Prefix    ${old}
    END
