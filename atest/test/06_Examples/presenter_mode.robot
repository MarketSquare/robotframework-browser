*** Settings ***
Resource            ../variables.resource
Library             Browser    enable_presenter_mode=True
Library             ../../library/presenter_mode.py

Suite Setup         New Browser    headless=False
Suite Teardown      Close Browser

*** Test Cases ***
Filling the text with True
    New Page    ${LOGIN_URL}
    type text    input#username_field    user

Filling the text with settings
    Set Presenter Mode    {"color": "red", "duration": "1s", "style": "solid"}
    New Page    ${LOGIN_URL}
    type text    input#username_field    user
