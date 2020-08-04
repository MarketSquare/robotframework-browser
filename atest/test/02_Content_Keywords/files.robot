*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Upload File
    Upload File    ${CURDIR}/test_upload_file
    Click    \#file_chooser
    Get Text    \#upload_label    ==    test_upload_file

Upload File with different name
    Upload File    ${CURDIR}/invalid_test_upload_file
    Click    \#file_chooser
    Get Text    \#upload_label    ==    wrong_upload_filename

Invalid Upload Path
    Run Keyword And Expect Error    STARTS: FileNotFoundError: [Errno 2] No such file or directory:    Upload File    NonExistentFile
