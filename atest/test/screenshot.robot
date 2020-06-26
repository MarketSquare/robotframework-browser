*** Settings ***
Library		Browser
Library		OperatingSystem

Test Setup	Open Browser	http://localhost:7272
Test Teardown	Close Browser



*** Variables ***
${failure_screnshot}	${OUTPUT_DIR}${/}Test_screenshotting_failing_test_FAILURE_SCREENSHOT.png
${test_screenshot}	${OUTPUT_DIR}${/}test_screenshot

*** Test Cases ***
Test screenshotting failing test
    Input Text		css=input#username_field	username	
    Run Keyword And Expect Error	*content should be not_username but was `username`	TextField Value Should Be	css=input#username_field	not_username
    Should Exist	${failure_screnshot}
    Remove File		${failure_screnshot}
    Should Not Exist	${failure_screnshot}

Test screenshotting by using keyword
    Take Page Screenshot 	${test_screenshot}
    Should Exist	${test_screenshot}.png
    Remove File		${test_screenshot}.png
    Should Not Exist	${test_screenshot}.png
