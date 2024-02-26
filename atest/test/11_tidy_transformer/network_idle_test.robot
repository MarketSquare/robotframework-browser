*** Settings ***
Resource        imports.resource

*** Test Cases ***
Tranform Wait Until Network Is Idle Keyword
    ${entry} =    Set Variable    ${CURDIR}/../../../Browser/entry.py
    ${python} =    Get Sys Executable
    ${command} =    Split Command Line    ${python} ${entry} deprecated --wait_until_network_is_idle --path ${CURDIR}/network_idle_file.robot
    Log   ${python} ${entry} deprecated --wait_until_network_is_idle --path ${CURDIR}/network_idle_file.robot
    ${process} =    Run Process     ${command}    shell=True
    Should Be Equal As Integers    ${process.rc}     0
    Should Contain    ${process.stdout}     "Wait Until Network Is Idle transformed 4 times."
