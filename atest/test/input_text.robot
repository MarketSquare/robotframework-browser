*** Settings ***
Library		Playwright

Test Setup	Run Keywords	Open Browser	chrome	AND	GoTo	http://localhost:7272
Test Teardown	Close Browser

*** Test Cases ***
Test inputting with css selector
    Input Text		username	\#username_field	
    TextField Value Should Be	username	\#username_field
