*** Settings ***
Library           Browser
Resource          keywords.resource
Test Setup        Open Browser    ${LOGIN URL}    headless=False
Test Teardown     Close Browser

*** Test Cases ***
0.5.0
    Sleep    2s
    Add Style Tag    input#username_field {border: 4px dotted blue;}
    Sleep    2s
    Type Text    input#username_field    demo    delay=600ms
    Sleep    0.5s
    Fill Secret    input#password_field    mode
    Sleep    0.5s
    Click    css=input#login_button
    Sleep    1s
