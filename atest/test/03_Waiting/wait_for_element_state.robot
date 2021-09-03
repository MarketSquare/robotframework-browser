*** Settings ***
Resource        imports.resource

Suite Setup     Open Browser To No Page
Test Setup      New Page    ${WAIT_URL}

*** Test Cases ***
Wait For Elements State attached
    Select Options By    \#dropdown    value    attached
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    attached    1s

Wait For Elements State attached With Strict On WaitForElementsState
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 2 elements.*
    ...    Wait For Elements State    //div    attached    0.5s
    Wait For Elements State    //div    attached    0.5s    strict=False

Wait For Elements State attached With Strict On WaitForElementsState
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 2 elements.*
    ...    Wait For Elements State    //div    attached    0.5s
    Wait For Elements State    //div    attached    0.5s    strict=False

Wait For Elements State enabled With Strict On wait_for_function
    Select Options By    \#dropdown    value    enabled
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 2 elements.*
    ...    Wait For Elements State    //div    enabled    0.5s
    Wait For Elements State    //div    enabled    0.5s    strict=False

Wait For Elements State detached
    Select Options By    \#dropdown    value    detached
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    detached    1s

Wait For Elements State visible
    Select Options By    \#dropdown    value    visible
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    1s

Wait For Elements State enabled
    Select Options By    \#dropdown    value    enabled
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    enabled    1s

Wait For Elements State disabled
    Select Options By    \#dropdown    value    disabled
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    disabled    1s

Wait For Elements State editable
    Select Options By    \#dropdown    value    editable
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    editable    1s

Wait For Elements State readonly
    Select Options By    \#dropdown    value    readonly
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    readonly    1s

Wait For Elements State selected
    Select Options By    \#dropdown    value    selected
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#person >> option[value=victim]    selected    1s

Wait For Elements State deselected
    Select Options By    \#dropdown    value    deselected
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#person >> option[value=victim]    deselected    1s

Wait For Elements State focused
    Select Options By    \#dropdown    value    focused
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    focused    1s

Wait For Elements State defocused
    Select Options By    \#dropdown    value    defocused
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    defocused    1s

Wait For Elements State checked
    Select Options By    \#dropdown    value    checked
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    checked    1s

Wait For Elements State unchecked
    Select Options By    \#dropdown    value    unchecked
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    unchecked    1s

Wait For Elements State fails On Too Short Timeout
    Select Options By    \#dropdown    value    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword and Expect Error
    ...    STARTS:TimeoutError: page.waitForFunction: Timeout 300ms exceeded.
    ...    Wait For Elements State    \#victim    unchecked    300ms

Wait For Elements State fails On Too Short Global Timeout
    ${timeout} =    Set Browser Timeout    0.3 s
    Run Keyword and Expect Error    Custom Error #submit, ElementState.hidden and 300 milliseconds
    ...    Wait For Elements State    \#submit    hidden    ${None}
    ...    Custom Error {selector}, {function} and {timeout}
    [Teardown]    Set Browser Timeout    ${timeout}

Wait For Elements State Fails On Too Short Timeout Custom Error With Formatting
    Select Options By    \#dropdown    value    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword and Expect Error    Custom Error #victim, e => !e.checked and 300 milliseconds
    ...    Wait For Elements State    \#victim    unchecked    300ms
    ...    Custom Error {selector}, {function} and {timeout}

Wait For Elements State Fails On Too Short Timeout Custom Error
    Select Options By    \#dropdown    value    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword and Expect Error
    ...    Custom Error
    ...    Wait For Elements State    \#victim    unchecked    300ms    Custom Error

Wait For Elements State Fails On Too Short Timeout Custom Error And Hidden
    Select Options By    \#dropdown    value    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword and Expect Error
    ...    Custom Error #victim, ElementState.hidden and 300 milliseconds
    ...    Wait For Elements State    \#victim    hidden    300ms    Custom Error {selector}, {function} and {timeout}

Wait For Elements State to hide with Promise
    Select Options By    \#dropdown    value    hidden    # Now it is visible
    ${promise} =    Promise to    Wait For Elements State    \#victim    hidden    3s
    Wait For Elements State    \#victim    visible    300ms
    Sleep    200 ms    reason=to check that the promise keeps beeing active
    ${start} =    Evaluate    time.time()
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    300ms
    Wait for    ${promise}
    ${end} =    Evaluate    time.time()
    Should Be True    ($end - $start) < 1.0

Wait For Elements State to hide fails with Promise
    Select Options By    \#dropdown    value    hidden    # Now it is visible
    ${promise} =    Promise to    Wait For Elements State    \#victim    hidden    200ms
    Run Keyword and Expect Error    *Timeout 200ms exceeded.*waiting for selector "#victim" to be hidden*    Wait for
    ...    ${promise}

Wait For Elements State to hide with Promise and wait for all promises
    [Tags]    No-Windows-Support
    Select Options By    \#dropdown    value    hidden    # Now it is visible
    ${promise} =    Promise to    Wait For Elements State    \#victim    hidden    3s
    Wait For Elements State    \#victim    visible    300ms
    Sleep    200 ms    reason=to check that the promise keeps beeing active
    ${start} =    Evaluate    time.time()
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    300ms
    Wait For All Promises
    ${end} =    Evaluate    time.time()
    Should Be True    ($end - $start) < 0.9
