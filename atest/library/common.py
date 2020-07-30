from typing import NamedTuple
from urllib.parse import urlparse


def parse_url(url: str) -> NamedTuple:
    return urlparse(url)
