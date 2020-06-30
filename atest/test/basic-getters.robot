*** Settings ***
Library  Browser

Test Setup	Open Browser	http://localhost:7272
Test Teardown	Close Browser

*** Test Cases ***
Get Text Simple
    Get Text  h1   ==  Login Page

Get Attribute
    Get Attribute  h1  innerText  ==  Login Page

