*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${WAIT_URL}

*** Test Cases ***
Wait For Elements State attached
    Select Options By    \#dropdown    value    attached
    Browser.Click     \#submit
    Wait For Elements State    \#victim    attached    1s

Wait For Elements State detached
    Select Options By    \#dropdown    value    detached
    Browser.Click     \#submit
    Wait For Elements State    \#victim    detached    1s

Wait For Elements State visible
    Select Options By    \#dropdown    value    visible
    Browser.Click     \#submit
    Wait For Elements State    \#victim    visible    1s

Wait For Elements State enabled
    Select Options By    \#dropdown    value    enabled
    Browser.Click     \#submit
    Wait For Elements State    \#victim    enabled    1s

Wait For Elements State disabled
    Select Options By    \#dropdown    value    disabled
    Browser.Click     \#submit
    Wait For Elements State    \#victim    disabled    1s

Wait For Elements State editable
    Select Options By    \#dropdown    value    editable
    Browser.Click     \#submit
    Wait For Elements State    \#victim    editable    1s

Wait For Elements State readonly
    Select Options By    \#dropdown    value    readonly
    Browser.Click     \#submit
    Wait For Elements State    \#victim    readonly    1s

Wait For Elements State selected
    Select Options By    \#dropdown    value    selected
    Browser.Click     \#submit
    Wait For Elements State    \#person >> option[value=victim]    selected    1s

Wait For Elements State deselected
    Select Options By    \#dropdown    value    deselected
    Browser.Click     \#submit
    Wait For Elements State    \#person >> option[value=victim]    deselected    1s

Wait For Elements State focused
    Select Options By    \#dropdown    value    focused
    Browser.Click     \#submit
    Wait For Elements State    \#victim    focused    1s

Wait For Elements State defocused
    Select Options By    \#dropdown    value    defocused
    Browser.Click     \#submit
    Wait For Elements State    \#victim    defocused    1s

Wait For Elements State checked
    Select Options By    \#dropdown    value    checked
    Browser.Click     \#submit
    Wait For Elements State    \#victim    checked    1s

Wait For Elements State unchecked
    Select Options By    \#dropdown    value    unchecked
    Browser.Click     \#submit
    Wait For Elements State    \#victim    unchecked    1s

Wait For Elements State fails on too short timeout
    Select Options By    \#dropdown    value    unchecked
    Browser.Click     \#submit
    Run Keyword and Expect Error    STARTS: page.waitForFunction: Timeout 1ms exceeded    Wait For Elements State    \#victim    unchecked    1ms

Wait For Elements State to hide with Promise
    ${promise}=    Promise to    Wait For Elements State    \#victim    hidden    3s
    Select Options By    \#dropdown    value    hidden
    Wait For Elements State    \#victim    visible    300ms
    Browser.Click     \#submit
    Wait for    ${promise}
    Run Keyword and Expect Error    Could not find element with selector `\#victim` within timeout.    Wait For Elements State    \#victim    visible    40ms

Wait For Elements State to hide fails with Promise
    ${promise}=    Promise to    Wait For Elements State    \#victim    hidden    3ms
    Run Keyword and Expect Error     Could not find element with selector `\#victim` within timeout.    Wait for    ${promise}

Wait For Elements State to hide with Promise and wait for all promises
    Promise to    Wait For Elements State    \#victim    hidden    3s
    Select Options By    \#dropdown    value    hidden
    Wait For Elements State    \#victim    visible    300ms
    Click    \#submit
    Wait for all promises
    Run Keyword and Expect Error    STARTS: page.waitForFunction: Timeout 40ms exceeded    Wait For Elements State    \#victim    checked    40ms
