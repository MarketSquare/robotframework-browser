*** Settings ***
Resource    ../variables.resource
Library     Browser    auto_delete_passed_tracing=True    tracing_group_mode=Full
Library     OperatingSystem
Library     ArchiveLibrary
Library     ../../library/tracing_groups.py
Library     Collections

*** Variables ***
${context_id} =                     ${EMPTY}
${SECRET_VALUE} =                   xyzzy-do-not-disclose
&{Initialize Context And Page} =    title=Initialize Context And Page    class=Tracing    method=tracingGroup
&{Browser.New Context} =            title=Browser.New Context    class=Tracing    method=tracingGroup
&{Keyword Without Browser} =        title=Keyword Without Browser    class=Tracing    method=tracingGroup
&{BuiltIn.Log} =                    title=BuiltIn.Log    class=Tracing    method=tracingGroup
&{Browser.New Page} =               title=Browser.New Page    class=Tracing    method=tracingGroup
&{browserContext.newPage} =         title=Default value    class=BrowserContext    method=newPage
&{page.goto} =                      title=Default value    class=Frame    method=goto
&{VAR_SUITE} =                      title=VAR    class=Tracing    method=tracingGroup
&{Browser.Close Context} =          title=Browser.Close Context    class=Tracing    method=tracingGroup
@{elements} =
...                                 ${Initialize Context And Page}
...                                 ${Browser.New Context}
...                                 ${Keyword Without Browser}
...                                 ${BuiltIn.Log}
...                                 ${Browser.New Page}
...                                 ${browserContext.newPage}
...                                 ${page.goto}
...                                 ${VAR_SUITE}
...                                 ${Browser.Close Context}

*** Test Cases ***
Trace File Will Stay
    Log    This is not in Trace
    Initialize Context And Page
    Browser.Close Context
    File Should Exist    ${OUTPUT_DIR}/browser/traces/trace_${context_id}.zip

Manual Context Close Shall Not Remove Trace File
    File Should Exist    ${OUTPUT_DIR}/browser/traces/trace_${context_id}.zip
    Extract Zip File
    ...    zip_file=${OUTPUT_DIR}/browser/traces/trace_${context_id}.zip
    ...    dest=${OUTPUT_DIR}/browser/traces/trace_${context_id}/
    ${trace} =    Get Trace Lines    ${OUTPUT_DIR}/browser/traces/trace_${context_id}/trace.trace
    FOR    ${trace_entry}    ${expected}    IN ZIP    ${trace}    ${elements}    mode=SHORTEST
        ${title} =    Get From Dictionary    ${trace_entry}    title    Default value
        Should Start With    ${title}    ${expected.title}
        Should Be Equal    ${trace_entry}[class]    ${expected}[class]
        Should Be Equal    ${trace_entry}[method]    ${expected.method}
        ${stack} =    Evaluate    $trace_entry.get('stack')
        IF    $stack is not None
            ${line} =    Get File Line    &{stack}[0]
            Should Contain    ${line}    ${{$expected['title'].replace(' ', ' ')}}
        END
    END

Trace File Will Be Deleted
    [Documentation]    Trace file will never be created.
    Initialize Context And Page

Automatic Context Close Shall Remove Trace File
    File Should Not Exist    ${OUTPUT_DIR}/browser/traces/trace_${context_id}.zip

Keywords In Branches That Did Not Run Get No Trace Group
    New Context
    New Page    ${FORM_URL}
    Start Tracing    scope=Test
    IF    False
        Log    if branch did not run
    ELSE
        Log    else branch ran
    END
    TRY
        Log    try branch ran
    EXCEPT    *
        Log    except branch did not run
    END
    ${trace} =    Stop Tracing    path=not-run-branches.zip
    Extract Zip File    zip_file=${trace}    dest=${OUTPUT_DIR}/not-run-branches/
    ${groups} =    Get Trace Group Titles    ${OUTPUT_DIR}/not-run-branches/trace.trace
    Should Contain Match    ${groups}    BuiltIn.Log*else branch ran
    Should Contain Match    ${groups}    BuiltIn.Log*try branch ran
    Should Not Contain Match    ${groups}    *did not run*
    Should Not Contain Match    ${groups}    IF*False
    Should Not Contain Match    ${groups}    EXCEPT*
    [Teardown]    Close Context

