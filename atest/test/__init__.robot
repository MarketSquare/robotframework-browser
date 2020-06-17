*** Settings ***
Test Timeout	5 seconds

Library		Process
Suite Setup     Start Process	python  atest/demoapp/server.py
Suite Teardown	Terminate All Processes
