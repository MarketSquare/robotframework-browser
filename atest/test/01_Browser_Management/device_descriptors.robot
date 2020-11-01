*** Settings ***
Library           Browser
Resource          imports.resource

*** Variables ***
${device_json}=
...               json.loads('''{
...               "userAgent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3765.0 Mobile Safari/537.36",
...               "viewport": {
...               "width": 360,
...               "height": 640
...               },
...               "deviceScaleFactor": 3,
...               "isMobile": true,
...               "hasTouch": true,
...               "defaultBrowserType": "chromium"
...               }''')

*** Test Cases ***
Get Devices
    # Has too much content for a sane assertion here
    ${devices}=    Get Devices

Get Device
    ${should_be}=    Evaluate    ${device_json}
    ${device}=    Get Device    Galaxy S5
    Should Be Equal    ${device}    ${should_be}

Get Invalid Device Errors
    Run Keyword And Expect Error    No device named NonExistentDeviceName    Get Device    NonExistentDeviceName

Descriptor Properly sets context settings
    ${device}=    Get Device    Galaxy S5
    New Context    &{device}
    New Page
    Get Viewport Size    ALL    ==    { "width": 360 , "height": 640 }
    Verify Browser Type    chromium
