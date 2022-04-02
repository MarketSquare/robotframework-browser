*** Settings ***
Library     Browser    timeout=5s    retry_assertions_for=3s
Resource    imports.resource

*** Test Cases ***
Issue 1685
    New Page    url=http://www.google.com
    ${promise} =    Promise To    Wait For Response    timeout=2s
    Wait For    ${promise}
