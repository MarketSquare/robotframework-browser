*** Settings ***
Library  Browser  timeout=0.001
Test Setup	Open Browser
Test Teardown  Close Browser
Resource          resource.robot

*** Test Cases ***
Test GoTo With Short Default Timeout
    Run Keyword And Expect Error  *Timeout 1ms exceeded during page.goto*  GoTo   ${LOGIN_URL}
Test Overriding GoTo Timeout With Short
    Set Timeout  0.001
    Run Keyword And Expect Error  *Timeout 1ms exceeded during page.goto*  GoTo   ${LOGIN_URL}
Test Overriding GoTo Timeout With Long
    Set Timeout 10s
    GoTo  ${LOGIN_URL}
