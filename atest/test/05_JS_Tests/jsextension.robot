*** Settings ***
Library         Browser    jsextension=${CURDIR}/funky.js
Resource        imports.resource

Force Tags      no-iframe

*** Test Cases ***
Promise To Call Custom Js Keyword
    New Page
    ${promise} =    Promise To    My Funky keyword    h1
    Go To    ${LOGIN_URL}
    Wait For    ${promise}
    Get Text    h1    ==    Funk yeah!