Groups After A Loop Or Branch That Did Not Run Keep Their Parent
    New Context
    New Page    ${FORM_URL}
    Start Tracing    scope=Test
    FOR    ${item}    IN    @{EMPTY}
        Log    ${item}
    END
    Log    after empty loop
    Catch An Invalid Condition And Log
    ${trace} =    Stop Tracing    path=loop-and-branch-not-run.zip
    Extract Zip File    zip_file=${trace}    dest=${OUTPUT_DIR}/loop-and-branch-not-run/
    ${parent} =    Get Trace Group Parent Title
    ...    ${OUTPUT_DIR}/loop-and-branch-not-run/trace.trace    BuiltIn.Log*after empty loop
    Should Be Equal    ${parent}    ${None}
    ${parent} =    Get Trace Group Parent Title
    ...    ${OUTPUT_DIR}/loop-and-branch-not-run/trace.trace    BuiltIn.Log*after invalid condition
    Should Be Equal    ${parent}    Catch An Invalid Condition And Log
    [Teardown]    Close Context

Trace Group Names Show Argument Values
    New Context
    New Page    about:blank
    Start Tracing    scope=Test
    Write And Read Paragraph    first
    Write And Read Paragraph    second
    ${trace} =    Stop Tracing    path=argument-values.zip
    Extract Zip File    zip_file=${trace}    dest=${OUTPUT_DIR}/argument-values/
    ${groups} =    Get Trace Group Titles    ${OUTPUT_DIR}/argument-values/trace.trace
    Should Contain Match    ${groups}    Browser.Get Text*id=a*==*first
    Should Contain Match    ${groups}    Browser.Get Text*id=a*==*second
    Should Contain Match    ${groups}    Browser.Evaluate JavaScript*None*>second</p>'
    Should Not Contain Match    ${groups}    *\${tag}*
    [Teardown]    Close Context

Trace Group Names Mask Secret Arguments
    New Context
    New Page    ${FORM_URL}
    Start Tracing    scope=Test
    TRY
        Fill Secret    css=input#username    ${SECRET_VALUE}
    EXCEPT    ValueError: Direct assignment of values or variables as 'secret' is not allowed.*    type=glob
        Log    secret was rejected
    END
    ${trace} =    Stop Tracing    path=masked-secret.zip
    Extract Zip File    zip_file=${trace}    dest=${OUTPUT_DIR}/masked-secret/
    ${groups} =    Get Trace Group Titles    ${OUTPUT_DIR}/masked-secret/trace.trace
    Should Contain Match    ${groups}    Browser.Fill Secret*css=input#username*[*][*][*]
    Should Not Contain Match    ${groups}    *xyzzy*
    [Teardown]    Close Context

Trace Group Names Cut Long Argument Values
    New Context
    New Page    about:blank
    Start Tracing    scope=Test
    VAR    ${long}    ${{'x' * 300}}
    Log    ${long}
    ${trace} =    Stop Tracing    path=long-value.zip
    Extract Zip File    zip_file=${trace}    dest=${OUTPUT_DIR}/long-value/
    ${groups} =    Get Trace Group Titles    ${OUTPUT_DIR}/long-value/trace.trace
    Should Contain Match    ${groups}    BuiltIn.Log*${{'x' * 200}}...
    Should Not Contain Match    ${groups}    *${{'x' * 201}}*
    [Teardown]    Close Context

Trace Group Names Do Not Evaluate Arguments Again
    New Context
    New Page    about:blank
    Start Tracing    scope=Test
    VAR    @{calls} =    first    second
    Log    ${{ $calls.append('inline') }}
    Log    ${calls.pop(0)}
    ${trace} =    Stop Tracing    path=evaluated-once.zip
    Should Be Equal    ${calls}    ${{ ['second', 'inline'] }}
    Extract Zip File    zip_file=${trace}    dest=${OUTPUT_DIR}/evaluated-once/
    ${groups} =    Get Trace Group Titles    ${OUTPUT_DIR}/evaluated-once/trace.trace
    Should Contain Match    ${groups}    BuiltIn.Log*\${{ $calls.append('inline') }}
    Should Contain Match    ${groups}    BuiltIn.Log*\${calls.pop(0)}
    [Teardown]    Close Context

*** Keywords ***
Keyword Without Browser
    [Arguments]    ${text}
    BuiltIn.Log    ${text}

Initialize Context And Page
    ${context_id} =    Browser.New Context    tracing=On
    Keyword Without Browser    this keyword has no browser in it
    Browser.New Page    ${FORM_URL}
    VAR    ${context_id} =    ${context_id}    scope=SUITE

Catch An Invalid Condition And Log
    Run Keyword And Expect Error    Invalid IF condition*    Use An Invalid Condition
    Log    after invalid condition

Use An Invalid Condition
    IF    $undefined > 1    Log    invalid condition did not run

Write And Read Paragraph
    [Arguments]    ${tag}
    Evaluate JavaScript    ${None}    document.body.innerHTML='<p id="a">${tag}</p>'
    Get Text    id=a    ==    ${tag}
