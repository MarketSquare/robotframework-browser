*** Settings ***
Library  Browser  0.01
Test Setup	Open Browser
Test Teardown  Close Browser

*** Test Cases ***
Test Too Low Default Timeout
    Run Keyword And Expect Error  *Timeout 10ms exceeded during page.goto*  GoTo  http://localhost:7272
