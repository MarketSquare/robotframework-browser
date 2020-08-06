*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Variables ***
${FailureScreenshot}=    ${OUTPUT_DIR}${/}Test_screenshotting_failing_test_FAILURE_SCREENSHOT.png
${TestScreenshot}=    ${OUTPUT_DIR}${/}test_screenshot

*** Test Cases ***
Test screenshotting failing test
    [Teardown]    Remove File    ${FailureScreenshot}
    Type Text    css=input#username_field    username
    Run Keyword And Expect Error    *`username` should be `not_username`    Get TextField Value    css=input#username_field    ==    not_username
    Should Exist    ${FailureScreenshot}

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
