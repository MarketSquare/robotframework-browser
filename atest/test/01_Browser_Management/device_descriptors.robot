*** Settings ***
Library     Browser
Resource    imports.resource

*** Test Cases ***
Get Devices
    # Has too much content for a sane assertion here
    ${devices} =    Get Devices
    Should Be True    ${devices.__len__() >= 6}

Get Device
    ${device} =    Get Device    Galaxy S5
    FOR    ${key}    IN    userAgent    viewport    deviceScaleFactor    isMobile    hasTouch    defaultBrowserType
        Dictionary Should Contain Key    ${device}    ${key}
    END
    Should Be True    ${device.__len__() >= 6}
    Should Be True    ${device}[isMobile]
    Should Be True    ${device}[hasTouch]

Get Device with Screen
    ${device} =    Get Device    iPhone 11
    New Browser
    New Context    &{device}    acceptDownloads=True

Get Invalid Device Errors
    Run Keyword And Expect Error
    ...    Error: No device named NonExistentDeviceName
    ...    Get Device    NonExistentDeviceName

Descriptor Properly sets context settings
    ${device} =    Get Device    Galaxy S5
    New Context    &{device}
    New Page
    Get Viewport Size    ALL    ==    { "width": 360 , "height": 640 }
    Verify Browser Type    chromium
