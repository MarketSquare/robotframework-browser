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
    ${re_prefix} =    Set Variable    \\d{4}-\\d\\d-\\d\\d\\s.{13}\\[INFO\\s{4}\\]\\s
    Should Match Regexp
    ...    ${lines}[0]
    ...    ${re_prefix}Found differences between translation and library, see below for details\.
    Should Match Regexp    ${lines}[1]    ${re_prefix}\\| Keyword name${SPACE * 23}\\| Reason${SPACE * 33}\\|
    Should Match Regexp
    ...    ${lines}[2]
    ...    ${re_prefix}\\| ---------------------------------- \\| -------------------------------------- \\|
    Should Match Regexp
    ...    ${lines}[3]
    ...    ${re_prefix}\\| cancel_download${SPACE * 20}\\| Documentation update needed${SPACE * 12}\\|
    Should Match Regexp
    ...    ${lines}[4]
    ...    ${re_prefix}\\| close_page${SPACE * 25}\\| Keyword is missing translation${SPACE * 9}\\|
    Should Match Regexp
    ...    ${lines}[5]
    ...    ${re_prefix}\\| grant_permissions${SPACE * 18}\\| Keyword is missing translation${SPACE * 9}\\|
    Should Match Regexp
    ...    ${lines}[6]
    ...    ${re_prefix}\\| focus${SPACE * 30}\\| Documentation update needed${SPACE * 12}\\|
    Should Match Regexp
    ...    ${lines}[7]
    ...    ${re_prefix}\\| get_style${SPACE * 26}\\| Keyword tranlsaton is missing checksum \\|
    Should Match Regexp
    ...    ${lines}[8]
    ...    ${re_prefix}\\| __intro__${SPACE * 26}\\| Documentation update needed${SPACE * 12}\\|
    Should Match Regexp
    ...    ${lines}[9]
    ...    ${re_prefix}\\| not_there${SPACE * 26}\\| Keyword not found from library${SPACE * 9}\\|
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
    ${re_prefix} =    Set Variable    \\d{4}-\\d\\d-\\d\\d\\s.{13}\\[INFO\\s{4}\\]\\s
    Should Match Regexp    ${process.stdout}    ${re_prefix}Translation is valid, no updated needed.
    [Teardown]    Remove Files    ${OUTPUT_DIR}/translation_new.json
