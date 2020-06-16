*** Settings ***
Test Timeout	5 seconds

Library		Process
Suite Setup	Start Process	atest/demoapp/server.py
Suite Teardown	Terminate All Processes
