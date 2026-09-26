*** Settings ***
Resource          imports.resource

Suite Setup       Setup
Suite Teardown    Teardown
Test Setup        New Context

Test Tags         slow

*** Test Cases ***
New Page Reports A Document That Never Answered
    [Documentation]
    ...    LOG 1.1:*    INFO    REGEXP: .*Navigation committed: no.*GET \\S+/slowpage\\.html \\[document\\] open for \\d+ ms.*
    Run Keyword And Expect Error    *Timeout*    New Page    ${SLOW_PAGE}

New Page Reports What The Stalled Page Was Still Loading
    [Documentation]
    ...    LOG 1.1:*    INFO    REGEXP: ${COMMITTED_AND_STALLED_IMAGE}
    Run Keyword And Expect Error    *Timeout*    New Page    ${STALLED_PAGE}

Go To Reports What The Stalled Page Was Still Loading
    [Documentation]
    ...    LOG 2.1:*    INFO    REGEXP: ${COMMITTED_AND_STALLED_IMAGE}
    New Page
    Run Keyword And Expect Error    *Timeout*    Go To    ${STALLED_PAGE}

Reload Reports What The Stalled Page Was Still Loading
    [Documentation]
    ...    LOG 3.1:*    INFO    REGEXP: ${COMMITTED_AND_STALLED_IMAGE}
    New Page
    Go To    ${STALLED_PAGE}    wait_until=commit
    Run Keyword And Expect Error    *Timeout*    Reload

Go Back Reports What The Stalled Page Was Still Loading
    [Documentation]
    ...    LOG 4.1:*    INFO    REGEXP: ${COMMITTED_AND_STALLED_IMAGE}
    New Page
    Go To    ${STALLED_PAGE}    wait_until=commit
    Go To    ${WELCOME_URL}
    Run Keyword And Expect Error    *Timeout*    Go Back

Go Forward Reports What The Stalled Page Was Still Loading
    [Documentation]
    ...    LOG 4.1:*    INFO    REGEXP: ${COMMITTED_AND_STALLED_IMAGE}
    New Page    ${WELCOME_URL}
    Go To    ${STALLED_PAGE}    wait_until=commit
    Go Back
    Run Keyword And Expect Error    *Timeout*    Go Forward

Wait For Navigation Reports What The Stalled Page Was Still Loading
    [Documentation]
    ...    LOG 3.1:*    INFO    REGEXP: ${COMMITTED_AND_STALLED_IMAGE}
    New Page
    Evaluate JavaScript    ${None}    window.location.href = '${STALLED_PAGE}'
    Run Keyword And Expect Error    *Timeout*    Wait For Navigation    ${STALLED_PAGE}

Wait For Load State Reports What The Stalled Page Was Still Loading
    [Documentation]
    ...    LOG 3.1:*    INFO    REGEXP: ${COMMITTED_AND_STALLED_IMAGE}
    New Page
    Go To    ${STALLED_PAGE}    wait_until=commit
    Run Keyword And Expect Error    *Timeout*    Wait For Load State    load

*** Keywords ***
Setup
    Set Browser Timeout    1s    scope=Suite
    ${original} =    Register Keyword To Run On Failure    ${None}
    VAR    ${original} =    ${original}    scope=SUITE
    VAR    ${COMMITTED_AND_STALLED_IMAGE} =
    ...    .*Navigation committed: yes.*readyState: ((loading|interactive).*load: never fired|unknown \\(probe failed: [^)]*\\)).*GET \\S+/api/stalled-image \\[image\\] open for \\d+ ms.*
    ...    scope=SUITE
    New Browser    headless=${HEADLESS}

Teardown
    Register Keyword To Run On Failure    ${original}
    Close Browser
