*** Settings ***
Library  Browser

*** Test Cases ***
No Open Browser Throws
    Run KeyWord and Expect Error	*	GoTo	"about:blank"
