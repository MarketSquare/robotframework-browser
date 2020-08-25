*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Variables ***
${FailureScreenshot}=    ${OUTPUT_DIR}${/}Register_Keyword_To_Run_On_Failure_FAILURE_SCREENSHOT_1.png
${TestScreenshot}=    ${OUTPUT_DIR}${/}test_screenshot

*** Test Cases ***
Register Keyword To Run On Failure
    [Teardown]    Remove File    ${FailureScreenshot}
    Type Text    css=input#username_field    username
    ${prev}=    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error    *`username` should be `not_username`    Get TextField Value    css=input#username_field    ==    not_username
    Should Exist    ${FailureScreenshot}
    Register Keyword To Run On Failure    ${prev}

Test screenshotting by using keyword
    [Teardown]    Remove File    ${TestScreenshot}.png
    Take Screenshot    ${TestScreenshot}
    Should Exist    ${TestScreenshot}.png

Test Element Screenshotting
    [Teardown]    Remove File    ${TestScreenshot}.png
    Take Screenshot    ${TestScreenshot}    selector=\#username_field
    Should Exist    ${TestScreenshot}.png

Test ElementHandle screenshotting
    [Teardown]    Remove File    ${TestScreenshot}.png
    ${ref}=    Get Element    \#username_field
    Take screenshot    ${TestScreenshot}    ${ref}
    Should Exist    ${TestScreenshot}.png

Test screenshotting without path
    ${path}=    Take Screenshot
    Should Exist    ${path}
    Remove File    ${path}

Test screenshot filename incrementation
    [Teardown]    Remove Screenshot Files
    Take Screenshot    ${TestScreenshot}_{index}
    Take Screenshot    ${TestScreenshot}_{index}
    Should Exist    ${TestScreenshot}_1.png
    Should Exist    ${TestScreenshot}_2.png
