*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${TABLES_URL}


*** Test Cases ***
Test Table
    [Timeout]    6000 sec
    Get Table Cell Index    "141g"
    Get Table Row Index    *css=tr >> "STM32F411"
