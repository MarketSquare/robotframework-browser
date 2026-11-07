*** Settings ***
Resource     imports.resource

Test Tags    no-coverage-support    no-windows-support

*** Variables ***
${MESSAGE} =    Robot log message that stays out of the Playwright log

*** Test Cases ***
Test That Logs Messages And Runs A User Keyword
    Log    ${MESSAGE}
    FOR    ${i}    IN RANGE    5
        Log    ${MESSAGE} ${i}
    END
    IF    ${True}    Dummy Keyword For Log File Checking

Playwright Log Holds No Robot Log Messages Or User Keyword Names
    ${log_file} =    Find Playwright Log File
    ${log} =    Get File    ${log_file}
    Log    ${log}
    Should Not Contain    ${log}    ${MESSAGE}
    Should Not Contain    ${log}    Dummy Keyword For Log File Checking
    Should Not Be Empty    ${log}

*** Keywords ***
Dummy Keyword For Log File Checking
    Log    ${MESSAGE}

Find Playwright Log File
    ${files} =    List Files In Directory    ${OUTPUT_DIR}
    IF    'playwright-log.txt' in ${files}
        RETURN    ${OUTPUT_DIR}/playwright-log.txt
    ELSE
        ${files} =    List Files In Directory    ${OUTPUT_DIR}/..
        IF    'playwright-log.txt' in ${files}
            RETURN    ${OUTPUT_DIR}/../playwright-log.txt
        ELSE
            ${files} =    List Files In Directory    ${OUTPUT_DIR}/../..
            IF    'playwright-log.txt' in ${files}
                RETURN    ${OUTPUT_DIR}/../../playwright-log.txt
            END
        END
    END
    Fail    Playwright log file not found in ${OUTPUT_DIR} or its parent directories
