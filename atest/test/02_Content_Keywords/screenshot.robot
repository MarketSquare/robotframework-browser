*** Settings ***
Resource          imports.resource
Suite Setup       New Page  ${LOGIN URL}

*** Variables ***
${failure_screnshot}    ${OUTPUT_DIR}${/}Test_screenshotting_failing_test_FAILURE_SCREENSHOT.png
${test_screenshot}    ${OUTPUT_DIR}${/}test_screenshot

*** Test Cases ***
Test screenshotting failing test
    [Teardown]    Remove File    ${failure_screnshot}
    Type Text    css=input#username_field    username
    Run Keyword And Expect Error    *`username` should be `not_username`    Get TextField Value    css=input#username_field    ==    not_username
    Should Exist    ${failure_screnshot}

Test screenshotting by using keyword
    [Teardown]    Remove File    ${test_screenshot}.png
    Take Page Screenshot    ${test_screenshot}
    Should Exist    ${test_screenshot}.png
