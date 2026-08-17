*** Settings ***
Documentation       Every test here starts a child `robot` run, which starts its own node process
...                 and browser. That does not fit the 30 second default test timeout.

Test Timeout        3 minutes
