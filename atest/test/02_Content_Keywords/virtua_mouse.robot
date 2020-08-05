*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click With coordinates
    ${xy}= 	Get BoundingBox 	\#login_button  x 	y
    Mouse Button    click   &{xy} 
    Get Text    text=Login failed. Invalid user name and/or password.
    Fail

Move In Circle
    Fail

