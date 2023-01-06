*** Settings ***
Library     Browser
Library     Collections
Resource    ../variables.resource

*** Test Cases ***
Test Insert
    New Browser    headless=False
    New Page       ${FORM_URL}
    ${elements} =           Get Elements        select
    FOR     ${element}      IN  @{elements}
            Log             ${element}
            ${value}=       Get Property    ${element}      id
            Log             ${value}
            ${attributes}=  Get Attribute Names     ${element}
            Log To Console     ${attributes}
            Highlight Elements    ${element}
            Take Screenshot
            FOR     ${attribute}    IN   @{attributes}
                Log      ${attribute}
            END
    END
    Close Browser           CURRENT