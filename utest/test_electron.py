import json
from datetime import timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from Browser import Browser
from Browser.generated.playwright_pb2 import Response


def test_electron_sends_zero_timeout_and_returns_page_details():
    library = Browser()
    stub = MagicMock()
    stub.LaunchElectron.return_value = Response.NewPersistentContextResponse(
        browserId="browser=electron",
        id="context=electron",
        pageId="page=electron",
        video=json.dumps({"video_path": None, "contextUuid": "context=electron"}),
    )
    with patch.object(library.playwright, "grpc_channel") as channel:
        channel.return_value.__enter__.return_value = stub
        browser_id, context_id, page = library.new_electron_application(
            Path("/electron"), timeout=timedelta(0)
        )
    request = stub.LaunchElectron.call_args.args[0]
    assert request.defaultTimeout == 0
    assert json.loads(request.rawOptions)["timeout"] == 0
    assert browser_id == "browser=electron"
    assert context_id == "context=electron"
    assert page["page_id"] == "page=electron"
    assert page["video_path"] == ""


def test_electron_resolves_recording_path_and_embeds_video(tmp_path):
    library = Browser()
    stub = MagicMock()
    video_path = str(tmp_path / "recording.webm")
    stub.LaunchElectron.return_value = Response.NewPersistentContextResponse(
        id="context=electron",
        video=json.dumps({"video_path": video_path, "contextUuid": "context=electron"}),
    )
    with patch.object(library.playwright, "grpc_channel") as channel:
        channel.return_value.__enter__.return_value = stub
        _, _, page = library.new_electron_application(
            Path("/electron"),
            recordVideo={"dir": str(tmp_path), "size": {"width": 640, "height": 480}},
        )
    options = json.loads(stub.LaunchElectron.call_args.args[0].rawOptions)
    assert options["recordVideo"]["dir"] == str(tmp_path.resolve())
    assert library._context_cache.get("context=electron") == {
        "width": 640,
        "height": 480,
    }
    assert page["video_path"] == video_path


def test_electron_close_uses_browser_close_deadline():
    library = Browser()
    with patch.object(library.playwright, "grpc_channel") as channel:
        library.close_electron_application()
    assert (
        channel.return_value.__enter__.return_value.CloseElectron.call_args.kwargs
        == {"timeout": 20}
    )


def test_electron_native_viewport_keeps_default_video_dimensions(tmp_path):
    library = Browser()
    stub = MagicMock()
    stub.LaunchElectron.return_value = Response.NewPersistentContextResponse(
        id="context=electron", video="{}"
    )
    with patch.object(library.playwright, "grpc_channel") as channel:
        channel.return_value.__enter__.return_value = stub
        library.new_electron_application(
            Path("/electron"), viewport=None, recordVideo={"dir": str(tmp_path)}
        )
    options = json.loads(stub.LaunchElectron.call_args.args[0].rawOptions)
    assert options["viewport"] is None
    assert options["recordVideo"]["size"] == {"width": 1280, "height": 720}
