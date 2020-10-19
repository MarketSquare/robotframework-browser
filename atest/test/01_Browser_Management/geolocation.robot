*** Settings ***
Resource          imports.resource

*** Test Cases ***
Set Geolocation On Browser Startup
    Start Context With Geolocation
    Check Geolocation    42    -42.42

Set Geolocation
    [Setup]    Start Context With Geolocation
    Set Geolocation    72.56    145.89    0.23
    Check Geolocation    72.56    145.89

Set Geolocation Out Of Bounds
    [Setup]    Start Context With Geolocation
    Run Keyword And Expect Error
    ...    browserContext.setGeolocation: geolocation.latitude: precondition *
    ...    Set Geolocation    1072    3
    Run Keyword And Expect Error
    ...    browserContext.setGeolocation: geolocation.longitude: precondition *
    ...    Set Geolocation    3    765.89

*** Keywords ***
Check Geolocation
    [Arguments]    ${latitude}    ${longitude}
    Click    id=button_location
    Take Screenshot
    Get Text    id=latitudeValue    equal    Latitude: ${latitude}
    Get Text    id=longitudeValue    equal    Longitude: ${longitude}

Start Context With Geolocation
    ${location} =    Create Dictionary    latitude=42.0    longitude=-42.42    accuracy=0.3
    ${permissions} =    Create List    geolocation
    New Context    geolocation=${location}    permissions=${permissions}
    New Page    ${GEOLOCATION_URL}
