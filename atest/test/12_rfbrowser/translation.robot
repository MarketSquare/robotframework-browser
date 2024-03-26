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
