import json
import os
from urllib import request as urllib_request

from robot.api.deco import library
from robot.libraries.BuiltIn import BuiltIn


@library(scope="GLOBAL", listener="SELF")
class TestAppListener:
    """Robot Framework listener that sends suite/test lifecycle events to the
    dynamic test-app log endpoint (``POST /api/log/context``).

    Registered automatically via ``@library(listener='SELF')`` — no explicit
    ``Register Listener`` call needed.  Import this library in
    ``atest/test/__init__.robot`` once and it covers the whole run.
    """

    ROBOT_LISTENER_API_VERSION = 3

    # ------------------------------------------------------------------
    # Listener hooks
    # ------------------------------------------------------------------

    def start_suite(self, data, result):
        self._post("start_suite", data)

    def end_suite(self, data, result):
        self._post("end_suite", data, status=result.status)

    def start_test(self, data, result):
        self._post("start_test", data)

    def end_test(self, data, result):
        self._post("end_test", data, status=result.status)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _post(self, event: str, data, status: str | None = None) -> None:
        server = BuiltIn().get_variable_value("${SERVER}")
        if not server:
            return
        entry: dict = {
            "event": event,
            "id": data.id,
            "name": data.name,
            "pid": os.getpid(),
        }
        if status is not None:
            entry["status"] = status
        try:
            payload = json.dumps(entry).encode("utf-8")
            req = urllib_request.Request(
                f"http://{server}/api/log/context",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib_request.urlopen(req, timeout=2):
                pass
        except Exception:  # noqa: BLE001
            pass
