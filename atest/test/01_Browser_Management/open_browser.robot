*** Settings ***
Resource         imports.resource

Test Teardown    Close Browser    ALL

*** Test Cases ***
Relative executablePath Is Not Relative To The Working Directory
    [Tags]    no-docker-pr
    File Should Exist    pyproject.toml
    # Today the path reaches Playwright unresolved, and Playwright looks for it in the working
    # directory of the Node process; issue #5620 changes this.
    Run Keyword And Expect Error    *executable doesn't exist at pyproject.toml
    ...    New Browser    browser=${BROWSER}    headless=${HEADLESS}    executablePath=pyproject.toml

Open Browser With Timeout Of Zero Seconds
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0 seconds
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0 second
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0 s
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0s

Open Browser With Default Timeout
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
