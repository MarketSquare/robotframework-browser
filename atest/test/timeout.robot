*** Settings ***
Library  Browser  0.01
Test Setup	Open Browser
Test Teardown  Close Browser
Resource          resource.robot

*** Test Cases ***
Test GoTo Timeout
    Run Keyword And Expect Error  *Timeout 10ms exceeded during page.goto*  GoTo   ${LOGIN_URL}
    GoTo  ${LOGIN_URL}	10.0
Test Get Title Timeout
    GoTo  ${LOGIN_URL}  10.0
    Run Keyword And Expect Error  *Timeout 10ms exceeded during asdasd*  Get Title
