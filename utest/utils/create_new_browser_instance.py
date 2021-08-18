import Browser

browser = Browser.Browser()
browser.new_page("https://youtube.com")
port: int = browser.playwright.port  # type: ignore


print(port)

while True:
    command = input()
    if command == "stop":
        browser.close_browser("ALL")
        break
