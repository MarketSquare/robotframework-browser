import json

import pytest
from approvaltests import verify  # type: ignore

from Browser.base import ContextCache

ITEM = {"video": "/path/to/file", "size": {"x": 1, "y": 2}}


@pytest.fixture
def cache():
    return ContextCache()


@pytest.fixture
def cache_items(cache: ContextCache):
    cache.add("a1", ITEM)
    cache.add("b2", ITEM)
    return cache


def _verify(athing):
    verify(json.dumps(athing, indent=4) + '\n')


def _verify_cache(cache: ContextCache):
    _verify(cache.cache)


def test_cache_is_empty(cache: ContextCache):
    _verify_cache(cache)


def test_add_cache(cache: ContextCache):
    cache.add("a1", ITEM)
    cache.add("b2", ITEM)
    _verify_cache(cache)


def test_remove_item_no_item(cache: ContextCache):
    cache.remove("a1")
    _verify_cache(cache)


def test_remove_item(cache_items: ContextCache):
    cache_items.remove("a1")
    _verify_cache(cache_items)


def test_get_item(cache_items: ContextCache):
    _verify(cache_items.get("a1"))


def test_get_item_no_item(cache_items: ContextCache):
    _verify(cache_items.get("not-here"))
