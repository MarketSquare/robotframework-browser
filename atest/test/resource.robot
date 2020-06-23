*** Settings ***
Library		Browser

*** Variables ***
${SERVER}         localhost:7272
${BROWSER}        chrome 
# TODO: make the delay and headed do stuff in open browser
${DELAY}          0
${HEADED}	False
${VALID USER}     demo
${VALID PASSWORD}    mode
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/welcome.html
${ERROR URL}      http://${SERVER}/error.html
${FORM_URL}	http://${SERVER}/prefilled_email_form.html

*** Keywords ***
Open Browser To Login Page
    Open Browser	${BROWSER}
    Go To	${LOGIN URL}
    Title Should Be	Login Page	

Open Form 
    Open Browser	${BROWSER}
    Go To	${FORM_URL}
    Title Should Be	prefilled_email_form.html

