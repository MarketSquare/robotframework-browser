*** Settings ***
Library     Browser    timeout=5s    retry_assertions_for=3s
Resource    imports.resource

*** Test Cases ***
Promise to wait for response
    New Page    url=http://www.google.com
    ${promise} =    Promise To    Wait For Response
    ${body} =    Wait For  ${promise}
