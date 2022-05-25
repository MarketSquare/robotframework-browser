*** Settings ***
Resource        imports.resource

Suite Setup     Open Browser To No Page
Test Setup      New Page    ${WAIT_URL}

Force Tags      slow

*** Test Cases ***
Wait For Elements State Attached
    Select Options By    \#dropdown    value    True    attached
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    attached    1.5 sec

Wait For Elements State Stable
    Select Options By    \#dropdown    value    True    attached
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    stable    1.5 sec

Wait For Elements State Attached With Strict On WaitForElementsState
    Run Keyword And Expect Error
    ...    *strict mode violation*//div*resolved to 2 elements*
    ...    Wait For Elements State    //div    attached    1.5 sec
    Set Strict Mode    False
    Wait For Elements State    //div    attached    1.5 sec
    [Teardown]    Set Strict Mode    True

Wait For Elements State Enabled With Strict On Wait_for_function
    Select Options By    \#dropdown    value    True    enabled
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    *strict mode violation*//div*resolved to 2 elements*
    ...    Wait For Elements State    //div    enabled    1.5 sec
    Set Strict Mode    False
    Wait For Elements State    //div    enabled    1.5 sec
    [Teardown]    Set Strict Mode    True

Wait For Elements State Detached
    Select Options By    \#dropdown    value    True    detached
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    detached    1.5 sec

Wait For Elements State Visible
    Select Options By    \#dropdown    value    True    visible
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    1.5 sec

Wait For Elements State Hidden
    Select Options By    \#dropdown    value    True    visible
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    hidden    1.5 sec

Wait For Elements State Hidden Not Strict
    Set Strict Mode    False
    Select Options By    \#dropdown    value    True    hidden
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    hidden    1.5 sec

Wait For Elements State From Attached To Hidden Not Strict
    Set Strict Mode    False
    Select Options By    \#dropdown    value    True    attached
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    attached    1.5 sec
    Select Options By    \#dropdown    value    True    detached
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    hidden    1.5 sec
    [Teardown]    Set Strict Mode    True

Wait For Elements State Enabled
    Select Options By    \#dropdown    value    True    enabled
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    enabled    1.5 sec

Wait For Elements State Disabled
    Select Options By    \#dropdown    value    True    disabled
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    disabled    1.5 sec

Wait For Elements State Editable
    Select Options By    \#dropdown    value    True    editable
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    editable    1.5 sec

Wait For Elements State Readonly
    Select Options By    \#dropdown    value    True    readonly
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    readonly    1.5 sec

Wait For Elements State Selected
    Select Options By    \#dropdown    value    True    selected
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#person >> option[value=victim]    selected    1.5 sec

Wait For Elements State Deselected
    Select Options By    \#dropdown    value    True    deselected
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#person >> option[value=victim]    deselected    1.5 sec

Wait For Elements State Focused
    Select Options By    \#dropdown    value    True    focused
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    focused    1.5 sec

Wait For Elements State Defocused
    Select Options By    \#dropdown    value    True    defocused
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    defocused    1.5 sec

Wait For Elements State Checked
    Select Options By    \#dropdown    value    True    checked
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    checked    1.5 sec

Wait For Elements State Unchecked
    Select Options By    \#dropdown    value    True    unchecked
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    unchecked    1.5 sec

Wait For Elements State Fails On Too Short Timeout
    Select Options By    \#dropdown    value    True    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    STARTS:TimeoutError: page.waitForFunction: Timeout 300ms exceeded.
    ...    Wait For Elements State    \#victim    unchecked    300ms

Wait For Elements State Fails On Too Short Global Timeout
    ${timeout} =    Set Browser Timeout    0.3 s
    Run Keyword And Expect Error    Custom Error #submit, hidden and 300 milliseconds
    ...    Wait For Elements State    \#submit    hidden    ${None}
    ...    Custom Error {selector}, {function} and {timeout}
    [Teardown]    Set Browser Timeout    ${timeout}

Wait For Elements State Fails On Too Short Timeout Custom Error With Formatting
    Select Options By    \#dropdown    value    True    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    Custom Error #victim, e => !e.checked and 300 milliseconds
    ...    Wait For Elements State    \#victim    unchecked    300ms
    ...    Custom Error {selector}, {function} and {timeout}

Wait For Elements State Fails On Too Short Timeout Custom Error
    Select Options By    \#dropdown    value    True    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    Custom Error
    ...    Wait For Elements State    \#victim    unchecked    300ms    Custom Error

Wait For Elements State Fails On Too Short Timeout Custom Error And Hidden
    Select Options By    \#dropdown    value    True    unchecked
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    Custom Error #victim, hidden and 300 milliseconds
    ...    Wait For Elements State    \#victim    hidden    300ms    Custom Error {selector}, {function} and {timeout}

Wait For Elements State To Hide With Promise
    Select Options By    \#dropdown    value    True    hidden    # Now it is visible
    ${promise} =    Promise To    Wait For Elements State    \#victim    hidden    3s
    Wait For Elements State    \#victim    visible    300ms
    Sleep    200 ms    reason=to check that the promise keeps beeing active
    ${start} =    Evaluate    time.time()
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    300ms
    Wait For    ${promise}
    Max Elapsed    ${start}    2.0

Wait For Elements State To Hide Fails With Promise
    Select Options By    \#dropdown    value    True    hidden    # Now it is visible
    ${promise} =    Promise To    Wait For Elements State    \#victim    hidden    200ms
    Run Keyword And Expect Error
    ...    *TimeoutError: locator.waitFor: Timeout 200ms exceeded.*
    ...    Wait for    ${promise}

Wait For Elements State To Hide With Promise And Wait For All Promises
    [Tags]    no-windows-support
    Select Options By    \#dropdown    value    True    hidden    # Now it is visible
    ${promise} =    Promise To    Wait For Elements State    \#victim    hidden    3s
    Wait For Elements State    \#victim    visible    300ms
    Sleep    200 ms    reason=to check that the promise keeps beeing active
    ${start} =    Evaluate    time.time()
    Click    \#submit    noWaitAfter=True
    Wait For Elements State    \#victim    visible    300ms
    Wait For All Promises
    Max Elapsed    ${start}    2.0

*** Keywords ***
Max Elapsed
    [Arguments]    ${start}    ${elapsed}
    ${end} =    Evaluate    time.time()
    Should Be True    ($end - $start) < ${elapsed}    ${{$end - $start}} < ${elapsed}
