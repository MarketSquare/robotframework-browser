*** Settings ***
Library      Browser    jsextension=atest/test/05_JS_Tests/funky.js
Resource     imports.resource

Test Tags    no-iframe    no-docker-pr

*** Test Cases ***
Relative jsextension Is Resolved Against The Working Directory
    New Page    ${LOGIN_URL}
    My Funky Keyword    h1
    Get Text    h1    ==    Funk yeah!
