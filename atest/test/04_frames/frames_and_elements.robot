*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${FRAMES_BUG_REPORT}

*** Test Cases ***
Get Text With Element
    ${count} =    Get Elements    css=th
    Length Should Be    ${count}    3
    Get Text    ${count}[0]
    Get Text    ${count}[1]
    Get Text    ${count}[2]

Get Text With Element From Frames
    ${count} =    Get Elements    css=iframe[id="test frame"] >>> css=th
    Length Should Be    ${count}    3
    Get Text    ${count}[2]
    Get Text    ${count}[1]
    Get Text    ${count}[0]
