*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${TABLES_URL}

*** Test Cases ***
Test Table
    [Timeout]    6000 sec
    ${cell} =    Get Table Cell Index    "141g"
    ${row} =    Get Table Row Index    "STM32F411"
    ${elem} =    Get Table Cell Element    table    "Babyhawk"    "Weight"
    Get Text    ${elem}    ==    141g
    Highlight Elements    ${elem}
