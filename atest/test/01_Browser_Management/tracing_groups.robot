*** Settings ***
Resource    ../variables.resource
Library     Browser    auto_delete_passed_tracing=True    tracing_group_mode=Full
Library     OperatingSystem
Library     ArchiveLibrary
Library     tracing_groups.py
Library     Collections

*** Variables ***
${context_id} =                     ${EMPTY}
&{Initialize Context And Page} =    title=Initialize Context And Page    class=Tracing    method=tracingGroup
&{Browser.New Context} =            title=Browser.New Context    class=Tracing    method=tracingGroup
&{Keyword Without Browser} =        title=Keyword Without Browser    class=Tracing    method=tracingGroup
&{BuiltIn.Log} =                    title=BuiltIn.Log    class=Tracing    method=tracingGroup
&{Browser.New Page} =               title=Browser.New Page    class=Tracing    method=tracingGroup
&{browserContext.newPage} =         title=Default value    class=BrowserContext    method=newPage
&{page.goto} =                      title=Default value    class=Frame    method=goto
&{BuiltIn.Set Suite Variable} =     title=BuiltIn.Set Suite Variable    class=Tracing    method=tracingGroup
&{Browser.Close Context} =          title=Browser.Close Context    class=Tracing    method=tracingGroup
@{elements} =
...                                 ${Initialize Context And Page}
...                                 ${Browser.New Context}
...                                 ${Keyword Without Browser}
...                                 ${BuiltIn.Log}
...                                 ${Browser.New Page}
...                                 ${browserContext.newPage}
...                                 ${page.goto}
...                                 ${BuiltIn.Set Suite Variable}
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

*** Keywords ***
Keyword Without Browser
    [Arguments]    ${text}
    BuiltIn.Log    ${text}

Initialize Context And Page
    ${context_id} =    Browser.New Context    tracing=On
    Keyword Without Browser    this keyword has no browser in it
    Browser.New Page    ${FORM_URL}
    BuiltIn.Set Suite Variable    ${context_id}
