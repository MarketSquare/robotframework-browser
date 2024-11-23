*** Settings ***
Resource            imports.resource
Library             ../../library/certificate.py

Suite Setup         Setup
Suite Teardown      Suite Teardown
Test Teardown       Close Browser    ALL

*** Test Cases ***
Open Browser With Client Certificate
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    ${cert} =    Create Dictionary
    ...    origin=https://localhost:${https_port}
    ...    certPath=${OUTPUT_DIR}/client.crt
    ...    keyPath=${OUTPUT_DIR}/client.key
    ${certs} =    Create List    ${cert}
    New Context
    ...    ignoreHTTPSErrors=True
    ...    clientCertificates=${certs}
    New Page    https://localhost:${https_port}/

Open Browser Without Client Certificate
    [Tags]    no-windows-support
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    New Context    ignoreHTTPSErrors=True
    ${error} =    Run Keyword And Expect Error
    ...    *    New Page    https://localhost:${https_port}/
    Should Match Regexp
    ...    ${error}
    ...    Error: page\.goto: net::(?:ERR_BAD_SSL_CLIENT_AUTH_CERT|ERR_SOCKET_NOT_CONNECTED).+

*** Keywords ***
Setup
    Generate Ca Certificate    ${OUTPUT_DIR}/ca.crt    ${OUTPUT_DIR}/ca.key
    Generate Server Certificate
    ...    "localhost"
    ...    ${OUTPUT_DIR}/server.crt
    ...    ${OUTPUT_DIR}/server.key
    ...    ${OUTPUT_DIR}/ca.crt
    ...    ${OUTPUT_DIR}/ca.key
    Generate Client Certificate
    ...    "client"
    ...    ${OUTPUT_DIR}/client.crt
    ...    ${OUTPUT_DIR}/client.key
    ...    ${OUTPUT_DIR}/ca.crt
    ...    ${OUTPUT_DIR}/ca.key
    ${port} =    Start Test Https Server
    ...    ${OUTPUT_DIR}/server.crt
    ...    ${OUTPUT_DIR}/server.key
    ...    ${OUTPUT_DIR}/ca.crt
    ...    True
    Set Global Variable    ${https_port}    ${port}

Suite Teardown
    Stop Test Server    ${https_port}
    Suite Cleanup
