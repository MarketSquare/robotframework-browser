*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Scroll To With Element
    New Page    ${LOGIN_URL}
    Set Viewport Size    300    400
    ${src} =    Get Page Source
    ${position} =    Get Scroll Position
    Log    ${src}
    Log    ${position}
    Scroll To    id=draggable    vertical=-50
    ${position} =    Get Scroll Position
    Scroll To    id=draggable    vertical=50
    ${position} =    Get Scroll Position
    Scroll To    id=draggable    vertical=-500
    ${position} =    Get Scroll Position
    Scroll To    id=draggable    vertical=500
    ${position} =    Get Scroll Position
    Scroll To    id=draggable    vertical=-183    horizontal=-100
    ${position} =    Get Scroll Position
    Take Screenshot
    Close Page
