*** Settings ***
Library     Browser    timeout=3s
Resource    ../variables.resource

*** Test Cases ***
Open With Extension
    ${args} =    Set Variable
    ...    ["--disable-extensions-except=./ublock/uBlock0.chromium", "--load-extension=./ublock/uBlock0.chromium"]

    New Persistent Context    headless=False    args=${args}
    New Page    https://www.iltalehti.fi/
    Wait Until Network Is Idle
    Sleep    10s

    Take Screenshot    filename=EMBED

    Close Browser

    New Browser    headless=False
    New Context
    New Page    https://www.iltalehti.fi/
    Sleep    10s
    Take Screenshot    filename=EMBED
