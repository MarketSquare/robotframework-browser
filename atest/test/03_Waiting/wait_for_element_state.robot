*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${WAIT_URL}

*** Test Cases ***
Wait For Elements State attached
    Select Options By    \#dropdown    value    attached
    Click With Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    attached    1s

Wait For Elements State detached
    Select Options By    \#dropdown    value    detached
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    detached    1s

Wait For Elements State visible
    Select Options By    \#dropdown    value    visible
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    1s

Wait For Elements State enabled
    Select Options By    \#dropdown    value    enabled
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    enabled    1s

Wait For Elements State disabled
    Select Options By    \#dropdown    value    disabled
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    disabled    1s

Wait For Elements State editable
    Select Options By    \#dropdown    value    editable
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    editable    1s

Wait For Elements State readonly
    Select Options By    \#dropdown    value    readonly
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    readonly    1s

Wait For Elements State selected
    Select Options By    \#dropdown    value    selected
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#person >> option[value=victim]    selected    1s

Wait For Elements State deselected
    Select Options By    \#dropdown    value    deselected
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#person >> option[value=victim]    deselected    1s

Wait For Elements State focused
    Select Options By    \#dropdown    value    focused
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    focused    1s

Wait For Elements State defocused
    Select Options By    \#dropdown    value    defocused
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    defocused    1s

Wait For Elements State checked
    Select Options By    \#dropdown    value    checked
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    checked    1s

Wait For Elements State unchecked
    Select Options By    \#dropdown    value    unchecked
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    unchecked    1s

Wait For Elements State fails on too short timeout
    Select Options By    \#dropdown    value    unchecked
    Click with Options    \#submit    noWaitAfter=True
    Run Keyword and Expect Error    STARTS:page.waitForFunction: Timeout 300ms exceeded.    Wait For Elements State    \#victim    unchecked    300ms

Wait For Elements State to hide with Promise
    Select Options By    \#dropdown    value    hidden      # Now it is visible
    ${promise}=    Promise to    Wait For Elements State    \#victim    hidden    3s
    Wait For Elements State    \#victim    visible    300ms
    Sleep    200 ms    reson=to check that the promise keeps beeing active
    ${start}=    Evaluate    time.time()
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    300ms
    Wait for    ${promise}
    ${end}=    Evaluate    time.time()
    Should Be True    ($end - $start) < 0.7

Wait For Elements State to hide fails with Promise
    Select Options By    \#dropdown    value    hidden      # Now it is visible
    ${promise}=    Promise to    Wait For Elements State    \#victim    hidden    200ms
    Run Keyword and Expect Error    Could not find element with selector `\#victim` within timeout.    Wait for    ${promise}

Wait For Elements State to hide with Promise and wait for all promises
    Select Options By    \#dropdown    value    hidden      # Now it is visible
    ${promise}=    Promise to    Wait For Elements State    \#victim    hidden    3s
    Wait For Elements State    \#victim    visible    300ms
    Sleep    200 ms    reson=to check that the promise keeps beeing active
    ${start}=    Evaluate    time.time()
    Click with Options    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    300ms
    Wait For All Promises
    ${end}=    Evaluate    time.time()
    Should Be True    ($end - $start) < 0.7