*** Settings ***
Test Timeout      30 seconds
Library           pabot.SharedLibrary    Process
Library           pabot.PabotLib
Suite Setup       Run Setup Only Once    Start Process    node    ${CURDIR}/../../dynamic-test-app/dist/server.js
Suite Teardown    Run Teardown Only Once    Terminate All Processes
