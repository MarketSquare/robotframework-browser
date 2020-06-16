*** Settings ***
Library  Playwright

Test Setup	Open Browser	chrome
Test Teardown	Close Browser

*** Test Cases ***
Google.com title
   GoTo		http://localhost:7272/
   TitleShouldBe	Login Page
