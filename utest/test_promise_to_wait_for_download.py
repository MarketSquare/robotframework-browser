from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from Browser.generated.playwright_pb2 import Response
from Browser.keywords.promises import Promises

DOWNLOAD = {
    "saveAs": "",
    "suggestedFilename": "f.txt",
    "state": "in_progress",
    "downloadID": "id",
}
LISTENING = Response.Json(log="Listening for download")


class _Node:
    def __init__(self):
        self.listening = threading.Event()
        self.download_started = threading.Event()

    def WaitForDownload(self, request):
        self.listening.wait()
        yield LISTENING
        self.download_started.wait()
        yield Response.Json(json=json.dumps(DOWNLOAD), log="Download started")


@pytest.fixture
def executor() -> Iterator[ThreadPoolExecutor]:
    executor = ThreadPoolExecutor(max_workers=2)
    yield executor
    executor.shutdown(wait=False, cancel_futures=True)


def _promises(node, executor: ThreadPoolExecutor) -> Promises:
    @contextmanager
    def grpc_channel():
        yield node

    promises = Promises.__new__(Promises)
    promises.library = SimpleNamespace(
        playwright=SimpleNamespace(grpc_channel=grpc_channel),
        _unresolved_promises=set(),
    )
    promises._executor = executor
    return promises


def test_returns_only_after_node_listens_for_the_download(executor):
    node = _Node()
    promises = _promises(node, executor)
    returned = threading.Event()
    keyword = threading.Thread(
        target=lambda: (promises.promise_to_wait_for_download(), returned.set())
    )

    keyword.start()
    assert not returned.wait(0.3)
    node.listening.set()
    assert returned.wait(5)
    keyword.join()

    node.download_started.set()
    (promise,) = promises.unresolved_promises
    assert promise.result(5).downloadID == "id"


def test_returns_when_node_fails_before_listening(executor):
    class _FailingNode:
        def WaitForDownload(self, request):
            raise AssertionError("No active page")
            yield

    promises = _promises(_FailingNode(), executor)

    promise = promises.promise_to_wait_for_download()

    with pytest.raises(AssertionError, match="No active page"):
        promise.result(5)


def test_fails_the_promise_when_node_fails_after_listening(executor):
    class _TimingOutNode:
        def WaitForDownload(self, request):
            yield LISTENING
            raise AssertionError("Timeout 3000ms exceeded")

    promises = _promises(_TimingOutNode(), executor)

    promise = promises.promise_to_wait_for_download()

    with pytest.raises(AssertionError, match="Timeout 3000ms exceeded"):
        promise.result(5)


def test_fails_the_promise_when_the_stream_ends_after_listening(executor):
    class _EndingNode:
        def WaitForDownload(self, request):
            yield LISTENING

    promises = _promises(_EndingNode(), executor)

    promise = promises.promise_to_wait_for_download()

    with pytest.raises(AssertionError, match="ended before the download started"):
        promise.result(5)
