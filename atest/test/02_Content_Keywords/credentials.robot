*** Settings ***
Resource            imports.resource
Library             credentials.py

Suite Setup         New Browser    ${BROWSER}    headless=${HEADLESS}
Test Setup          Credential Test Setup
Test Teardown       Credential Test Teardown

*** Test Cases ***
Add Valid Credential With Secret
    ${credentials} =    Get Credentials
    Create Credential
    ...    rpId=localhost
    ...    id_=${credentials["id"]}
    ...    privateKey=${credentials["privateKey"]}
    ...    publicKey=${credentials["publicKey"]}
    ...    userHandle=${credentials["userHandle"]}
    New Page    ${CREDENTIAL_URL}
    Click    id=login
    Get Text    id=status    ==    Success

Add Valid Credential With Variable
    ${credentials} =    Get Credentials
    VAR    ${privateKey} =    ${credentials["privateKey"]}
    VAR    ${publicKey} =    ${credentials["publicKey"]}
    Create Credential
    ...    rpId=localhost
    ...    id_=${credentials["id"]}
    ...    privateKey=$privateKey
    ...    publicKey=$publicKey
    ...    userHandle=${credentials["userHandle"]}
    New Page    ${CREDENTIAL_URL}
    Click    id=login
    Get Text    id=status    ==    Success

Add Credential With Invalid rpId
    ${credentials} =    Get Credentials
    Create Credential
    ...    rpId=invalid
    ...    id_=${credentials["id"]}
    ...    privateKey=${credentials["privateKey"]}
    ...    publicKey=${credentials["publicKey"]}
    ...    userHandle=${credentials["userHandle"]}
    Create Credential    # To ensure that same credential can be created two times
    ...    rpId=invalid
    ...    id_=${credentials["id"]}
    ...    privateKey=${credentials["privateKey"]}
    ...    publicKey=${credentials["publicKey"]}
    ...    userHandle=${credentials["userHandle"]}
    New Page    ${CREDENTIAL_URL}
    Click    id=login
    Get Text    id=status    ==    Error during login: No matching credential

Add Empty Credential
    Create Credential
    ...    rpId=localhost
    New Page    ${CREDENTIAL_URL}
    Click    id=login
    Get Text    id=status    ==    Success

Get Credential Preinstalled
    Install Credential
    New Page    ${CREDENTIAL_URL}
    Click    id=navigatorCredentialsCreate
    Get Text    id=status    contains    Navigator Credentials Create Success
    ${id} =    Get Text    id=debug-id
    ${credential1} =    Get Credential    id_=${id}
    Take Screenshot
    Should Be Equal    ${credential1["id"]}    ${id}
    Should Be Equal    ${credential1["rpId"]}    localhost
    Should Be Equal    ${credential1["userHandle"]}    T_xTSNYHWRo
    Should Not Be Empty    ${credential1["privateKey"].value}
    Should Not Be Empty    ${credential1["publicKey"].value}
    ${credential2} =    Get Credential    rpId=localhost
    Compare Credentials    ${credential1}    ${credential2}

Delete Credential
    ${credentials} =    Get Credentials
    Create Credential
    ...    rpId=localhost
    ...    id_=${credentials["id"]}
    ...    privateKey=${credentials["privateKey"]}
    ...    publicKey=${credentials["publicKey"]}
    ...    userHandle=${credentials["userHandle"]}
    New Page    ${CREDENTIAL_URL}
    Click    id=login
    Get Text    id=status    ==    Success
    ${id} =    Get Text    id=debug-id
    ${credential} =    Get Credential    id_=${id}
    Should Be Equal    ${credential["id"]}    ${id}
    Delete Credential    id_=${id}
    Get Credential Should Fail
    Delete Credential    id_=${id}

Get Credential Without Creating Credential
    New Page    ${CREDENTIAL_URL}
    Get Credential Should Fail

*** Keywords ***
Credential Test Setup
    New Context

Credential Test Teardown
    Get Text    id=credentialDebug    text_type=allTextContents
    Close Context    ALL

Compare Credentials
    [Arguments]    ${expected}    ${actual}
    Should Be Equal    ${expected["id"]}    ${actual["id"]}
    Should Be Equal    ${expected["rpId"]}    ${actual["rpId"]}
    Should Be Equal    ${expected["userHandle"]}    ${actual["userHandle"]}
    Should Be Equal    ${expected["privateKey"].value}    ${actual["privateKey"].value}
    Should Be Equal    ${expected["publicKey"].value}    ${actual["publicKey"].value}

Get Credential Should Fail
    VAR    ${Failed} =    ${False}
    TRY
        Get Credential    id_=invalid
    EXCEPT    TypeError*    type=GLOB    AS    ${error}
        Log    ${error}
        VAR    ${Failed} =    ${True}
    END
    IF    ${Failed}
        Log    Credential retrieval failed as expected.
    ELSE
        Fail    Credential retrieval did not fail as expected.
    END
