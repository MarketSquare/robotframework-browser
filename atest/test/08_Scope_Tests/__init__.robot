*** Settings ***
Resource            ../keywords.resource

Suite Setup         Set New Global Settings
Suite Teardown      Reset Global Settings

*** Variables ***
${org_timeout} =    ${None}
${org_retry} =      ${None}
${org_strict} =     ${None}

*** Keywords ***
Close All And Open New Browser
    Close Browser    ALL
    Set New Global Settings

Set New Global Settings
    ${org_timeout} =    Set Browser Timeout    1001 ms    scope=global
    Set Global Variable    $org_timeout
    ${org_retry} =    Set Retry Assertions For    1001 ms    scope=global
    Set Global Variable    $org_retry
    ${org_strict} =    Set Strict Mode    False    scope=global
    Set Global Variable    $org_strict

Reset Global Settings
    Set Browser Timeout    ${org_timeout}    scope=global
    Set Retry Assertions For    ${org_retry}    scope=global
    Set Strict Mode    ${org_strict}    scope=global
