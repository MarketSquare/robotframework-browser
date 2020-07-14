*** Settings ***
Test Timeout      ${DEFAULT_TEST_TIMEOUT}
Library           pabot.SharedLibrary    Process
Library           pabot.PabotLib
Resource          variables.resource
Suite Setup       Run Setup Only Once    Start Process    node    ${CURDIR}/../../node/dynamic-test-app/dist/server.js    ${DEFAULT_TEST_TIMEOUT}
Suite Teardown    Run Teardown Only Once    Terminate All Processes
