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
    [Teardown]    Remove File    ${OUTPUT_DIR}/translation.json

Create Translation File With Python Plugin
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} translation ${OUTPUT_DIR}/translation.json --plugings ${CURDIR}/SomePlugin.py
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    ${data} =    Verify Translation    ${OUTPUT_DIR}/translation.json
    Should Be True    ${data}[this_is_plugin_keyword]
    ${inro} =    Set Variable    ${data}[__intro__]
    Should Start With    ${inro}[doc]    Browser library${SPACE}
    Should Be Equal    ${inro}[name]    __intro__
    ${init} =    Set Variable    ${data}[__init__]
    Should Start With    ${init}[doc]    Browser library${SPACE}
    Should Be Equal    ${init}[name]    __init__
    [Teardown]    Remove File    ${OUTPUT_DIR}/translation.json

Create Translation File With JS Plugin
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} translation ${OUTPUT_DIR}/translation.json --plugings ${CURDIR}/SomePlugin.py --jsextension ${CURDIR}/jsplugin.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    ${data} =    Verify Translation    ${OUTPUT_DIR}/translation.json
    Should Be True    ${data}[this_is_plugin_keyword]
    Should Be True    ${data}[mouseWheelAsPlugin]
    [Teardown]    Remove File    ${OUTPUT_DIR}/translation.json

Compare Translation Files
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} translation ${OUTPUT_DIR}/translation_new.json
    ...    shell=True
    Should Be Equal As Integers    ${process.rc}    0
    Modify Sha256    ${OUTPUT_DIR}/translation_new.json    cancel_download    focus    __intro__
    Remoe Kw    ${OUTPUT_DIR}/translation_new.json    close_page    grant_permissions
    Add Kw    ${OUTPUT_DIR}/translation_new.json    not_there
    Remove Sha256    ${OUTPUT_DIR}/translation_new.json    get_style
    ${process} =    Run Process
    ...    ${entry_cmd} translation --compare ${OUTPUT_DIR}/translation_new.json
    ...    shell=True
    Log    ${process.stderr}
    Log    ${process.stdout}
    Should Be Equal As Integers    ${process.rc}    0
    ${lines} =    Split To Lines    ${process.stdout}
    Log    ${lines}
    Length Should Be    ${lines}    10
    Should Match Regexp
    ...    ${lines}[0]
    ...    Found differences between translation and library, see below for details\.
    Should Match Regexp    ${lines}[1]    \\| Keyword name${SPACE * 23}\\| Reason${SPACE * 33}\\|
    Should Match Regexp
    ...    ${lines}[2]
    ...    \\| ---------------------------------- \\| -------------------------------------- \\|
    Should Match Regexp
    ...    ${lines}[3]
    ...    \\| cancel_download${SPACE * 20}\\| Documentation update needed${SPACE * 12}\\|
    Should Match Regexp
    ...    ${lines}[4]
    ...    \\| close_page${SPACE * 25}\\| Keyword is missing translation${SPACE * 9}\\|
    Should Match Regexp
    ...    ${lines}[5]
    ...    \\| grant_permissions${SPACE * 18}\\| Keyword is missing translation${SPACE * 9}\\|
    Should Match Regexp
    ...    ${lines}[6]
    ...    \\| focus${SPACE * 30}\\| Documentation update needed${SPACE * 12}\\|
    Should Match Regexp
    ...    ${lines}[7]
    ...    \\| get_style${SPACE * 26}\\| Keyword tranlsaton is missing checksum \\|
    Should Match Regexp
    ...    ${lines}[8]
    ...    \\| __intro__${SPACE * 26}\\| Documentation update needed${SPACE * 12}\\|
    Should Match Regexp
    ...    ${lines}[9]
    ...    \\| not_there${SPACE * 26}\\| Keyword not found from library${SPACE * 9}\\|
    [Teardown]    Remove Files    ${OUTPUT_DIR}/translation_new.json

Translation Files Does Not Require Updates
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} translation ${OUTPUT_DIR}/translation_new.json
    ...    shell=True
    ${process} =    Run Process
    ...    ${entry_cmd} translation --compare ${OUTPUT_DIR}/translation_new.json
    ...    shell=True
    Log    ${process.stderr}
    Log    ${process.stdout}
    Should Be Equal As Integers    ${process.rc}    0
    Should Match Regexp    ${process.stdout}    Translation is valid, no updated needed.
    [Teardown]    Remove Files    ${OUTPUT_DIR}/translation_new.json
