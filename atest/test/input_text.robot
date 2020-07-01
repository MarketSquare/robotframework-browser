*** Settings ***
Library		Browser

Test Setup	Open Browser	http://localhost:7272
Test Teardown	Close Browser

*** Test Cases ***
Test inputting with css selector
    Input Text		css=input#username_field	username	
    Get TextField Value		css=input#username_field	==	username	

Test Typing
    Input Text		css=input#username_field	username	type=True
    Get TextField Value		css=input#username_field	==	username	

Test inputting password
    Input Password	css=input#password_field	password
    Get TextField Value		css=input#password_field	==	password

