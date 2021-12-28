*** Settings ***
Resource            imports.resource

Test Setup          New Page    ${FORMATTER_URL}
Test Teardown       Set Assertion Formatters    {"Get Text": []}

*** Test Cases ***
Normalize &nbsp;
    Set Assertion Formatters    {"Get Text": ["normalize spaces"]}
    Get Text    id=nbsp    ==    Hello Space

Normalize Spaces Not Applied Fails
    Run Keyword And Expect Error    Text 'Space${SPACE*3}Space' (str) should be 'Space Space' (str)
    ...    Get Text    id=normalize-spaces    ==    Space Space

Normalize Spaces
    Set Assertion Formatters    {"Get Text": ["normalize spaces"]}
    Get Text    id=normalize-spaces    ==    Space Space

Strip Spaces Not Applied Fails
    Run Keyword And Expect Error
    ...    Text '${SPACE*2}Leading and Trailing Spaces${SPACE*2}' (str) should be 'Leading and Trailing Spaces' (str)
    ...    Get Text    id=strip    ==    Leading and Trailing Spaces

Strip Spaces
    Set Assertion Formatters    {"Get Text": ["strip"]}
    Get Text    id=strip    ==    Leading and Trailing Spaces
