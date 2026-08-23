*** Settings ***
Library           pabot.SharedLibrary    Process
Library           pabot.PabotLib
Library           ../library/common.py
Resource          variables.resource
Resource          keywords.resource

Suite Setup       Start Test Application
Suite Teardown    Suite Teardown
Test Timeout      ${DEFAULT_TEST_TIMEOUT}

*** Keywords ***
Start Test Application
    ${port} =    Start Test Server
    VAR    ${SERVER_PORT} =    ${port}    scope=GLOBAL
    VAR    ${SERVER} =    localhost:${SERVER_PORT}    scope=GLOBAL
    ${python_version} =    Is Python 314
    VAR    ${PYTHON_314} =    ${python_version}    scope=GLOBAL
    ${rf_version} =    Get Robot Version
    Set Suite Metadata    Robot Framework Version    ${rf_version}
    Log To Console    RF Version: ${rf_version}
    ${python_version} =    Get Python Version
    Set Suite Metadata    Python Version    ${python_version}
    # Which NodeJS and which machine ran this. output.xml is the only thing that
    # outlives a CI run, so anything worth slicing failures by has to be in it.
    ${node_version} =    Get Node Version
    Set Suite Metadata    Node Version    ${node_version}
    Log To Console    NodeJS Version: ${node_version}
    ${os_release} =    Get Os Release
    Set Suite Metadata    OS    ${os_release}

Suite Teardown
    Stop Test Server    ${SERVER_PORT}
    Suite Cleanup
