*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser    about:blank    browser=${BROWSER}    headless=${HEADLESS}
Suite Teardown    Close Browser
