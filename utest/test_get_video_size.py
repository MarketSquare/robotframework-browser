import pytest
from approvaltests import verify_all  # type: ignore

from Browser.keywords import PlaywrightState


@pytest.fixture
def state():
    return PlaywrightState(None)


def test_get_video_size(state: PlaywrightState):
    results = [
        state._get_video_size({}),
        state._get_video_size({"recordVideo": {"path": "/path/to"}}),
        state._get_video_size({"recordVideo": {"size": {"width": 12, "height": 11}}}),
        state._get_video_size({"viewport": {"width": 123, "height": 111}}),
        state._get_video_size(
            {
                "recordVideo": {"size": {"width": 12, "height": 11}},
                "viewport": {"width": 123, "height": 111},
            }
        ),
    ]
    verify_all("Video size", results)
