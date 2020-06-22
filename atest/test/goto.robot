*** Settings ***
Library  Browser

*** Test Cases ***
No Open Browser Throws
    Run KeyWord and Expect Error	*details = "Tried to open URl but had no browser open"*	GoTo	"about:blank"
