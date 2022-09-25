*** Settings ***
Resource            scope_keywords.resource

Suite Setup         Set New Global Settings
Suite Teardown      Reset Global Settings

*** Variables ***
${org_timeout} =    ${None}
${org_retry} =      ${None}
${org_strict} =     ${None}
${org_prefix} =     ${None}

*** Keywords ***
Close All And Open New Browser
    Close Browser    ALL
    Set New Global Settings

Set New Global Settings
    ${org_timeout} =    Set Browser Timeout    1000 ms    scope=global
    Set Global Variable    $org_timeout
    ${org_retry} =    Set Retry Assertions For    1000 ms    scope=global
    Set Global Variable    $org_retry
    ${org_strict} =    Set Strict Mode    False    scope=global
    Set Global Variable    $org_strict
    ${org_prefix} =    Set Selector Prefix    ${EMPTY}
    Set Global Variable    $org_prefix

    Log All Scopes    1000    1000    False    ${EMPTY}

Reset Global Settings
    Set Browser Timeout    ${org_timeout}    scope=global
    Set Retry Assertions For    ${org_retry}    scope=global
    Set Strict Mode    ${org_strict}    scope=global
    Set Selector Prefix    ${org_prefix}    scope=global
