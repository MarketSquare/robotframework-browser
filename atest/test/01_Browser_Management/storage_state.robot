*** Settings ***
Resource          imports.resource
Suite Setup       New Browser

*** Test Cases ***
Save storage state
    New Context
    New Page    ${LOGIN_URL}
    ${state_file} =    Save Storage State
    File Should Not Be Empty    ${state_file}
