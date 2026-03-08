*** Settings ***
Library         OperatingSystem
Resource        imports.resource

Suite Setup     Check Screenshots Before

Force Tags      slow

*** Test Cases ***
Failing With Screenshot 1
    New Page    ${ERROR_URL}
    TRY
        Click    .nonexisting
    EXCEPT    TimeoutError*    type=GLOB    AS    ${error}
        Log    ${error}
    END

Failing With Screenshot 2
    New Page    ${ERROR_URL}
    TRY
        Click    .nonexisting
    EXCEPT    TimeoutError*    type=GLOB    AS    ${error}
        Log    ${error}
    END

Failing With Screenshot 3
    New Page    ${ERROR_URL}
    TRY
        Click    .nonexisting
    EXCEPT    TimeoutError*    type=GLOB    AS    ${error}
        Log    ${error}
    END

Failing When Selector Is Not Found When Get Attribute
    New Page    ${CLOCK_URL}
    TRY
        Get Attribute    .nonexisting4    attribute=data-testid
    EXCEPT    TimeoutError*    type=GLOB    AS    ${error}
        Log    ${error}
    END

Failing When Attribute Is Not Found When Get Attribute
    New Page    ${CLOCK_URL}
    TRY
        Get Attribute    selector=#current-time    attribute=nonexisting-attribute
    EXCEPT    AttributeError: Attribute 'nonexisting-attribute' not found!    type=GLOB    AS    ${error}
        Log    ${error}
    END

Check Screenshots
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-1.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-2.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-3.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-4.png
    File Should Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-5.png
    File Should Not Exist    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-6.png

*** Keywords ***
Check Screenshots Before
    Set Browser Timeout    3s    scope=Suite
    FOR    ${index}    IN RANGE    1    7
        Remove File    ${OUTPUT DIR}/browser/screenshot/fail-screenshot-${index}.png
    END
