*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Variables ***
${FailureScreenshot} =      ${OUTPUT_DIR}${/}Register_Keyword_To_Run_On_Failure_FAILURE_SCREENSHOT_1.png
${FailureScreenshot2} =     ${OUTPUT_DIR}${/}Register_KW_On_Failure_with_unicode____FAILURE_SCREENSHOT_1.png
${FailureScreenshot3} =     ${OUTPUT_DIR}${/}myfailure_screenshot.png

*** Test Cases ***
Register Keyword To Run On Failure
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot}
    Directory Should Not Exist    ${OUTPUT_DIR}/browser/screenshot
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot}

Register KåWä On Failure with unicode " 💩 "
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot2}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot2}

Register kw with custom path
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot    ${FailureScreenshot3}
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot3}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot3}

Register Keyword With Arguments
    Type Text    css=input#username_field    username
    ${prev} =    Register Keyword To Run On Failure    Take Screenshot    ${FailureScreenshot3}    ${EMPTY}    True
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot3}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot3}

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
    ...    LOG 3.1:4    DEBUG    Page source obtained succesfully.
    ${prev} =    Register Keyword To Run On Failure    Get Page Source
    Type Text    css=input#username_field    username
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    [Teardown]    Register Keyword To Run On Failure    ${prev}

Register None
    ${prev1} =    Register Keyword To Run On Failure    NONE
    Should Not Be Empty    ${prev1.name}
    Should Not Be Empty    ${prev1.args}
    Should Not Be Empty    ${prev1.original_name}
    ${prev2} =    Register Keyword To Run On Failure    ${prev1}
    Should Not Be True    ${prev2.name}
    Should Not Be True    ${prev2.args}
    Should Not Be True    ${prev2.original_name}
    Log    ${prev2}
    Log    ${prev1}

*** Keywords ***
Custom User Keyword
    [Arguments]    ${log}
    Create File    ${OUTPUT_DIR}/log_file.log    ${log}
