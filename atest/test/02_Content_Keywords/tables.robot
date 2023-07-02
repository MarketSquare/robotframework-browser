*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${TABLES_URL}

*** Test Cases ***
Get Table Cell Index By Text
    ${index} =    Get Table Cell Index    id=table1 >> "Babyhawk"
    Should Be Equal    ${index}    ${2}

Assert Table Cell Index By Text
    Get Table Cell Index    id=table1 >> "Babyhawk"    ==    2
    Get Table Cell Index    id=table2 >> "Babyhawk"    ==    2
    Get Table Cell Index    id=table2 >> "MERICA"    ==    3
    Get Table Cell Index    id=table2 >> id=drone3    ==    3
    Get Table Cell Index    *css=td > table >> "two"    ==    3

Get Table Cell Index From Subtable
    Get Table Cell Index    td > table >> "two"    ==    1

Get Table Row Index From Cell
    Get Table Row Index    id=table1 >> "Babyhawk"    ==    0
    Get Table Row Index    table#table2 > tfoot > tr:nth-child(1)    ==    6
    Get Table Row Index    td > table >> "2"    ==    1

Get Table Row Index From Row
    Get Table Row Index    table#table2 > thead > tr:nth-child(1)    ==    0
    Get Table Row Index    table#table2 > tbody > tr:nth-child(1)    ==    1
    Get Table Row Index    table#table2 > tbody > tr:nth-child(2)    ==    2
    Get Table Row Index    table#table2 > tbody > tr:nth-child(3)    ==    3
    Get Table Row Index    table#table2 > tbody > tr:nth-child(4)    ==    4
    Get Table Row Index    table#table2 > tbody > tr:nth-child(5)    ==    5
    Get Table Row Index    table#table2 > tfoot > tr:nth-child(1)    ==    6
    Get Table Row Index    "two"    ==    0
    Get Table Row Index    "1"    ==    1

Get Table Row Index From Table Element
    Get Table Row Index    td > table    ==    -1
    ${index} =    Get Table Row Index    td > table
    Should Be Equal    ${index}    ${-1}

Check Return Type
    Get Table Row Index    id=table2    validate    isinstance(value, int)
    Get Table Row Index    id=table2 >> "141g"    validate    isinstance(value, int)
    Get Table Cell Index    id=table2 >> "141g"    validate    isinstance(value, int)

Get Table Cell Element
    ${e} =    Get Table Cell Element    id=table2    "Babyhawk"    "Weight"
    Get Text    ${e}    ==    141g
    ${e} =    Get Table Cell Element    id=table1    "Babyhawk"    "Weight"
    Get Text    ${e}    ==    141g
    ${subtable_parent} =    Get Table Cell Element    id=table2    "MERICA"    "Weight"
    ${e} =    Get Table Cell Element    ${subtable_parent} >> :scope > table    "two"    "1"
    Get Text    ${e}    ==    2
    ${e} =    Get Table Cell Element    td > table    1    1
    Get Text    ${e}    ==    2
    ${e} =    Get Table Cell Element    td > table    -1    -1
    Get Text    ${e}    ==    2
    ${e} =    Get Table Cell Element    td > table    -1    -1
    Get Text    ${e}    ==    2

Click Table Element
    ${e} =    Get Table Cell Element    id=table1    "Smart35"    -1
    Click    ${e} >> input
    Get Text    id=selection    ==    Smart35
    ${e} =    Get Table Cell Element    id=table2    "Babyhawk"    -1
    Click    ${e} >> input
    Get Text    id=selection    ==    Babyhawk
    ${e} =    Get Table Cell Element    id=table2    "MERICA"    -1
    Click    ${e} >> input
    Get Text    id=selection    ==    MERICA

Select Wrong Table Element
    ${subtable_parent} =    Get Table Cell Element    id=table2    "MERICA"    "Weight"
    Run Keyword And Expect Error
    ...    REGEXP:ValueError: Selector id=.*? must select a <table> element but selects <td>\.
    ...    Get Table Cell Element    ${subtable_parent}    "two"    "1"

Get Table Cell Element With Multiple Elements
    Set Strict Mode    False
    ${e} =    Get Table Cell Element    table    "Babyhawk"    "Weight"
    Get Text    ${e}    ==    141g
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *strict mode violation*
    ...    Get Table Cell Element
    ...    table
    ...    "Babyhawk"
    ...    "Weight"
