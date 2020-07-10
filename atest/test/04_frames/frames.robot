*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser    ${FRAMES URL}    browser=${BROWSER}    headless=${HEADLESS}
Suite Teardown    Close Browser

*** Test Cases ***
Pierce iFrame implicit CSS, xpath and text
    Click    iframe[name="left"] >>> "foo"
    Get Attribute    \#left >>> a[href="foo.html"]    target    ==    right
    Get Text    //iframe[@id="right"] >>> p    ==    You're looking at foo.

Pierce iFrame nested selectors
    Click    body >> [src="left.html"] >>> body >> //input[@name="searchbutton"]
    Get Text    xpath=//body >> css=#right >>> xpath=/html >> css=body > p    ==    You're looking at search results.

