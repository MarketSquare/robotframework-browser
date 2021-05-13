*** Settings ***
Resource          imports.resource
Library           Browser

*** Test Cases ***
Can access web component
    New Page    ${WEBCOMPONENT_PAGE}
    Get Text    my-web-component    ==    Hello hoard
    Get Text    id=container >> id=inside    ==    Inside Shadow DOM
