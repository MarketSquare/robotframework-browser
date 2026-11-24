from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from types import SimpleNamespace

from Browser.generated.playwright_pb2 import Response
from Browser.keywords.promises import Promises

DOWNLOAD = {
    "saveAs": "",
    "suggestedFilename": "f.txt",
    "state": "in_progress",
    "downloadID": "id",
}


class _Node:
    def __init__(self):
        self.listening = threading.Event()
        self.download_started = threading.Event()

    def WaitForDownload(self, request):
        self.listening.wait()
        yield Response.Json(log="Listening for download")
        self.download_started.wait()
        yield Response.Json(json=json.dumps(DOWNLOAD), log="Download started")


def _promises(node: _Node) -> Promises:
    @contextmanager
    def grpc_channel():
        yield node

    promises = Promises.__new__(Promises)
    promises.library = SimpleNamespace(
        playwright=SimpleNamespace(grpc_channel=grpc_channel),
        _unresolved_promises=set(),
    )
    promises._executor = ThreadPoolExecutor(max_workers=2)
    return promises


def test_returns_only_after_node_listens_for_the_download():
    node = _Node()
    promises = _promises(node)
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


def test_returns_when_node_fails_before_listening():
    class _FailingNode(_Node):
        def WaitForDownload(self, request):
            raise AssertionError("No active page")
            yield

    promises = _promises(_FailingNode())

    promise = promises.promise_to_wait_for_download()

    assert isinstance(promise.exception(5), AssertionError)
