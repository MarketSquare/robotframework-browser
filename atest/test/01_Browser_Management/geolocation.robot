*** Settings ***
Resource          imports.resource

*** Test Cases ***
Set Geolocation On Browser Startup
    ${location} =    Create Dictionary    latitude=42.0    longitude=-42.42    accuracy=0.3
    ${permissions} =    Create List    geolocation
    New Context    geolocation=${location}    permissions=${permissions}
    New Page    ${GEOLOCATION_URL}
    Check Geolocation    42    -42.42

*** Keywords ***
Check Geolocation
    [Arguments]    ${latitude}    ${longitude}
    Click    id=button_location
    Take Screenshot
    Get Text    id=latitudeValue    equal    Latitude: ${latitude}
    Get Text    id=longitudeValue    equal    Longitude: ${longitude}
