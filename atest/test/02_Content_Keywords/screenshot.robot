*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Variables ***
${FailureScreenshot}=    ${OUTPUT_DIR}${/}Register_Keyword_To_Run_On_Failure_FAILURE_SCREENSHOT_1.png
${FailureScreenshot2}=    ${OUTPUT_DIR}${/}Register_KW_On_Failure_with_unicode____FAILURE_SCREENSHOT_1.png
${FailureScreenshot3}=    ${OUTPUT_DIR}${/}myfailure_screenshot.png
${TestScreenshot}=    ${OUTPUT_DIR}${/}test_screenshot

*** Test Cases ***
Register Keyword To Run On Failure
    Type Text    css=input#username_field    username
    ${prev}=    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot}

Register KåWä On Failure with unicode " 💩 "
    Type Text    css=input#username_field    username
    ${prev}=    Register Keyword To Run On Failure    Take Screenshot
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot2}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot2}

Register kw with custom path
    Type Text    css=input#username_field    username
    ${prev}=    Register Keyword To Run On Failure    Take Screenshot    ${FailureScreenshot3}
    Run Keyword And Expect Error
    ...    *'username' (str) should be 'not_username' (str)
    ...    Get Text    css=input#username_field    ==    not_username
    File Should Exist    ${FailureScreenshot3}
    Register Keyword To Run On Failure    ${prev}
    [Teardown]    Remove File    ${FailureScreenshot3}

Screenshot By Default Filename
    Take Screenshot
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.png
    [Teardown]    Remove File    ${OUTPUT_DIR}/browser/screenshot/*.png

Screenshotting By Custom Path
    Take Screenshot    ${TestScreenshot}
    File Should Exist    ${TestScreenshot}.png
    [Teardown]    Remove File    ${TestScreenshot}.png

Screenshotting By Custom Filename
    Take Screenshot    TestScreenshot
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/TestScreenshot.png
    [Teardown]    Remove File    ${OUTPUT_DIR}/browser/screenshot/TestScreenshot.png

Element Screenshotting
    Take Screenshot    selector=\#username_field
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.png
    [Teardown]    Remove File    ${OUTPUT_DIR}/browser/screenshot/*.png

Quality Argument Incompatible With Png
    Run Keyword And Expect Error    *quality is unsupported for the png screenshots*    Take Screenshot    fullPage=True    fileType=png    timeout=10s    quality=50
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.png

Screenshot Fails Due To Timeout
    Run Keyword And Expect Error    *TimeoutError*    Take Screenshot    timeout=1ms
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.png

Screenshot Pass With Right Timeout
    Take Screenshot    fullPage=True    fileType=png    timeout=10s
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.png
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.png

Screenshotting With Jpeg Extension And Quality
    Take Screenshot    fullPage=True    fileType=jpeg    quality=50    timeout=10s
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.jpeg
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.jpeg

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
    ...    LOG 1:4    </td></tr><tr><td colspan="3"><a href="test_screenshot_1.png"><img src="test_screenshot_1.png" width="800px"></a>
    ...    LOG 2:4    </td></tr><tr><td colspan="3"><a href="test_screenshot_2.png"><img src="test_screenshot_2.png" width="800px"></a>
    Take Screenshot    ${TestScreenshot}_{index}
    Take Screenshot    ${TestScreenshot}_{index}
    File Should Exist    ${TestScreenshot}_1.png
    File Should Exist    ${TestScreenshot}_2.png
    [Teardown]    Remove File    ${TestScreenshot}_*.png

Embed ScreenShot To log.html File
    [Documentation]
    ...    LOG 1:4    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    ${path} =    Take screenshot    EMBED
    Should Not Exist    ${OUTPUT_DIR}/EMBED*
    Should Be Equal    ${path}    EMBED

Embed Element Picture To log.html File
    [Documentation]
    ...    LOG 1:4    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    ${path} =    Take screenshot    EMbeD    selector=\#username_field
    Should Not Exist    ${OUTPUT_DIR}/EM??D*
    Should Be Equal    ${path}    EMBED

Screenshot Without Active Page
    Close Page    ALL
    Run Keyword And Expect Error
    ...    Error: Tried to take screenshot, but no page was open.
    ...    Take Screenshot
