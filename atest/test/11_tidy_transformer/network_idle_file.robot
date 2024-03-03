*** Settings ***
Test Tags    tidy-transformer

*** Test Cases ***
Parsing Wait Until Network Is Idle To Wait For Load State
    ${not used} =  New Context    # This is not changed
    Wait Until Network Is Idle    timeout=0.1s
    Wait Until Network Is Idle
    Wait Until Network Is Idle    timeout=0.1s    # Comment should be preserved
    Browser.Wait Until Network Is Idle    timeout=1.2s    # Comment should be preserved
    ${not used} =       New Context    # This is not changed
