*** Settings ***
Resource        imports.resource
Library         ../../library/certificate.py

Suite Setup     Setup

Test Teardown       Close Browser    ALL

*** Test Cases ***
Open Browser With Default Timeout
    New Browser    browser=${BROWSER}    headless=${HEADLESS}

*** Keywords ***
Setup
    Generate Ca Certificate    ${OUTPUT_DIR}/ca.crt    ${OUTPUT_DIR}/ca.key    "passphrase"
    Generate Server Certificate    "localhost"    ${OUTPUT_DIR}/server.crt    ${OUTPUT_DIR}/server.key    "passphrase"    ${OUTPUT_DIR}/ca.crt    ${OUTPUT_DIR}/ca.key    "passphrase"
    Generate Client Certificate    "client"    ${OUTPUT_DIR}/client.crt    ${OUTPUT_DIR}/client.key    "passphrase"    ${OUTPUT_DIR}/ca.crt    ${OUTPUT_DIR}/ca.key    "passphrase"
