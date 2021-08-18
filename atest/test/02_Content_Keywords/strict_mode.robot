*** Settings ***
Resource    imports.resource

*** Test Cases ***
Set Strict Mode
    ${old_mode} =    Set Strict Mode    False
    Should Be True    ${old_mode}
    ${old_mode} =    Set Strict Mode    True
    Should Not Be True    ${old_mode}
    ${old_mode} =    Set Strict Mode    ${True}
    Should Be True    ${old_mode}
