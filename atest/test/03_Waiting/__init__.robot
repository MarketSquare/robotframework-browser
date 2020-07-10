*** Settings ***
Resource          imports.resource
Suite Setup       Run Keywords  New Browser    browser=${BROWSER}    headless=${HEADLESS}  AND  New Page
Suite Teardown    Close Browser
