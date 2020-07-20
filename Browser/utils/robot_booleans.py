from typing import Any

TRUE_STRINGS = {"TRUE", "YES", "ON", "1", "CHECKED"}
FALSE_STRINGS = {"FALSE", "NO", "OFF", "0", "UNCHECKED", "NONE", ""}


def is_truthy(item: Any) -> bool:
    if isinstance(item, bool):
        return item
    parsed = item.upper()
    if parsed in FALSE_STRINGS:
        return False
    elif parsed in TRUE_STRINGS:
        return True
    else:
        raise ValueError(f"{item} is not a valid Robot Framework boolean")


def is_falsy(item: Any) -> bool:
    return not is_truthy(item)
