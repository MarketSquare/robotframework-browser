*** Settings ***
Resource        imports.resource

Suite Setup     Close Browser    ALL

*** Test Cases ***
Set Geolocation On Browser Startup
    Start Context With Geolocation
    Check Geolocation    42    -42.42

Set Geolocation
    [Setup]    Start Context With Geolocation
    Set Geolocation    72.56    145.89    0.23
    Check Geolocation    72.56    145.89

Enable Geolocation
    [Tags]    slow
    [Setup]    Start Context Without Geolocation
    Set Geolocation    11.11    22.22    33.33
    Run Keyword And Expect Error    *    Check Geolocation    11.11    22.22
    Grant Permissions    geolocation    midi    origin=${GEOLOCATION_URL}
    Set Geolocation    72.56    145.89    0.23
    Check Geolocation    72.56    145.89

Clear Geolocation Permission
    [Tags]    slow
    [Setup]    Start Context With Geolocation
    Clear Permissions
    Set Geolocation    72.56    145.89    0.23
    Run Keyword And Expect Error    *    Check Geolocation    72.56    145.89

Enable Geolocation On Wrong Origin
    [Tags]    slow
    [Setup]    Start Context Without Geolocation
    Grant Permissions    geolocation    origin=http://www.example.com
    Set Geolocation    72.56    145.89    0.23
    Run Keyword And Expect Error    *    Check Geolocation    72.56    145.89

Set Geolocation Out Of Bounds
    [Setup]    Start Context With Geolocation
    Run Keyword And Expect Error
    ...    Error: browserContext.setGeolocation: geolocation.latitude: precondition *
    ...    Set Geolocation    1072    3
    Run Keyword And Expect Error
    ...    Error: browserContext.setGeolocation: geolocation.longitude: precondition *
    ...    Set Geolocation    3    765.89

*** Keywords ***
Check Geolocation
    [Arguments]    ${latitude}    ${longitude}
    Click    id=button_location
    Get Text    id=latitudeValue    equal    Latitude: ${latitude}
    Get Text    id=longitudeValue    equal    Longitude: ${longitude}

Start Context With Geolocation
    ${location} =    Create Dictionary    latitude=42.0    longitude=-42.42    accuracy=0.3
    ${permissions} =    Create List    geolocation
    New Context    geolocation=${location}    permissions=${permissions}
    New Page    ${GEOLOCATION_URL}

Start Context Without Geolocation
    New Context
    New Page    ${GEOLOCATION_URL}
