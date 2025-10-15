*** Settings ***
Resource        imports.resource

Test Setup      Screenshot Timeout

*** Variables ***
${TestScreenshot} =     ${OUTPUT_DIR}${/}test_screenshot

*** Test Cases ***
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
    Run Keyword And Expect Error    *quality is unsupported for the png screenshots*    Take Screenshot
    ...    fullPage=True    fileType=png    timeout=10s    quality=50
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.png

Screenshot Fails Due To Timeout
    Run Keyword And Expect Error    *Error*    Take Screenshot    timeout=1ms
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.png

Screenshot Pass With Right Timeout
    Take Screenshot    fullPage=True    fileType=png    timeout=10s
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.png
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.png

Screenshotting With Jpeg Extension And Quality
    Take Screenshot    fullPage=True    fileType=jpeg    quality=50    timeout=10s
    File Should Exist    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.jpeg
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.jpeg

Screenshotting With Jpeg Extension And Quality Borders
    [Setup]    Screenshot Timeout    ${FORM_URL}    # used form url as login page has too much active elements
    ${difference} =    Set Variable    ${42}    # Seems usually be 28 but use 42 to be safe side
    Take Screenshot    fullPage=True    fileType=jpeg    quality=0    timeout=10s
    ${size_0} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.jpeg
    Take Screenshot    fullPage=True    fileType=jpeg    quality=-190    timeout=10s
    ${size_1} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-2.jpeg
    Numbers Are Close    ${size_0}    ${size_1}    ${difference}
    Take Screenshot    fullPage=True    fileType=jpeg    quality=100    timeout=10s
    ${size_100} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-3.jpeg
    Take Screenshot    fullPage=True    fileType=jpeg    quality=2023    timeout=10s
    ${size_101} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-4.jpeg
    Numbers Are Close    ${size_100}    ${size_101}    ${difference}
    Take Screenshot    fullPage=True    fileType=jpeg    quality=50    timeout=10s
    ${size_50} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-5.jpeg
    Should Be True    ${size_0} < ${size_50} < ${size_100}
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.jpeg

