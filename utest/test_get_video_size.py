import pytest
from approvaltests.approvals import verify_all  # type: ignore

from Browser.keywords import PlaywrightState


@pytest.fixture
def state():
    return PlaywrightState(None)


def test_get_video_size(state: PlaywrightState):
    results = [
        state._video_size({}, None),
        state._video_size({"path": "/path/to"}, None),
        state._video_size({"size": {"width": 12, "height": 11}}, None),
        state._video_size({}, {"width": 123, "height": 111}),
        state._video_size(
            {"size": {"width": 12, "height": 11}}, {"width": 123, "height": 111}
        ),
    ]
    verify_all("Video size", results)
