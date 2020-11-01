*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${DRAGGAME_URL}

*** Test Cases ***
Move obstacle away and make a goal
    Get text    h2    ==    Put the circle in the goal
    Drag And Drop    css=.obstacle    css=.goal
    Drag And Drop    css=.circle    css=.goal
    Get text    h2    ==    GOAL!!
