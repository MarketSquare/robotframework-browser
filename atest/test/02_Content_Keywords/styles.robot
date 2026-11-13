*** Settings ***
Resource      imports.resource

Test Setup    New Page    ${LOGIN_URL}

Test Tags     no-iframe

*** Test Cases ***
Add Style
    Add Style Tag    \#goes_hidden{color:aqua}

Verify Style
    Add Style Tag    \#goes_hidden{color:aqua}
    Get Style    \#goes_hidden    color    ==    rgb(0, 255, 255)

Add Style Tag From Url
    Add Style Tag    url=${ROOT_URL}style_tag.css
    Get Style    \#goes_hidden    color    ==    rgb(0, 255, 255)

Add Style Tag From Path
    Add Style Tag    path=${CURDIR}/style_tag.css
    Get Style    \#goes_hidden    color    ==    rgb(0, 255, 255)

Add Style Tag Fails When Url Does Not Load
    Run Keyword And Expect Error    *addStyleTag: Event
    ...    Add Style Tag    url=${ROOT_URL}no_such_style.css

Add Style Tag Into Frame
    [Setup]    New Page    ${FRAMES_URL}
    Add Style Tag    body {background-color: aqua;}    frame_selector=id=left >>> body
    Get Style    id=left >>> body    background-color    ==    rgb(0, 255, 255)
    Get Style    id=right >>> body    background-color    !=    rgb(0, 255, 255)
    Get Style    body    background-color    !=    rgb(0, 255, 255)

Add Style Tag Fails With Empty Url
    Run Keyword And Expect Error    *Provide an object with a `url`, `path` or `content` property
    ...    Add Style Tag    url=${EMPTY}
