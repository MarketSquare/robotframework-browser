*** Settings ***
Library  Browser  timeout=1ms
Test Setup	Open Browser
Test Teardown  Close Browser
Resource          resource.robot

*** Test Cases ***
Test GoTo With Short Default Timeout
    Run Keyword And Expect Error  *Timeout 1ms exceeded during page.goto*  GoTo   ${LOGIN_URL}
Test Overriding With Short
    Set Timeout  1ms	
    Run Keyword And Expect Error  *Timeout 1ms exceeded during page.goto*  GoTo   ${LOGIN_URL}
Test Overriding With Long
    Set Timeout  10s
    GoTo  ${LOGIN_URL}
