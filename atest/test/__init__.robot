*** Settings ***
Test Timeout      30 seconds
Library           Process
Suite Setup       Start Process    python    atest/demoapp/server.py
Suite Teardown    Terminate All Processes
