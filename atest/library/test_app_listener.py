import logging
import os

import requests
from robot.api import logger

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
from robot.libraries.BuiltIn import BuiltIn


def _post(event: str, data, status: str | None = None) -> None:
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
        requests.post(
            f"http://{server}/api/log/context",
            json=entry,
            timeout=2,
        )
    except Exception as error:  # noqa: BLE001
        logger.debug(
            f"Listener: Failed to POST event: {event}, id={data.id}, name={data.name}, status={status}, server={server} - {error!r}"
        )

def start_suite(data, result):
    _post("start_suite", data)

def end_suite(data, result):
    _post("end_suite", data, status=result.status)

def start_test(data, result):
    _post("start_test", data)

def end_test(data, result):
    _post("end_test", data, status=result.status)
