*** Settings ***
Resource    imports.resource

*** Test Cases ***
Create Default Translation File
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} translation ${OUTPUT_DIR}/translation.json
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    ${data} =    Verify Translation    ${OUTPUT_DIR}/translation.json
    Should Be True    ${data}[new_page]
