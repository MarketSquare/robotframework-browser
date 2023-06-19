*** Settings ***
Resource            imports.resource

Test Teardown       Close Browser    ALL

*** Test Cases ***
Open Browser With Timeout Of Zero Seconds
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0 seconds
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0 second
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0 s
    New Browser    browser=${BROWSER}    headless=${HEADLESS}    timeout=0s

Open Browser With Default Timeout
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
