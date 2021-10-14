*** Settings ***
Resource            imports.resource

Test Teardown       Close Browser    ALL

*** Variables ***
${ARGS}=  ["--user-agent FAKE_AGENT"]

*** Test Cases ***

New Browser with skip_if_exists does not open new browser if matching one exists
    New Browser  skip_if_exists=True
    ${catalog}=  Get Browser Catalog
    New Browser  skip_if_exists=True
    ${new_catalog}=  Get Browser Catalog
    ${length}=  Get Length  ${new_catalog}
    Should Be Equal As Integers    1  ${length}
    Should Be Equal  ${catalog}  ${new_catalog}

New Browser with skip_if_exists opens new browser if no matching one is found
    New Browser  browser=firefox  skip_if_exists=True
    ${catalog}=  Get Browser Catalog
    New Browser  skip_if_exists=True
    ${new_catalog}=  Get Browser Catalog
    ${length}=  Get Length  ${new_catalog}
    Should Be Equal As Integers    2  ${length}
    Should Not Be Equal    ${catalog}  ${new_catalog}

New Browser behaviour with list arguments
    New Browser  args=${ARGS}
    ${catalog}=  Get Browser Catalog
    New Browser  skip_if_exists=True  args=${ARGS}
    ${new_catalog}=  Get Browser Catalog
    Should Be Equal  ${catalog}  ${new_catalog}

    New Browser  skip_if_exists=True  args=["--user-agent DIFFERENT"]
    ${third_catalog}=  Get Browser Catalog
    Should Not Be Equal    ${catalog}  ${third_catalog}


