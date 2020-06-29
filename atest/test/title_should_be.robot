*** Settings ***
Library  Browser

Test Setup	Open Browser
Test Teardown	Close Browser

*** Test Cases ***
test server title
   GoTo		http://localhost:7272/
   Get Title	==	Login Page

about:blank title
    Get Title	==	${EMPTY}

