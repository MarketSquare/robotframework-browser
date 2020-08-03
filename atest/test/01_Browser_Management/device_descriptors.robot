*** Settings ***
Library           Browser    timeout=1ms
Resource          imports.resource
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${device_json}=
...               json.loads("""{
...               "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
...               "viewport": { "width": 375, "height": 812 },
...               "deviceScaleFactor": 3,
...               "isMobile": true,
...               "hasTouch": true
...               }""")

*** Test Cases ***
Get Devices
    # Has too much content for a sane assertion here
    ${devices}=    Get Devices

Get Device
    ${should_be}=    Evaluate    ${device_json}
    ${device}=    Get Device    iPhone X
    Should Be Equal    ${device}    ${should_be}

Get Invalid Device Errors
    Run Keyword And Expect Error    No device named NonExistentDeviceName    Get Device    NonExistentDeviceName

Descriptor Properly sets context settings
    ${device}=    Get Device    iPhone X
    New Context    &{device}
    New Page
    Get Viewport Size    ==    { "width": 375, "height": 812 }
