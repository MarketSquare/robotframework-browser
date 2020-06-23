*** Settings ***
Library		Browser
Test Setup	Run Keywords 	Open Browser	chrome	AND	Go To	http://localhost:7272/checkbox_and_radio.html
Test Teardown	Close Browser

*** Test Cases ***
Checkbox Should Be Selected
    Checkbox Should Be	css=[name=can_send_email]	checked	


