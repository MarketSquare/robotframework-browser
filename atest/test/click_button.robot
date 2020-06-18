*** Settings ***
Library		Browser

Test Setup	Run Keywords	Open Browser	chrome	AND	GoTo	http://localhost:7272
Test Teardown	Close Browser

*** Test Cases ***
Test clicking submit
    Click Button	css=input#login_button
    Page Should Contain		Login failed. Invalid user name and/or password.
