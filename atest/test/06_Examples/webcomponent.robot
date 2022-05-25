*** Settings ***
Library     Browser
Resource    imports.resource

*** Test Cases ***
Can Access Web Component
    New Page    ${WEBCOMPONENT_PAGE}
    Get Text    my-web-component    ==    Hello hoard
    Get Text    id=container >> id=inside    ==    Inside Shadow DOM
