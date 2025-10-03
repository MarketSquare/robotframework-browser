*** Settings ***
Resource            ../variables.resource
Library             Browser    enable_presenter_mode=True
Library             ../../library/presenter_mode.py

Suite Setup         New Browser    headless=False
Suite Teardown      Close Browser

Test Tags           slow    no-iframe    no-docker-pr

*** Test Cases ***
Filling The Text With True
    New Page    ${LOGIN_URL}
    Type Text    input#username_field    user

Filling The Text With Settings
    Set Presenter Mode    {"color": "red", "duration": "1s", "style": "solid"}
    New Page    ${LOGIN_URL}
    Type Text    input#username_field    user
    [Teardown]    Set Presenter Mode    False
