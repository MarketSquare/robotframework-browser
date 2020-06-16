class LocatorParse:

    _strategies_light = ("css:light", "text:light")
    _strategies = ("css", "xpath", "id", "text", *_strategies_light)

    def parse_locator(self, locator: str):
        if locator.startswith(("//", "(//")):
            return f"xpath={locator}"
        index = self._strategy_index(locator)
        if index != -1:
            strategy = locator[:index].strip()
            if strategy in self._strategies:
                return f"{strategy}={locator[index + 1:].lstrip()}"
        return f"css={locator}"

    def _strategy_index(self, locator: str):
        if locator.lower().startswith(self._strategies_light):
            strategy = ":".join(locator.split(":", 2)[:2])
            return len(strategy)
        return locator.find(":")
