*** Settings ***
Resource        imports.resource

Suite Setup     Prepare Suite

Force Tags      no-iframe

*** Variables ***
@{permissions} =    geolocation
...                 midi
...                 notifications
...                 camera
...                 microphone
...                 background-sync
...                 accelerometer
...                 gyroscope
...                 magnetometer
...                 clipboard-read
...                 clipboard-write
...                 payment-handler

*** Test Cases ***
Set Geolocation On Browser Startup
    [Tags]    no-docker-pr
    Start Context With Geolocation
    Check Geolocation    42    -42.42

Set Geolocation
    [Tags]    no-docker-pr
    [Setup]    Start Context With Geolocation
    Set Geolocation    72.56    145.89    0.23
    Check Geolocation    72.56    145.89

Enable Geolocation
    [Tags]    no-docker-pr
    [Setup]    Start Context Without Geolocation
    Set Browser Timeout    timeout=500ms    scope=Test
    Set Geolocation    11.11    22.22    33.33
    Run Keyword And Expect Error    *    Check Geolocation    11.11    22.22
    Grant Permissions    geolocation    midi    origin=${GEOLOCATION_URL}
    Set Geolocation    72.56    145.89    0.23
    Check Geolocation    72.56    145.89

Grant Permissions With All Permissions
    Start Context Without Geolocation
    Grant Permissions    @{permissions}    origin=${GEOLOCATION_URL}
    Check Permissions

New Context With All Permissions
    New Context    permissions=${permissions}
    New Page    ${GEOLOCATION_URL}
    Check Permissions

Grant Permissions With All Underscore Permissions
    @{u_permissions} =    Get Underscore Permissions
    Start Context Without Geolocation
    Grant Permissions    @{u_permissions}    origin=${GEOLOCATION_URL}
    Check Permissions

New Context With All Underscore Permissions
    ${u_permissions} =    Get Underscore Permissions
    New Context    permissions=${u_permissions}
    New Page    ${GEOLOCATION_URL}
    Check Permissions

Clear Geolocation Permission
    [Setup]    Start Context With Geolocation
    Set Browser Timeout    timeout=500ms    scope=Test
    Clear Permissions
    Set Geolocation    72.56    145.89    0.23
    Run Keyword And Expect Error    *    Check Geolocation    72.56    145.89

Enable Geolocation On Wrong Origin
    [Setup]    Start Context Without Geolocation
    Set Browser Timeout    timeout=500ms    scope=Test
    Grant Permissions    geolocation    origin=http://www.example.com
    Set Geolocation    72.56    145.89    0.23
    Run Keyword And Expect Error    *    Check Geolocation    72.56    145.89

Set Geolocation Out Of Bounds
    [Setup]    Start Context With Geolocation
    Set Browser Timeout    timeout=500ms    scope=Test
    Run Keyword And Expect Error
    ...    Error: browserContext.setGeolocation: geolocation.latitude: precondition *
    ...    Set Geolocation    1072    3
    Run Keyword And Expect Error
    ...    Error: browserContext.setGeolocation: geolocation.longitude: precondition *
    ...    Set Geolocation    3    765.89

New Persistent Context With All Permissions
    New Persistent Context    url=${GEOLOCATION_URL}    permissions=${permissions}
    Check Permissions
    [Teardown]    Close Browser    ALL

New Persistent Context With All Underscore Permissions
    ${u_permissions} =    Get Underscore Permissions
    New Persistent Context    url=${GEOLOCATION_URL}    permissions=${u_permissions}
    Check Permissions
    [Teardown]    Close Browser    ALL

*** Keywords ***
Prepare Suite
    Close Browser    ALL

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

Check Permissions
    FOR    ${permisison}    IN    @{permissions}
        ${res} =    Evaluate JavaScript
        ...    ${None}
        ...    async () => await navigator.permissions.query({name:'${permisison}'}).then((result) => result.state)
        Should Be Equal    ${res}    granted
    END

Get Underscore Permissions
    RETURN    ${{[permission.replace('-', '_') for permission in $permissions]}}
