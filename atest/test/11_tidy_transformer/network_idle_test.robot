*** Settings ***
Resource        imports.resource

*** Test Cases ***
Tranform Wait Until Network Is Idle Keyword
    ${root} =   Normalize Path    ${CURDIR}/../../..
    ${entry} =    Set Variable    ${root}/Browser/entry.py
    ${python} =    Get Sys Executable
    ${process} =    Run Process     
    ...    ${python} ${entry} transform --wait-until-network-is-idle ${CURDIR}/network_idle_file.robot
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}     0
    ${file} =    Get File    ${CURDIR}/network_idle_file.robot
    ${lines} =    Split To Lines   ${file}
    Log    ${lines}
    Should Be Equal    ${lines}[5]        ${SPACE*4}\${not used} =${SPACE*2}New Context${SPACE*4}\# This is not changed
    Should Be Equal    ${lines}[6]        ${SPACE*4}Wait For Load State${SPACE*4}networkidle${SPACE*4}timeout=0.1s
    Should Be Equal    ${lines}[7]        ${SPACE*4}Wait For Load State${SPACE*4}networkidle
    Should Be Equal    ${lines}[8]        ${SPACE*4}Wait For Load State${SPACE*4}networkidle${SPACE*4}timeout=0.1s${SPACE*4}# Comment should be preserved
    Should Be Equal    ${lines}[9]        ${SPACE*4}Browser.Wait For Load State${SPACE*4}networkidle${SPACE*4}timeout=1.2s${SPACE*4}# Comment should be preserved
    Should Be Equal    ${lines}[10]        ${SPACE*4}\${not used} =${SPACE*7}New Context${SPACE*4}# This is not changed
    Length Should Be    ${lines}    11
