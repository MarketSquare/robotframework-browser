class LocatorParse:

    _strategies = ["css", "xpath", "id"]
    css = "css"
    xpath = "xpath"
    id_ = "id"

    def parse_locator(self, locator: str):
        if locator.startswith(("//", "(//")):
            return f"{self.xpath}={locator}"
        if ":" not in locator:
            return f"css={locator}"
        strategy, locator = locator.split(":", 1)
        return f"{strategy.rstrip()}={locator.lstrip()}"
