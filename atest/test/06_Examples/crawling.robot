*** Settings ***
Library     Collections
Library     Browser
Resource    imports.resource

*** Test Cases ***
Normal Crawling
    Set Test Variable    @{TITLES}    @{EMPTY}
    ${urls} =    Crawl site    ${LINKER_URL}    My page keyword
    log list    ${TITLES}
    sort list    ${TITLES}
    ${expected} =    Create List    Always    Link 1    Link 2    Link 3    Link 4
    lists should be equal    ${TITLES}    ${expected}

Crawling only limited pages
    Set Test Variable    @{TITLES}    @{EMPTY}
    ${urls} =    Crawl site    ${LINKER_URL}    My page keyword    max_number_of_page_to_crawl=4
    log list    ${TITLES}
    sort list    ${TITLES}
    ${expected} =    Create List    Always    Link 1    Link 2    Link 3
    lists should be equal    ${TITLES}    ${expected}

Crawling only limited depth
    Set Test Variable    @{TITLES}    @{EMPTY}
    ${urls} =    Crawl site    ${LINKER_URL}    My page keyword    max_depth_to_crawl=1
    log list    ${TITLES}
    sort list    ${TITLES}
    ${expected} =    Create List    Always    Link 1    Link 2
    lists should be equal    ${TITLES}    ${expected}

*** Keywords ***
My page keyword
    ${title} =    get title
    log    ${TITLES}
    append to list    ${TITLES}    ${title}
