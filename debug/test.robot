*** Settings ***
Library     Browser


*** Test Cases ***
Test
    New Browser    chromium    headless=False
    New Context
    New Page    https://robotframework.org/code
    ${p}    Promise To    Click    text="log.html"    left    position_x=10    position_y=5
    Click    "Run"
    Wait For     ${p}