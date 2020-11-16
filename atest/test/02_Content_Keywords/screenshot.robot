*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Variables ***
${FailureScreenshot}=    ${OUTPUT_DIR}${/}Register_Keyword_To_Run_On_Failure_FAILURE_SCREENSHOT_1.png
${TestScreenshot}=    ${OUTPUT_DIR}${/}test_screenshot

*** Test Cases ***
Register Keyword To Run On Failure
    Type Text    css=input#username_field    username
    ${prev}=    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get TextField Value    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot}

Screenshotting By Using Keyword
    Take Screenshot    ${TestScreenshot}
    File Should Exist    ${TestScreenshot}.png
    [Teardown]    Remove File    ${TestScreenshot}.png

Element Screenshotting
    Take Screenshot    selector=\#username_field
    File Should Exist    ${OUTPUT_DIR}/robotframework-browser-screenshot-1.png
    [Teardown]    Remove File    ${OUTPUT_DIR}/*.png

If Element Not Found Screenshot Should Fail
    Run Keyword And Expect Error
    ...    Error: Tried to capture element screenshot, element '#not_there' wasn't found.
    ...    Take Screenshot    selector=\#not_there
    [Teardown]    Remove File    ${OUTPUT_DIR}/*.png

ElementHandle Screenshotting
    ${ref}=    Get Element    \#username_field
    Take screenshot    ${TestScreenshot}    ${ref}
    File Should Exist    ${TestScreenshot}.png
    [Teardown]    Remove File    ${TestScreenshot}.png

Screenshotting Without Path
    Remove File    ${OUTPUT_DIR}/*.png
    ${path1}=    Take Screenshot
    File Should Exist    ${path1}
    ${path2}=    Take Screenshot
    File Should Exist    ${path2}
    Should Not Be Equal    ${path1}    ${path2}
    [Teardown]    Remove Files    ${path1}    ${path2}

Screenshot Filename Incrementation
    [Documentation]
    ...    LOG 2:4    </td></tr><tr><td colspan="3"><a href="test_screenshot_1.png"><img src="test_screenshot_1.png" width="800px"></a>
    ...    LOG 3:4    </td></tr><tr><td colspan="3"><a href="test_screenshot_2.png"><img src="test_screenshot_2.png" width="800px"></a>
    Take Screenshot    ${TestScreenshot}_{index}
    Take Screenshot    ${TestScreenshot}_{index}
    File Should Exist    ${TestScreenshot}_1.png
    File Should Exist    ${TestScreenshot}_2.png
    [Teardown]    Remove File    ${TestScreenshot}_*.png

Embed ScreenShot To log.html File
    [Documentation]
    ...    LOG 2:4    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    ${path} =    Take screenshot    EMBED
    Should Not Exist    ${OUTPUT_DIR}/EMBED*
    Should Be Equal    ${path}    EMBED

Embed Element Picture To log.html File
    [Documentation]
    ...    LOG 2:4    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    ${path} =    Take screenshot    EMbeD    selector=\#username_field
    Should Not Exist    ${OUTPUT_DIR}/EM??D*
    Should Be Equal    ${path}    EMBED

Screenshot Without Active Page
    Close Page    ALL
    Run Keyword And Expect Error
    ...    Error: Tried to take screenshot, but no page was open.
    ...    Take Screenshot
