import json

import pytest

import tasks


@pytest.fixture
def nodejs_org(monkeypatch):
    def serve(*releases):
        def download(_url, destination):
            destination.write_text(json.dumps(list(releases)), encoding="utf-8")

        monkeypatch.setattr(tasks, "_download", download)

    monkeypatch.setattr(tasks, "NODE_VERSION", "26.13.0")
    return serve


def test_prerelease_of_the_next_line_is_ignored(nodejs_org):
    nodejs_org(
        {"version": "v27.0.0-alpha.0.0.0", "lts": False},
        {"version": "v26.13.0", "lts": "Lithium"},
    )
    assert tasks._node_release_state() == ((26, 13, 0), (26, 13, 0), (26, 13, 0))


def test_prerelease_in_the_shipped_line_is_not_a_bump(nodejs_org):
    nodejs_org(
        {"version": "v26.14.0-rc.1", "lts": False},
        {"version": "v26.13.0", "lts": "Lithium"},
    )
    assert tasks._node_release_state()[1] == (26, 13, 0)
