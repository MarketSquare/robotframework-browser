*** Settings ***
Resource            imports.resource

*** Test Cases ***
This should not be logged to file playwright_log.txt
    Log    This should not be logged to file
    FOR    ${i}    IN RANGE    5
        Log    This should not be logged to file ${i}
    END
