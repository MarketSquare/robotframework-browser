*** Settings ***
Resource            imports.resource

Suite Setup         Create Browser Catalog State
Suite Teardown      Close Browser    ALL

*** Test Cases ***
Get Browser IDs
    Check Browser IDs    ALL    ${All}
    Check Browser IDs    ACTIVE    ${Active}

Get Context IDs
    Check Context IDs    Active    Active    ${Active Active}
    Check Context IDs    Active    All    ${Active All}
    Check Context IDs    All    Active    ${All Active}
    Check Context IDs    All    All    ${All All}

Get Page IDs
    Check Page IDs    Active    Active    Active    ${Active Active Active}
    Check Page IDs    Active    Active    All    ${Active Active All}
    Check Page IDs    Active    All    Active    ${Active All Active}
    Check Page IDs    Active    All    All    ${Active All All}
    Check Page IDs    All    Active    Active    ${All Active Active}
    Check Page IDs    All    Active    All    ${All Active All}
    Check Page IDs    All    All    Active    ${All All Active}
    Check Page IDs    All    All    All    ${All All All}

*** Keywords ***
Create Browser Catalog State
    Close Browser    ALL
    ${Browser1} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${Context1.1} =    New Context
    ${Page1.1.1} =    New Page
    ${ActivePage1.1} =    New Page
    ${ActiveContext1} =    New Context
    ${ActivePage1.2} =    New Page
    ${Page1.2.2} =    New Page
    Switch Page    ${ActivePage1.2}
    ${Browser2} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${ActiveContext2} =    New Context
    ${ActivePage2.1} =    New Page
    ${CurrentBrowser} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    ${Context3.1} =    New Context
    ${ActivePage3.1} =    New Page
    ${CurrentContext} =    New Context
    ${Page3.2.1} =    New Page
    ${CurrentPage} =    New Page
    # setting all variables
    VAR    @{Active} =    ${CurrentBrowser}
    VAR    @{All} =    ${Browser1}    ${Browser2}    ${CurrentBrowser}
    VAR    @{Active Active} =    ${CurrentContext}
    VAR    @{Active All} =    ${ActiveContext1}    ${ActiveContext2}    ${CurrentContext}
    VAR    @{All Active} =    ${Context3.1}    ${CurrentContext}
    VAR    @{All All} =    ${Context1.1}    ${Context3.1}    @{Active All}
    VAR    @{Active Active Active} =    ${CurrentPage}
    VAR    @{Active Active All} =    ${ActivePage1.2}    ${ActivePage2.1}    ${CurrentPage}
    VAR    @{Active All Active} =    ${ActivePage3.1}    ${CurrentPage}
    VAR    @{Active All All} =    ${ActivePage1.1}    ${ActivePage3.1}    @{Active Active All}
    VAR    @{All Active Active} =    ${Page3.2.1}    ${CurrentPage}
    VAR    @{All Active All} =
    ...    ${ActivePage1.2}
    ...    ${Page1.2.2}
    ...    ${ActivePage2.1}
    ...    ${Page3.2.1}
    ...    ${CurrentPage}
    VAR    @{All All Active} =    ${ActivePage3.1}    ${Page3.2.1}    ${CurrentPage}
    VAR    @{All All All} =    ${Page1.1.1}    ${Page1.2.2}    ${Page3.2.1}    @{Active All All}
    VAR    ${Active} =    ${Active}    scope=SUITE
    VAR    ${All} =    ${All}    scope=SUITE
    VAR    ${Active Active} =    ${Active Active}    scope=SUITE
    VAR    ${Active All} =    ${Active All}    scope=SUITE
    VAR    ${All Active} =    ${All Active}    scope=SUITE
    VAR    ${All All} =    ${All All}    scope=SUITE
    VAR    ${Active Active Active} =    ${Active Active Active}    scope=SUITE
    VAR    ${Active Active All} =    ${Active Active All}    scope=SUITE
    VAR    ${Active All Active} =    ${Active All Active}    scope=SUITE
    VAR    ${Active All All} =    ${Active All All}    scope=SUITE
    VAR    ${All Active Active} =    ${All Active Active}    scope=SUITE
    VAR    ${All Active All} =    ${All Active All}    scope=SUITE
    VAR    ${All All Active} =    ${All All Active}    scope=SUITE
    VAR    ${All All All} =    ${All All All}    scope=SUITE

Check Browser IDs
    [Arguments]    ${browser}    ${exp_ids}
    ${current} =    Get Browser Ids    ${browser}
    Run Keyword And Continue On Failure    Lists Should Be Equal    ${exp_ids}    ${current}    ignore_order=True

Check Context IDs
    [Arguments]    ${context}    ${browser}    ${exp_ids}
    ${current} =    Get Context Ids    ${context}    ${browser}
    Run Keyword And Continue On Failure    Lists Should Be Equal    ${exp_ids}    ${current}    ignore_order=True

Check Page IDs
    [Arguments]    ${page}    ${context}    ${browser}    ${exp_ids}
    ${current} =    Get Page Ids    ${page}    ${context}    ${browser}
    VAR    @{page_ids} =    @{EMPTY}
    FOR    ${page}    IN    @{exp_ids}
        Append To List    ${page_ids}    ${page}[page_id]
    END
    Run Keyword And Continue On Failure    Lists Should Be Equal    ${page_ids}    ${current}    ignore_order=True
