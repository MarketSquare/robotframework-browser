*** Settings ***
Documentation     Tests frames
Test Setup        Open Browser    localhost:7272/frames/frameset.html
Test Teardown     Close Browser
Resource          keywords.resource

*** Variables ***
${IFRAMES}        localhost:7272/frames/iframes.html

*** Test Cases ***
Page Should Have Content In Frame
    Pass Execution    Functionality Not Implemented yet
    Page Should Have    css=#right    "You're looking at right."
    Page Should Have    css=#left    "Links"

Page Should Have iframe content
    Pass Execution    Functionality Not Implemented yet
    Go To    ${IFRAMES}
    Frame Should contain    right    "You're looking at right."
    Frame Should Contain    left    Links

Current Frame Should (Not) Contain
    Pass Execution    Functionality Not Implemented yet
    Select Frame    left
    Current Frame Should Contain    This is LEFT side.
    Current Frame Should Not Contain    RIGHT
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    This is RIGHT side.
    Current Frame Should Not Contain    LEFT

Page Should Contain Text Within Frames
    Pass Execution    Functionality Not Implemented yet
    Page Should contain    "You're looking at right."
    Page Should Contain    Links

Page Should Contain Text Within Frames should also work with iframes
    Pass Execution    Functionality Not Implemented yet
    Go To    ${IFRAMES}
    Page Should contain    "You're looking at right."
    Page Should Contain    Links

Select And Unselect Frame
    Pass Execution    Functionality Not Implemented yet
    [Documentation]    LOG 2 Selecting frame 'left'.
    Select Frame    left
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    "You're looking at foo."

Select And Unselect Frame should also work with iframes
    Pass Execution    Functionality Not Implemented yet
    Go To    ${IFRAMES}
    Select Frame    left
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    "You're looking at foo."

Select Frame with non-unique name attribute
    Pass Execution    Functionality Not Implemented yet
    Go To    "localhost:7272/frames/poorlynamedframe.html"
    Run Keyword And Expect Error    "No Element matching"*    Select Frame    left
    Select Frame    xpath=//frame[@name='left']|//iframe[@name='left']
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    You're looking at foo.
