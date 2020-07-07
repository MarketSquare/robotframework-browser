*** Variables ***
${SERVER}         localhost:7272
${BROWSER}        chromium
${DELAY}          0
${HEADLESS}         TRUE
${VALID USER}     demo
${VALID PASSWORD}    mode
${ROOT URL}      http://${SERVER}
${LOGIN URL}      ${ROOT URL}/dist/
${FORM URL}       ${ROOT URL}/prefilled_email_form.html
