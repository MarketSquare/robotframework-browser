*** Settings ***
Resource    variables.resource
Library     Collections
Library     DateTime
Library     OperatingSystem
Library     Process
Library     String
Library     Browser
...             timeout=${PLAYWRIGHT_TIMEOUT}
...             enable_playwright_debug=${True}
...             enable_presenter_mode=False
...             selector_prefix=${SELECTOR_PREFIX}
...             highlight_on_failure=True
Library     ../library/common.py
Library     ../library/os_wrapper.py
Library     ../library/show_trace_tool.py
Library     ../library/screenshot.py
Library     ../library/event_delay.py

*** Keywords ***
Open Browser To No Page
    New Browser    ${BROWSER}    headless=${HEADLESS}

Open Browser To Frame Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${FRAMES_URL}

Open Browser To Deep Frame Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${DEEP_FRAMES_URL}

Open Browser To Form Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${FORM_URL}

Open Browser To Login Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${LOGIN_URL}
    Login Page Should Be Open

Login Page Should Be Open
    Get Title    matches    (?i)login

Go To Login Page
    Go To    ${LOGIN_URL}
    Login Page Should Be Open

Login User
    Input Username    demo
    Input Pwd    mode
    Submit Credentials

Input Username
    [Arguments]    ${username}
    Fill Text    input#username_field    ${username}

Input Pwd
    [Arguments]    ${password}
    Fill Secret    input#password_field    $password

Submit Credentials
    Click    css=input#login_button

Welcome Page Should Be Open
    Get Url    ==    ${WELCOME_URL}
    Get Title    ==    Welcome Page

Verify Browser Type
    [Arguments]    ${expectedType}
    Get Browser Catalog    validate    value[0]['type'] == $expectedType

Assert Position
    [Documentation]    Compare the real cursor position to the expected location with given tolerance
    [Arguments]    ${expect_x}    ${expect_y}    ${tol}
    ${Center_Func} =    Set Variable
    ...    {'x': (value["x"] + (value["width"] / 2)), 'y': (value["y"] + (value["height"] / 2))}
    ${Node_Func} =    Set Variable
    ...    {'x': (value["x"]), 'y': (value["y"])}
    ${obj_node} =    Get Boundingbox    id=blue-box    ALL    evaluate    ${Node_Func}
    ${obj_center} =    Get Boundingbox    id=blue-box    ALL    evaluate    ${Center_Func}
    ${x_diff} =    Evaluate    ${obj_node}[x] - ${expect_x}
    ${y_diff} =    Evaluate    ${obj_node}[y] - ${expect_y}
    Log Many    Node x,y: \t${obj_node}[x],\t${obj_node}[y]
    ...    Center x,y: \t${obj_center}[x],\t${obj_center}[y]\nExpected xy \t${expect_x},\t${expect_y}
    ...    X-Diff: ${x_diff}, Y-Diff: ${y_diff}, tolerance: ${tol}
    Should Be True    -${tol} < ${x_diff} and ${x_diff} < ${tol}
    Should Be True    -${tol} < ${y_diff} and ${y_diff} < ${tol}

Suite Cleanup
    IF    "${SUITE STATUS}" == "PASS" and "${SYS_VAR_CLEAN}" == "${True}"
        Delete Files On Teardown
    ELSE
        Log    Suite ${SUITE NAME} status is ${SUITE STATUS}, not running stuie cleaning
    END

Delete Files On Teardown
    Remove Directory    ${OUTPUT_DIR}/browser    recursive=True
    Remove File    ${OUTPUT_DIR}/*.png
    Remove File    ${OUTPUT_DIR}/*.zip
    Remove File    ${OUTPUT_DIR}/*.webm

Ensure Open Page
    [Arguments]    ${url}=${NONE}
    New Browser    ${BROWSER}    headless=${HEADLESS}
    ${IDs} =    Get Page Ids
    IF    len($IDs) == 0
        New Page    ${url}
    ELSE
        Switch To Page    ${IDs}[0]
        IF    $url    Go To    ${url}
        Reload
    END

Ensure Location
    [Arguments]    ${url}
    Ensure Open Page
    ${loc} =    Get Url
    IF    "${url}" != "${loc}"    Go To    ${url}

Switch To Page
    [Arguments]    ${page_id}
    ${cat} =    Get Browser Catalog
    FOR    ${br}    IN    @{cat}
        FOR    ${con}    IN    @{br}[contexts]
            FOR    ${pa}    IN    @{con}[pages]
                IF    "${pa}[id]" == "${page_id}"
                    Switch Page    ${pa}[id]    ${con}[id]    ${br}[id]
                    RETURN
                END
            END
        END
    END
    New Page
