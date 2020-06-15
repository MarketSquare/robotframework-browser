*** Settings ***
Library  Playwright

Test Setup	Open Browser	chrome
Test Teardown	Close Browser

*** Test Cases ***
Google.com title
   GoTo		https://www.google.com
   TitleShouldBe	Google
