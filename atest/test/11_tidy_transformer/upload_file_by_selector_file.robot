*** Settings ***
Test Tags       tidy-transformer

*** Test Cases ***
Parsing Wait Until Network Is Idle To Wait For Load State
    ${not used} =    New Context    # This is not changed
    Upload File By Selector    id=file    file.txt    # This is not changed
    Upload File By Selector    selector=id=file    path=file.txt
    Browser.Upload File By Selector    selector=id=file    path=file.txt
    ${not used} =    New Context    # This is not changed
