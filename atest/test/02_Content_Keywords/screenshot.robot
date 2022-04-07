*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

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

Screenshotting With Jpeg Extension And Quality Borders
    Take Screenshot    fullPage=True    fileType=jpeg    quality=0    timeout=10s
    ${size_0} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-1.jpeg
    Take Screenshot    fullPage=True    fileType=jpeg    quality=-190    timeout=10s
    ${size_1} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-2.jpeg
    Should Be Equal    ${size_0}    ${size_1}
    Take Screenshot    fullPage=True    fileType=jpeg    quality=100    timeout=10s
    ${size_100} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-3.jpeg
    Take Screenshot    fullPage=True    fileType=jpeg    quality=2023    timeout=10s
    ${size_101} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-4.jpeg
    Should Be Equal    ${size_100}    ${size_101}
    Take Screenshot    fullPage=True    fileType=jpeg    quality=50    timeout=10s
    ${size_50} =    Get File Size    ${OUTPUT_DIR}/browser/screenshot/robotframework-browser-screenshot-5.jpeg
    Should Be True    ${size_0} < ${size_50} < ${size_100}
    [Teardown]    Remove Files    ${OUTPUT_DIR}/browser/screenshot/*.jpeg

If Element Not Found Screenshot Should Fail
    ${timeout} =    Set Browser Timeout    200ms
    Run Keyword And Expect Error
    ...    TimeoutError: locator.screenshot: Timeout 200ms exceeded.*waiting for selector "#not_there"*
    ...    Take Screenshot    selector=\#not_there
    Set Browser Timeout    ${timeout}
    [Teardown]    Remove File    ${OUTPUT_DIR}/*.png

ElementHandle Screenshotting
    ${ref} =    Get Element    \#username_field
    Take Screenshot    ${TestScreenshot}    ${ref}
    File Should Exist    ${TestScreenshot}.png
    [Teardown]    Remove File    ${TestScreenshot}.png

Take Take screenshot With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Take screenshot    selector=//input
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
    ${path} =    Take Screenshot    EMBED
    Should Not Exist    ${OUTPUT_DIR}/EMBED*
    Should Be Equal    ${path}    EMBED

Embed Element Picture To log.html File
    [Documentation]
    ...    LOG 1:4    STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64
    ${path} =    Take Screenshot    EMbeD    selector=\#username_field
    Should Not Exist    ${OUTPUT_DIR}/EM??D*
    Should Be Equal    ${path}    EMBED

Screenshot Without Active Page
    Close Page    ALL
    Run Keyword And Expect Error
    ...    Error: Tried to take screenshot, but no page was open.
    ...    Take Screenshot

Screenshot With Cropping jpg
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
    [Teardown]    Remove File    ${path}

Screenshot With fixed Cropping
    ${path} =    Take Screenshot    crop={"x": 200, "y": 100, "height": 123, "width": 654}
    File Should Exist    ${path}
    ${width}    ${height} =    Get Image Size    ${path}
    Should Be Equal As Integers    ${height}    123
    Should Be Equal As Integers    ${width}    654
    ${color} =    Get Pixel Color    ${path}    ${width//2}    ${height//2}
    Should Be Equal    ${color}    ${{(255,255,255,255)}}
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
