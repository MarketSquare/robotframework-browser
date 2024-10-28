*** Settings ***
Resource            imports.resource
Library             ../../library/certificate.py

Suite Setup         Setup
Suite Teardown      Suite Teardown
Test Teardown       Close Browser    ALL

*** Test Cases ***
Open Browser With Client Certificate
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    New Context
    ...    ignoreHTTPSErrors=True
    ...    clientCertificates=[{'origin': 'https://localhost:${https_port}', 'certPath': '${OUTPUT_DIR}/client.crt', 'keyPath': '${OUTPUT_DIR}/client.key'}]
    New Page    https://localhost:${https_port}/

Open Browser Without Client Certificate
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    New Context    ignoreHTTPSErrors=True
    Run Keyword And Expect Error
    ...    Error: page.goto: net::ERR_SOCKET_NOT_CONNECTED*    New Page    https://localhost:${https_port}/

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
