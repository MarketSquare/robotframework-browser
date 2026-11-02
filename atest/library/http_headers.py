def header_values(headers_array: list[dict], name: str) -> list[str]:
    """Return the values of all entries in ``headersArray`` named ``name``, ignoring case."""
    return [
        entry["value"] for entry in headers_array if entry["name"].lower() == name.lower()
    ]
