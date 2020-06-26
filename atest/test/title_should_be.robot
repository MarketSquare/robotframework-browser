*** Settings ***
Library  Browser

Test Setup	Open Browser
Test Teardown	Close Browser

*** Test Cases ***
test server title
   GoTo		http://localhost:7272/
   TitleShouldBe	Login Page

about:blank title
    TitleShouldBe	${EMPTY}