If Element Not Found Screenshot Should Fail
    ${timeout} =    Set Browser Timeout    200ms
    Run Keyword And Expect Error
    ...    *Error: locator.screenshot: Timeout 200ms exceeded.*waiting for locator('#not_there')*
    ...    Take Screenshot    selector=\#not_there
    Set Browser Timeout    ${timeout}
    [Teardown]    Remove File    ${OUTPUT_DIR}/*.png

ElementHandle Screenshotting
    ${ref} =    Get Element    \#username_field
    Take Screenshot    ${TestScreenshot}    ${ref}
    File Should Exist    ${TestScreenshot}.png
    [Teardown]    Remove File    ${TestScreenshot}.png

Take Take Screenshot With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Take Screenshot    selector=//input
    Set Strict Mode    False
    ${path} =    Take Screenshot    browser-strict    selector=//input
    Set Strict Mode    True
    [Teardown]    Remove File    ${path}

Screenshotting Without Path
    Remove File    ${OUTPUT_DIR}/*.png
    ${path1} =    Take Screenshot
    File Should Exist    ${path1}
    ${path2} =    Take Screenshot
    File Should Exist    ${path2}
    Should Not Be Equal    ${path1}    ${path2}
    [Teardown]    Remove Files    ${path1}    ${path2}

Screenshot Filename Incrementation
    [Documentation]
    ...    LOG 1:3    </td></tr><tr><td colspan="3"><a href="test_screenshot_1.png" target="_blank"><img src="test_screenshot_1.png" width="800px"/></a>
    ...    LOG 2:3    </td></tr><tr><td colspan="3"><a href="test_screenshot_2.png" target="_blank"><img src="test_screenshot_2.png" width="800px"/></a>
    Take Screenshot    ${TestScreenshot}_{index}
    Take Screenshot    ${TestScreenshot}_{index}
    Take Screenshot    ${TestScreenshot}_{{index}}_{index}
    Take Screenshot    ${TestScreenshot}
    File Should Exist    ${TestScreenshot}_1.png
    File Should Exist    ${TestScreenshot}_2.png
    File Should Exist    ${TestScreenshot}_{index}_1.png
    File Should Exist    ${TestScreenshot}.png
    [Teardown]    Remove File    ${TestScreenshot}_*.png

Embed ScreenShot To Log.html File
    [Documentation]
    ...    LOG 1:4    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    ${path} =    Take Screenshot    EMBED
    Should Not Exist    ${OUTPUT_DIR}/EMBED*
    Should Be Equal    ${path}    EMBED

Embed Element Picture To Log.html File
    [Documentation]
    ...    LOG 1:*    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    ${path} =    Take Screenshot    EMbeD    selector=\#username_field
    Should Not Exist    ${OUTPUT_DIR}/EM??D*
    Should Be Equal    ${path}    EMBED

Screenshot Without Active Page
    Close Page    ALL
    Run Keyword And Expect Error
    ...    Error: Tried to take screenshot, but no page was open.
    ...    Take Screenshot

Screenshot With Cropping Jpg
    ${box} =    Get BoundingBox
    ...    input >> nth=1
    ...    ALL
    ...    then
    ...    {"x": value["x"] - 10, "y": value["y"] - 10, "width": value["width"] + 20, "height": value["height"] + 20}
    ${path} =    Take Screenshot    fileType=jpeg    crop=${box}
    File Should Exist    ${path}
    Should End With    ${path}    .jpeg
    ${width}    ${height} =    Get Image Size    ${path}
    Should Be Equal As Integers    ${height}    ${box}[height]
    Should Be Equal As Integers    ${width}    ${box}[width]
    [Teardown]    Remove File    ${path}

Screenshot With Cropping, Masking, Omitting Background(png)
    ${box} =    Get BoundingBox
    ...    input >> nth=1
    ...    ALL
    ...    then
    ...    {"x": value["x"] - 10, "y": value["y"] - 10, "width": value["width"] + 20, "height": value["height"] + 20}
    ${path} =    Take Screenshot    crop=${box}    mask=input >> nth=1    omitBackground=True
    File Should Exist    ${path}
    Should End With    ${path}    .png
    ${width}    ${height} =    Get Image Size    ${path}
    Should Be Equal As Integers    ${height}    ${box}[height]
    Should Be Equal As Integers    ${width}    ${box}[width]
    ${color} =    Get Pixel Color    ${path}    1    ${height//2}
    Should Be Equal    ${color}    ${{(0,0,0,0)}}
    ${color} =    Get Pixel Color    ${path}    ${width//2}    ${height//2}
    Should Be Equal    ${color}    ${{(255,0,255,255)}}
    ${color} =    Get Pixel Color    ${path}    ${width//2}    2
    Should Be Equal    ${color}    ${{(255,255,255,255)}}
    ${path} =    Take Screenshot
    ...    EMBED
    ...    fileType=png
    ...    crop=${box}
    ...    mask=input >> nth=1
    ...    omitBackground=True
    ${path 2} =    Take Screenshot    crop=${box}    mask=input >> nth=1    maskColor=#2F4E4A    omitBackground=True
    File Should Exist    ${path 2}
    [Teardown]    Remove Files    ${path}    ${path 2}

Screenshot With Scale
    ${path 1} =    Take Screenshot    EMBED    scale=css
    # File Should Exist    ${path 1}
    ${path 2} =    Take Screenshot    EMBED    scale=device
    # File Should Exist    ${path 2}
    [Teardown]    Remove Files    ${path 1}    ${path 2}

Screenshot With Fixed Cropping
    ${path} =    Take Screenshot    crop={"x": 200, "y": 100, "height": 123, "width": 654}
    File Should Exist    ${path}
    ${width}    ${height} =    Get Image Size    ${path}
    Should Be Equal As Integers    ${height}    123
    Should Be Equal As Integers    ${width}    654
    ${color} =    Get Pixel Color    ${path}    ${width//2}    ${height//2}
    Should Be Equal    ${color}    ${{(255,255,255)}}
    [Teardown]    Remove File    ${path}

Screenshot With Omit Background
    ${path} =    Take Screenshot    crop={"x": 200, "y": 100, "height": 123, "width": 654}    omitBackground=True
    File Should Exist    ${path}
    ${width}    ${height} =    Get Image Size    ${path}
    Should Be Equal As Integers    ${height}    123
    Should Be Equal As Integers    ${width}    654
    ${color} =    Get Pixel Color    ${path}    ${width//2}    ${height//2}
    Should Be Equal    ${color}    ${{(0,0,0,0)}}
    [Teardown]    Remove File    ${path}

Screenshot Returns Base64 And Path
    New Page    ${ELEMENT_STATE_URL}
    ${path} =    Take Screenshot    return_as=path
    ${base64} =    Take Screenshot    return_as=base64
    Type Text    [name="enabled_input"]    Hello
    ${base64_diff} =    Take Screenshot    return_as=base64
    Should Be True    isinstance($path, pathlib.Path)
    ${bytes} =    Evaluate    base64.b64decode($base64)
    Compare Images    ${path.absolute().resolve()}    ${bytes}
    Should Not Be Equal    ${base64}    ${base64_diff}
    ${bytes_diff} =    Evaluate    base64.b64decode($base64_diff)
    TRY
        Compare Images    ${path}    ${bytes_diff}    yes
        Fail    Should have failed
    EXCEPT    AssertionError
        Log    correct error
    END

Screenshot Returns Bytes And Path String
    New Page    ${ELEMENT_STATE_URL}
    ${path} =    Take Screenshot    return_as=path_string
    ${bytes} =    Take Screenshot    return_as=bytes
    Type Text    [name="enabled_input"]    Hello
    ${bytes_diff} =    Take Screenshot    return_as=bytes
    Should Be True    isinstance($path, str)
    Should Be True    isinstance($bytes, bytes)
    Compare Images    ${path}    ${bytes}
    Should Not Be Equal    ${bytes}    ${bytes_diff}
    TRY
        Compare Images    ${path}    ${bytes_diff}    yes
        Fail    Should have failed
    EXCEPT    AssertionError
        Log    correct error
    END

Screenshot On Failure
    [Documentation]
    ...    LOG 6:2    INFO    Highlighting ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements
    ...    LOG 7.1:3    INFO    Highlighting failing selector: input
    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.*
    ${no_highlight} =    Take Screenshot
    Highlight Elements    input    duration=0    mode=playwright
    ${manual_highlight} =    Take Screenshot
    Highlight Elements    ${EMPTY}    duration=0    mode=playwright
    ${integrated_highlight} =    Take Screenshot    highlight_selector=input
    Run Keyword And Expect Error
    ...    *
    ...    Get Text    input    ==    Hello
    Compare Images    ${manual_highlight}    ${integrated_highlight}    error_threshold=100000
    Compare Images
    ...    ${manual_highlight}
    ...    ${OUTPUT_DIR}/browser/screenshot/fail-screenshot-1.png
    ...    error_threshold=100000
    Set Highlight On Failure    False
    Run Keyword And Expect Error
    ...    *
    ...    Get Text    input    ==    Hello
    Run Keyword And Expect Error
    ...    ValueError: Box * has difference of *
    ...    Compare Images
    ...    ${manual_highlight}
    ...    ${OUTPUT_DIR}/browser/screenshot/fail-screenshot-2.png
    ...    error_threshold=100000
    Compare Images    ${no_highlight}    ${OUTPUT_DIR}/browser/screenshot/fail-screenshot-2.png    error_threshold=1000

Failing Selector Variable
    Register Keyword To Run On Failure    Run On Failure Variable Assertion    input >> ../.. >> input    scope=Test
    Run Keyword And Expect Error
    ...    *
    ...    Get Text    input >> ../.. >> input    ==    Hello

Screenshot With UUID
    ${file} =    Take Screenshot    UUID
    ${file} =    Get File Name    ${file}
    Length Should Be    ${file}    36
    Should Match Regexp    ${file}    [a-f0-9]{32}\\.png

Screenshot With Same Filename And No Index
    ${file1} =    Take Screenshot    same_name
    ${file2} =    Take Screenshot    same_name
    Should Be Equal    ${file1}    ${file2}
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/same_name*.png

*** Keywords ***
Run On Failure Variable Assertion
    [Arguments]    ${selector}
    Should Be Equal    ${selector}    ${ROBOT_FRAMEWORK_BROWSER_FAILING_SELECTOR}

Screenshot Timeout
    [Arguments]    ${url}=${LOGIN_URL}
    Set Browser Timeout    1s
    New Page    ${url}
