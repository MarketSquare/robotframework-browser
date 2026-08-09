import pytest
from invoke import Exit

from tasks import (
    DOCKERFILES,
    PLAYWRIGHT_IMAGE,
    _dockerfile_pw_images,
    _locked_pw_version,
    _stale_dockerfiles,
)


def test_nothing_stale_when_every_dockerfile_matches():
    images = {
        "Dockerfile.dev_pr": ("1.62.1", "v1.62.1-noble"),
        "Dockerfile.latest_release": ("1.62.1", "v1.62.1-noble"),
    }
    assert _stale_dockerfiles("1.62.1", images) == []


def test_a_patch_behind_is_stale():
    images = {
        "Dockerfile.dev_pr": ("1.62.0", "v1.62.0-noble"),
        "Dockerfile.latest_release": ("1.62.1", "v1.62.1-noble"),
    }
    assert _stale_dockerfiles("1.62.1", images) == ["Dockerfile.dev_pr"]


def test_stale_names_are_sorted():
    images = {
        "Dockerfile.latest_release": ("1.61.0", "v1.61.0-noble"),
        "Dockerfile.dev_pr": ("1.62.0", "v1.62.0-noble"),
    }
    assert _stale_dockerfiles("1.62.1", images) == [
        "Dockerfile.dev_pr",
        "Dockerfile.latest_release",
    ]


def test_the_repository_dockerfiles_are_readable():
    images = _dockerfile_pw_images()
    assert sorted(images) == sorted(path.name for path in DOCKERFILES)
    for version, tag in images.values():
        assert tag.startswith(f"v{version}")


def test_the_repository_is_on_one_playwright_version():
    assert _stale_dockerfiles(_locked_pw_version(), _dockerfile_pw_images()) == []


def test_a_dockerfile_without_a_playwright_image_is_an_error(tmp_path, monkeypatch):
    dockerfile = tmp_path / "Dockerfile.dev_pr"
    dockerfile.write_text("FROM python:3.14\n", encoding="utf-8")
    monkeypatch.setattr("tasks.DOCKERFILES", (dockerfile,))
    with pytest.raises(Exit):
        _dockerfile_pw_images()


def test_the_image_pattern_keeps_the_distro_suffix():
    line = "FROM mcr.microsoft.com/playwright:v1.62.0-noble"
    assert PLAYWRIGHT_IMAGE.sub(r"\g<image>1.62.1", line) == (
        "FROM mcr.microsoft.com/playwright:v1.62.1-noble"
    )
