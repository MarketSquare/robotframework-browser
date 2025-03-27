*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Retry Assertions For    1s
Test Setup          Go To    ${LOGIN_URL}

*** Variables ***
${FailureScreenshot} =              ${OUTPUT_DIR}${/}Register_Keyword_To_Run_On_Failure_FAILURE_SCREENSHOT_1.png
${FailureScreenshot2} =             ${OUTPUT_DIR}${/}Register_KW_On_Failure_With_Unicode____FAILURE_SCREENSHOT_1.png
${FailureScreenshot3} =             ${OUTPUT_DIR}${/}Register_Kw_With_Custom_Path_Named_Not_First_FAILURE_SCREENSHOT_1.png
${FailureScreenshot4_no_ext} =      ${OUTPUT_DIR}${/}myfailure_screenshot
${FailureScreenshot4} =             ${FailureScreenshot4_no_ext}.png
${FailureScreenshot5_no_ext} =      ${OUTPUT_DIR}${/}myfailure_screenshot_44
${FailureScreenshot5} =             ${FailureScreenshot5_no_ext}.png

*** Test Cases ***
Register Keyword To Run On Failure
    ${count_before} =    Glob Files    ${OUTPUT_DIR}/browser/screenshot
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot}
    ${count_after} =    Glob Files    ${OUTPUT_DIR}/browser/screenshot
    Lists Should Be Equal    ${count_before}    ${count_after}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot}

Register Kw With Custom Path Named
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot    filename=${FailureScreenshot4_no_ext}
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot4}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot4}

Register Kw With Custom Path Positional
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot    ${FailureScreenshot5_no_ext}
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot5}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot5}

Register Kw With Custom Path Named Not First
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot    selector=css=input#username_field
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot3}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot3}

Register KåWä On Failure With Unicode " 💩 "
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot2}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot2}

Register Keyword With Arguments
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot    image-{index}    fullPage=True
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/image-1.png
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${OUTPUT_DIR}/browser/screenshot/image-1.png

Register Keyword With Named Arguments
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot    ${FailureScreenshot3}    fullPage=True
    ${with_args} =    Register Keyword To Run On Failure    Take Screenshot    ${FailureScreenshot3}    fullPage=True
    Register Keyword To Run On Failure    ${with_args}
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot3}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot3}

Register Keyword With Wrong Arguments
    TRY
        Register Keyword To Run On Failure
        ...    Take Screenshot
        ...    image-{index}
        ...    ${NONE}
        ...    True
    EXCEPT    Keyword 'Take Screenshot' expected 0 to 2 non-named arguments, got 3.    AS    ${error}
        Log    ${error}
    END

Register User Keyword
    ${prev} =    Register Keyword To Run On Failure    Custom User Keyword    Foobar
    Type Text    css=input#username_field    username
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    Register Keyword To Run On Failure    ${prev}
    File Should Exist    ${OUTPUT_DIR}/log_file.log
    [Teardown]    Remove File    ${OUTPUT_DIR}/log_file.log

Register Get Page Source
    [Documentation]
    ...    LOG 3.1:4    DEBUG    Page source obtained successfully.
    ...    LOG 3.1:5    INFO    GLOB:    *playwright-log.txt for additional details.
    [Tags]    no-iframe
    ${prev} =    Register Keyword To Run On Failure    Get Page Source
    Type Text    css=input#username_field    username
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)*
    ...    Get Text    css=input#username_field    ==    not_username
    [Teardown]    Register Keyword To Run On Failure    ${prev}

Register None
    ${prev1} =    Register Keyword To Run On Failure    NONE
    Should Not Be Empty    ${prev1.name}
    Should Not Be Empty    ${prev1.args}
    Should Not Be Empty    ${prev1.original_name}
    Should Be Empty    ${prev1.kwargs}
    ${prev2} =    Register Keyword To Run On Failure    ${prev1}
    Should Not Be True    ${prev2.name}
    Should Not Be True    ${prev2.args}
    Should Not Be True    ${prev2.original_name}
    Should Not Be True    ${prev2.kwargs}
    Log    ${prev2}
    Log    ${prev1}

*** Keywords ***
Setup
    Ensure Open Page
    Set Retry Assertions For    0

Custom User Keyword
    [Arguments]    ${log}
    Create File    ${OUTPUT_DIR}/log_file.log    ${log}
