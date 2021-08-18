import Browser

browser = Browser.Browser()
browser.new_page("https://youtube.com")
port: int = browser.playwright.port  # type: ignore


print(port)
print("")

while True:
    try:
        command = input()
    except Exception:
        command = ""
    if command == "stop":
        browser.close_browser("ALL")
        break
