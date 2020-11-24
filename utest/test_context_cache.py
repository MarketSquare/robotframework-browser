from __future__ import annotations
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


def test_cache_is_empty(cache: ContextCache):
    verify(json.dumps(cache.cache, indent=4))


def test_add_cache(cache: ContextCache):
    cache.add("a1", ITEM)
    cache.add("b2", ITEM)
    verify(json.dumps(cache.cache, indent=4))


def test_remove_item_no_item(cache: ContextCache):
    cache.remove("a1")
    verify(json.dumps(cache.cache, indent=4))


def test_remove_item(cache_items: ContextCache):
    cache_items.remove("a1")
    verify(json.dumps(cache_items.cache, indent=4))


def test_get_item(cache_items: ContextCache):
    verify(json.dumps(cache_items.get("a1"), indent=4))


def test_get_item_no_item(cache_items: ContextCache):
    verify(json.dumps(cache_items.get("not-here"), indent=4))
