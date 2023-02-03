*** Settings ***
Library         Collections
Resource        imports.resource

Force Tags      no-iframe

*** Test Cases ***
Normal Crawling
    Set Test Variable    @{TITLES}    @{EMPTY}
    ${urls} =    Crawl Site    ${LINKER_URL}    My page keyword
    Log List    ${TITLES}
    Sort List    ${TITLES}
    ${expected} =    Create List    Always    Link 1    Link 2    Link 3    Link 4
    Lists Should Be Equal    ${TITLES}    ${expected}

Crawling Only Limited Pages
    Set Test Variable    @{TITLES}    @{EMPTY}
    ${urls} =    Crawl Site    ${LINKER_URL}    My page keyword    max_number_of_page_to_crawl=4
    Log List    ${TITLES}
    Sort List    ${TITLES}
    ${expected} =    Create List    Always    Link 1    Link 2    Link 3
    Lists Should Be Equal    ${TITLES}    ${expected}

Crawling Only Limited Depth
    Set Test Variable    @{TITLES}    @{EMPTY}
    ${urls} =    Crawl Site    ${LINKER_URL}    My page keyword    max_depth_to_crawl=1
    Log List    ${TITLES}
    Sort List    ${TITLES}
    ${expected} =    Create List    Always    Link 1    Link 2
    Lists Should Be Equal    ${TITLES}    ${expected}

*** Keywords ***
My Page Keyword
    ${title} =    Get Title
    Log    ${TITLES}
    Append To List    ${TITLES}    ${title}
