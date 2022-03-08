*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${TABLES_URL}

*** Test Cases ***
Test Table
    [Timeout]    6000 sec
    ${cell} =    Get Table Cell Index    id=table1 >> "141g"
    ${row} =    Get Table Row Index    id=table1 >> "STM32F411"
    ${elem} =    Get Table Cell Element    id=table1    "Babyhawk"    "Weight"
    Get Text    ${elem}    ==    141g
    ${elem} =    Get Table Cell Element    id=table1    2    4
    ${elem} =    Get Table Cell Element    id=table2    -1    4
    Highlight Elements    ${elem}
