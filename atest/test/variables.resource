*** Variables ***
${SERVER_PORT}
${SERVER}         localhost:${SERVER_PORT}
${BROWSER}        chromium
${DELAY}          0
${HEADLESS}       TRUE
${VALID_USER}     demo
${VALID_PASSWORD}    mode
${ROOT_URL}       http://${SERVER}
${LOGIN_URL}      ${ROOT_URL}/dist/
${FORM_URL}       ${ROOT_URL}/prefilled_email_form.html
${DIALOGS_URL}    ${ROOT_URL}/dialogs.html
${FRAMES_URL}     ${ROOT_URL}/frames/iframes.html
${WELCOME_URL}    ${ROOT_URL}/welcome.html
${ERROR_URL}      ${ROOT_URL}/error.html
${DEFAULT_TEST_TIMEOUT}    30 seconds
${PLAYWRIGHT_TIMEOUT}      1 second
