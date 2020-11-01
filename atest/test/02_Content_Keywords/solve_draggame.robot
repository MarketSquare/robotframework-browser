*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${DRAGGAME_URL}

*** Test Cases ***
Move obstacle to goal and make a goal
    Get text    h2    ==    Put the circle in the goal
    Drag And Drop    css=.obstacle    css=.goal
    Drag And Drop    css=.circle    css=.goal
    Get text    h2    ==    GOAL!!

Move Obstacle away and drag and Drop
    Hover    "Obstacle"
    Mouse Button    down
    Mouse Move Relative To    "Obstacle"    500
    Mouse Button    up
    Drag And Drop    "Circle"    "Goal"

Test
    [Setup]    New Page
    FOR    ${i}    IN RANGE    20
        Go To    ${SHELLGAME_URL}
        Mouse Move Relative To    id=indicator    -100
        Mouse Button    click
        Get Text    h1    ==    CORRECT :D
    END
