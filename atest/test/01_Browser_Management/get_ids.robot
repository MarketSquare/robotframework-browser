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
    ${Browser1} =    New Browser
    ${Context1.1} =    New Context
    ${Page1.1.1} =    New Page
    ${ActivePage1.1} =    New Page
    ${ActiveContext1} =    New Context
    ${ActivePage1.2} =    New Page
    ${Page1.2.2} =    New Page
    Switch Page    ${ActivePage1.2}
    ${Browser2} =    New Browser
    ${ActiveContext2} =    New Context
    ${ActivePage2.1} =    New Page
    ${CurrentBrowser} =    New Browser
    ${Context3.1} =    New Context
    ${ActivePage3.1} =    New Page
    ${CurrentContext} =    New Context
    ${Page3.2.1} =    New Page
    ${CurrentPage} =    New Page
    # setting all variables
    ${Active} =    Create List
    ...    ${CurrentBrowser}
    ${All} =    Create List
    ...    ${Browser1}
    ...    ${Browser2}
    ...    ${CurrentBrowser}
    ${Active Active} =    Create List
    ...    ${CurrentContext}
    ${Active All} =    Create List
    ...    ${ActiveContext1}
    ...    ${ActiveContext2}
    ...    ${CurrentContext}
    ${All Active} =    Create List
    ...    ${Context3.1}
    ...    ${CurrentContext}
    ${All All} =    Create List
    ...    ${Context1.1}
    ...    ${Context3.1}
    ...    @{Active All}
    ${Active Active Active} =    Create List
    ...    ${CurrentPage}
    ${Active Active All} =    Create List
    ...    ${ActivePage1.2}
    ...    ${ActivePage2.1}
    ...    ${CurrentPage}
    ${Active All Active} =    Create List
    ...    ${ActivePage3.1}
    ...    ${CurrentPage}
    ${Active All All} =    Create List
    ...    ${ActivePage1.1}
    ...    ${ActivePage3.1}
    ...    @{Active Active All}
    ${All Active Active} =    Create List
    ...    ${Page3.2.1}
    ...    ${CurrentPage}
    ${All Active All} =    Create List
    ...    ${ActivePage1.2}
    ...    ${Page1.2.2}
    ...    ${ActivePage2.1}
    ...    ${Page3.2.1}
    ...    ${CurrentPage}
    ${All All Active} =    Create List
    ...    ${ActivePage3.1}
    ...    ${Page3.2.1}
    ...    ${CurrentPage}
    ${All All All} =    Create List
    ...    ${Page1.1.1}
    ...    ${Page1.2.2}
    ...    ${Page3.2.1}
    ...    @{Active All All}
    Set Suite Variable    ${Active}
    Set Suite Variable    ${All}
    Set Suite Variable    ${Active Active}
    Set Suite Variable    ${Active All}
    Set Suite Variable    ${All Active}
    Set Suite Variable    ${All All}
    Set Suite Variable    ${Active Active Active}
    Set Suite Variable    ${Active Active All}
    Set Suite Variable    ${Active All Active}
    Set Suite Variable    ${Active All All}
    Set Suite Variable    ${All Active Active}
    Set Suite Variable    ${All Active All}
    Set Suite Variable    ${All All Active}
    Set Suite Variable    ${All All All}

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
    Run Keyword And Continue On Failure    Lists Should Be Equal    ${exp_ids}    ${current}    ignore_order=True
