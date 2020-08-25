import contextlib
import socket


def find_free_port() -> str:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def is_same_keyword(first: str, second: str) -> bool:
    if isinstance(first, str) and isinstance(second, str):
        return get_normalized_keyword(first) == get_normalized_keyword(second)
    else:
        return False


def get_normalized_keyword(keyword: str) -> str:
    return keyword.lower().replace(" ", "").replace("_", "")
