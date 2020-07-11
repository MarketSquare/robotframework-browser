*** Settings ***
Test Timeout      ${DEFAULT TEST TIMEOUT}
Library           pabot.SharedLibrary    Process
Library           pabot.PabotLib
Resource          variables.resource
Suite Setup       Run Setup Only Once    Start Process    node    ${CURDIR}/../dynamic-test-app/dist/server.js    ${DEFAULT TEST TIMEOUT}
Suite Teardown    Run Teardown Only Once    Terminate All Processes
