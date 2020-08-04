*** Settings ***
Resource          imports.resource

*** Test Cases ***
Upload File
    New Page    ${LOGIN_URL}
    Upload File    ${CURDIR}/test_upload_file
    Click    \#file_chooser
    Get Text    \#upload_label    ==    test_upload_file

Upload File with different name
    New Page    ${LOGIN_URL}
    Upload File    ${CURDIR}/invalid_test_upload_file
    Click    \#file_chooser
    Get Text    \#upload_label    ==    wrong_upload_filename

Invalid Upload Path
    Run Keyword And Expect Error    STARTS: FileNotFoundError: [Errno 2] No such file or directory:    Upload File    NonExistentFile

Wait For Download
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise}    Promise To    Wait For Download
    Click    \#file_download
    ${file_path}=    Wait For    ${dl_promise}
    File Should Exist    ${file_path}
    Remove File    ${file_path}
#Wait For Download with custom path
#    New Context    acceptDownloads=True
#    New Page    ${LOGIN_URL}
#    ${dl_promise}=    Promise To    Wait For Download    saveAs=${CURDIR}/download_file
#    Click    \#file_download
#    ${file_path}=    Wait For    ${dl_promise}
#    File Should Exist    ${file_path}
#    Remove File    ${file_path}
#    Fail
