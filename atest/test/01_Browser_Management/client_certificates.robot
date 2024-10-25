*** Settings ***
Resource            imports.resource
Library             ../../library/certificate.py

Suite Setup         Setup
Suite Teardown      Suite Teardown

Test Teardown       Close Browser    ALL

*** Test Cases ***
Open Browser With Default Timeout
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    New Context    ignoreHTTPSErrors=True  clientCertificates=[{'origin': '${HTTPS_SERVER_URL}', 'certPath': '${OUTPUT_DIR}/client.crt', 'keyPath': '${OUTPUT_DIR}/client.key', 'passphrase': 'passphrase'}]
    New Page       ${HTTPS_ROOT_URL}


*** Keywords ***
Setup
    Generate Ca Certificate    ${OUTPUT_DIR}/ca.crt    ${OUTPUT_DIR}/ca.key    "passphrase"
    Generate Server Certificate    "localhost"    ${OUTPUT_DIR}/server.crt    ${OUTPUT_DIR}/server.key    "passphrase"    ${OUTPUT_DIR}/ca.crt    ${OUTPUT_DIR}/ca.key    "passphrase"
    Generate Client Certificate    "client"    ${OUTPUT_DIR}/client.crt    ${OUTPUT_DIR}/client.key    "passphrase"    ${OUTPUT_DIR}/ca.crt    ${OUTPUT_DIR}/ca.key    "passphrase"
    ${port} =    Start Test Https Server    ${OUTPUT_DIR}/server.crt    ${OUTPUT_DIR}/server.key    "passphrase"    ${OUTPUT_DIR}/ca.crt    True
    Set Global Variable    $HTTPS_SERVER_PORT    ${port}

Suite Teardown
    Stop Test Server    ${HTTPS_SERVER_PORT}
    Suite Cleanup
