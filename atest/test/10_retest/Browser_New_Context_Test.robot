*** Settings ***
Library             Browser
Library             OperatingSystem
Library             mylib.py
Resource            ../variables.resource

Suite Teardown      Clean Up
Test Setup          New Browser And Path Setup
Test Teardown       Close Browser    ALL
Test Timeout        10 minutes

*** Variables ***
${non_existing_relative_path} =     new_rel_folder
${existing_relative_path} =         existing_rel_folder
${non_existing_absolute_path} =     ${OUTPUT_DIR}/new_abs_folder
${existing_absolute_path} =         ${OUTPUT_DIR}/existing_abs_folder

*** Test Cases ***
Test New Context With Existing Path Of Type String
    [Template]    Create New Context With recordVideo.dir As String And Validate That recordVideo.dir After New Context Call Is Of Type String
    ${existing_relative_path}
    ${existing_absolute_path}

Test New Context With Non-existing Path Of Type String
    [Template]    Create New Context With recordVideo.dir As String And Validate That recordVideo.dir After New Context Call Is Of Type String
    ${non_existing_relative_path}
    ${non_existing_absolute_path}

Test New Context With Existing Path Of Type Path
    [Template]    Create New Context With recordVideo.dir As Path And Validate That recordVideo.dir After New Context Call Is Of Type Path
    ${existing_relative_path}
    ${existing_absolute_path}

Test New Context With Non-existing Path Of Type Path
    [Template]    Create New Context With recordVideo.dir As Path And Validate That recordVideo.dir After New Context Call Is Of Type Path
    ${non_existing_relative_path}
    ${non_existing_absolute_path}

Test New Persistent Context With Existing Path Of Type String
    [Template]    Create New Persistent Context With recordVideo.dir As String And Validate That recordVideo.dir After New Context Call Is Of Type String
    ${existing_relative_path}
    ${existing_absolute_path}

Test New Persistent Context With Non-existing Path Of Type String
    [Template]    Create New Persistent Context With recordVideo.dir As String And Validate That recordVideo.dir After New Context Call Is Of Type String
    ${non_existing_relative_path}
    ${non_existing_absolute_path}

Test New Persistent Context With Existing Path Of Type Path
    [Template]    Create New Persistent Context With recordVideo.dir As Path And Validate That recordVideo.dir After New Context Call Is Of Type Path
    ${existing_relative_path}
    ${existing_absolute_path}

Test New Persistent Context With Non-existing Path Of Type Path
    [Template]    Create New Persistent Context With recordVideo.dir As Path And Validate That recordVideo.dir After New Context Call Is Of Type Path
    ${non_existing_relative_path}
    ${non_existing_absolute_path}

*** Keywords ***
New Browser And Path Setup
    New Browser
    Create Directory    ${OUTPUT_DIR}/browser/video/${existing_relative_path}
    Create Directory    ${existing_absolute_path}
    Remove Directory    ${OUTPUT_DIR}/browser/video/${non_existing_relative_path}    recursive=True
    Remove Directory    ${non_existing_absolute_path}    recursive=True

Clean Up
    Remove Directory    ${OUTPUT_DIR}/browser/video/${existing_relative_path}    recursive=True
    Remove Directory    ${existing_absolute_path}    recursive=True
    Remove Directory    ${OUTPUT_DIR}/browser/video/${non_existing_relative_path}    recursive=True
    Remove Directory    ${non_existing_absolute_path}    recursive=True

Create New Context With RecordVideo.Dir As String And Validate That RecordVideo.Dir After New Context Call Is Of Type String
    [Arguments]    ${path}
    ${dir_type} =    Create Context With String Type RecordVideodir And Get Type Of RecordVideo Dir    ${path}
    Log    Type of recordVideo.dir with given value (${path}) is ${dir_type}
    Should Be Equal As Strings    ${dir_type}    <class 'str'>

Create New Context With RecordVideo.Dir As Path And Validate That RecordVideo.Dir After New Context Call Is Of Type Path
    [Arguments]    ${path}
    ${dir_type} =    Create Context With Path Type RecordVideodir And Get Type Of RecordVideo Dir    ${path}
    Log    Type of recordVideo.dir with given value (${path}) is ${dir_type}
    Should Match Regexp    ${dir_type}    <class 'pathlib.+Path'>    # Python 3.13 need mode wired regex

Create New Persistent Context With RecordVideo.Dir As String And Validate That RecordVideo.Dir After New Context Call Is Of Type String
    [Arguments]    ${path}
    ${dir_type} =    Create Persistent Context With String Type RecordVideodir And Get Type Of RecordVideo Dir
    ...    ${path}
    Log    Type of recordVideo.dir with given value (${path}) is ${dir_type}
    Should Be Equal As Strings    ${dir_type}    <class 'str'>

Create New Persistent Context With RecordVideo.Dir As Path And Validate That RecordVideo.Dir After New Context Call Is Of Type Path
    [Arguments]    ${path}
    ${dir_type} =    Create Persistent Context With Path Type RecordVideodir And Get Type Of RecordVideo Dir    ${path}
    Log    Type of recordVideo.dir with given value (${path}) is ${dir_type}
    Should Match Regexp    ${dir_type}    <class 'pathlib.+Path'>    # Python 3.13 need mode wired regex
