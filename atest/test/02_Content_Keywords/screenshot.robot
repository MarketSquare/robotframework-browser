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
    File Should Exist    ${FailureScreenshot}
    Register Keyword To Run On Failure    ${prev}

Screenshotting By Using Keyword
    [Teardown]    Remove File    ${TestScreenshot}.png
    Take Screenshot    ${TestScreenshot}
    File Should Exist    ${TestScreenshot}.png

Element Screenshotting
    [Teardown]    Remove File    ${TestScreenshot}.png
    Take Screenshot    ${TestScreenshot}    selector=\#username_field
    File Should Exist    ${TestScreenshot}.png

ElementHandle Screenshotting
    [Teardown]    Remove File    ${TestScreenshot}.png
    ${ref}=    Get Element    \#username_field
    Take screenshot    ${TestScreenshot}    ${ref}
    File Should Exist    ${TestScreenshot}.png

Screenshotting Without Path
    [Teardown]    Remove Files    ${path1}    ${path2}
    ${path1}=    Take Screenshot
    File Should Exist    ${path1}
    ${path2}=    Take Screenshot
    File Should Exist    ${path2}
    Should Not Be Equal    ${path1}    ${path2}

Screenshot Filename Incrementation
    [Teardown]    Remove File    ${TestScreenshot}_*.png
    Take Screenshot    ${TestScreenshot}_{index}
    Take Screenshot    ${TestScreenshot}_{index}
    File Should Exist    ${TestScreenshot}_1.png
    File Should Exist    ${TestScreenshot}_2.png

Embed ScreenShot To log.html File
    [Documentation]
    ...    LOG 2:3    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    Take screenshot    EMBED
    Should Not Exist    ${OUTPUT_DIR}/EMBED*

Embed Element Picture To log.html File
    [Documentation]
    ...    LOG 2:3    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    Take screenshot    EMbeD    selector=\#username_field
    Should Not Exist    ${OUTPUT_DIR}/EM??D*
