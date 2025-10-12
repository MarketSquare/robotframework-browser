*** Settings ***
Library             pabot.SharedLibrary    Process
Library             pabot.PabotLib
Library             ../library/common.py
Resource            variables.resource
Resource            keywords.resource

Suite Setup         Start Test Application
Suite Teardown      Suite Teardown
Test Timeout        ${DEFAULT_TEST_TIMEOUT}

*** Keywords ***
Start Test Application
    ${port} =    Start Test Server
    Set Global Variable    $SERVER_PORT    ${port}
    ${python_version} =    Is Python 314
    Set Global Variable    $PYTHON_314    ${python_version}

Suite Teardown
    Stop Test Server    ${SERVER_PORT}
    Suite Cleanup
