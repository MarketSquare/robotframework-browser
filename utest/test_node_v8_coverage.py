import io
import sys

import pytest

from Browser import playwright
from Browser.playwright import spawn_wrapper_process

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Node coverage is not collected on Windows"
)


@pytest.fixture
def spawned_env(monkeypatch):
    received = {}

    def fake_popen(args, env, **kwargs):
        received["NODE_V8_COVERAGE"] = env.get("NODE_V8_COVERAGE")

    monkeypatch.setattr(playwright, "Popen", fake_popen)
    monkeypatch.setenv("ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE", "1")
    monkeypatch.delenv("NODE_V8_COVERAGE", raising=False)
    return received


def _spawn(run_dir):
    spawn_wrapper_process(
        node_executable="node",
        script=run_dir / "index.js",
        cwd=run_dir,
        logfile=io.StringIO(),
        host="127.0.0.1",
        port="0",
        enable_playwright_debug=False,
        coverage_output=run_dir,
    )


def test_node_writes_coverage_to_run_output_by_default(spawned_env, tmp_path):
    _spawn(tmp_path)
    assert spawned_env["NODE_V8_COVERAGE"] == str(tmp_path / "node-v8-coverage")


def test_explicit_node_v8_coverage_wins(spawned_env, tmp_path, monkeypatch):
    explicit = tmp_path / "explicit"
    monkeypatch.setenv("NODE_V8_COVERAGE", str(explicit))
    _spawn(tmp_path / "run")
    assert spawned_env["NODE_V8_COVERAGE"] == str(explicit)


def test_each_run_writes_coverage_to_its_own_output(spawned_env, tmp_path):
    _spawn(tmp_path / "first")
    _spawn(tmp_path / "second")
    assert spawned_env["NODE_V8_COVERAGE"] == str(
        tmp_path / "second" / "node-v8-coverage"
    )
