*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${DRAGGAME_URL}

*** Test Cases ***
Move Obstacle To Element And Make A Goal
    Get Text    h2    ==    Put the circle in the goal
    ${box1} =    Get BoundingBox    id=blue-box
    Drag And Drop    id=blue-box    id=invisible-element    steps=10
    ${box2} =    Get BoundingBox    id=blue-box
    Should Not Be Equal As Numbers    ${box1.y}    ${box2.y}
    Drag And Drop    id=red-circle    id=goal-post    steps=10
    Get Text    h2    ==    GOAL!!!
    [Teardown]    Get Text    id=debug-log

Move Obstacle Away And Drag And Drop
    Get Text    h2    ==    Put the circle in the goal
    Hover    id=blue-box
    Mouse Button    down
    Mouse Move Relative To    id=blue-box    200
    Mouse Button    up
    Drag And Drop    id=red-circle    id=goal-post    steps=10
    Get Text    h2    ==    GOAL!!!
    [Teardown]    Get Text    id=debug-log

Test Shell Game By Clicking Indicator
    [Tags]    slow
    [Setup]    New Page
    FOR    ${_}    IN RANGE    20
        Go To    ${SHELLGAME_URL}
        Mouse Move Relative To    id=indicator    -100
        Mouse Button    click
        Get Text    h1    ==    CORRECT :D
    END
