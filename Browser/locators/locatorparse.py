class LocatorParse:

    _strategies = ["css", "xpath", "id", "text"]

    def parse_locator(self, locator: str):
        if locator.startswith(("//", "(//")):
            return f"xpath={locator}"
        if ":" not in locator:
            return f"css={locator}"
        strategy, locator = locator.split(":", 1)
        return f"{strategy.rstrip()}={locator.lstrip()}"
