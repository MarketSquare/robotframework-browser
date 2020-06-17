*** Settings ***
Library		Playwright

Test Setup	Run Keywords	Open Browser	chrome	AND	GoTo	http://localhost:7272
Test Teardown	Close Browser

*** Test Cases ***
Test inputting with css selector
    Input Text		css=input#username_field	username	
    TextField Value Should Be	css=input#username_field	username	
