"""Tests for tools/ci_failures/commands.py: what each `inv ci-*` task prints and
which exit code it refuses with. See ADR 0007."""

import json
import zipfile

import pytest

from tools.ci_failures import commands, github, workspace
from tools.ci_failures.db import UnanswerableError
from tools.ci_failures.refusal import MisaskedError, UnreachableError

from .test_tool_ci_failures import seed

LEG = "source · ubuntu-latest · shard 1 · 3.14 · 22.x"
ARTIFACT = "Test results-ubuntu-latest-1-3.14-22.x"


@pytest.fixture
def one_leg_on_github(monkeypatch, tmp_path):
    """Run 1 on GitHub with one Leg, whose artifact holds an empty output.xml."""
    zip_path = tmp_path / "artifact.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("output.xml", "<robot/>")

    def download(artifact_id, destination):
        destination.write_bytes(zip_path.read_bytes())
        return destination

    monkeypatch.setattr(
        github,
        "list_test_artifacts",
        lambda run_id: [github.Artifact(id=7, name=ARTIFACT, expired=False, url="u")],
    )
    monkeypatch.setattr(
        github,
        "get_run",
        lambda run_id: github.Run(
            id=run_id,
            event="push",
            head_sha="s",
            head_branch="main",
            created_at="2026-09-27T10:00:00Z",
            conclusion="failure",
            url="u",
        ),
    )
    monkeypatch.setattr(github, "download_artifact", download)


class TestArtifact:
    def test_without_run_and_leg_test_or_clean_it_is_misasked(self, tmp_path):
        with pytest.raises(MisaskedError, match="--run and --leg") as refused:
            commands.artifact(run="1", db=tmp_path / "ci.sqlite3", out=print)

        assert refused.value.code == 2

    @pytest.mark.parametrize(
        "flags",
        [
            {"run": "latest", "leg": "wheel · windows-latest"},
            {"run": "1", "leg": "wheel · windows-latest", "attempt": "second"},
            {"run": "latest", "test": "Test.S.T"},
        ],
    )
    def test_a_run_or_attempt_that_is_not_a_number_is_misasked(self, tmp_path, flags):
        with pytest.raises(MisaskedError, match="whole number"):
            commands.artifact(**flags, db=tmp_path / "ci.sqlite3", out=print)

    def test_a_fetch_github_refuses_is_unreachable(
        self, one_leg_on_github, monkeypatch, tmp_path
    ):
        def offline(artifact_id, destination):
            raise github.GhError("could not resolve host")

        monkeypatch.setattr(github, "download_artifact", offline)

        with pytest.raises(UnreachableError) as refused:
            commands.artifact(run="1", leg=LEG, db=tmp_path / "ci.sqlite3", out=print)

        assert refused.value.code == 3

    def test_a_leg_the_run_does_not_have_is_unanswerable(
        self, one_leg_on_github, tmp_path
    ):
        with pytest.raises(UnanswerableError, match="has no leg") as refused:
            commands.artifact(
                run="1", leg="wheel · windows-latest", db=tmp_path / "ci.sqlite3"
            )

        assert refused.value.code == 1

    def test_a_fetched_leg_prints_its_shortlist(self, one_leg_on_github, tmp_path):
        said: list[str] = []

        commands.artifact(run="1", leg=LEG, db=tmp_path / "ci.sqlite3", out=said.append)

        assert said[0].startswith("directory:")
        assert said[0].endswith("1-source-ubuntu-latest-shard-1-3.14-22.x-attempt-1")
        assert said[1].startswith("output.xml:")

    def test_run_and_test_without_leg_lists_the_runs_legs_from_the_database(
        self, tmp_path
    ):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "FAIL", "artifact": ARTIFACT}])
        said: list[str] = []

        commands.artifact(run="1", test="Test.S.T", db=db, out=said.append)

        assert said[0] == "Run 1 · commit sha1 · Test.S.T"
        assert said[-1].startswith("fetch one: inv ci-artifact --run 1")

    def test_listing_legs_with_no_database_is_unanswerable(self, tmp_path):
        with pytest.raises(UnanswerableError) as refused:
            commands.artifact(
                run="1", test="Test.S.T", db=tmp_path / "ci.sqlite3", out=print
            )

        assert refused.value.code == 1
        assert not (tmp_path / "ci.sqlite3").exists()

    def test_clean_removes_the_fetched_artifacts_and_says_so(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        workspace.artifacts(db).mkdir()
        said: list[str] = []

        commands.artifact(clean=True, db=db, out=said.append)

        assert not workspace.artifacts(db).exists()
        assert said == [f"Removed {workspace.artifacts(db)}"]


class TestReport:
    def test_a_baseline_of_one_test_is_misasked(self, tmp_path):
        with pytest.raises(MisaskedError, match="without --test"):
            commands.report(
                test="Test.S.T", mark_seen=True, db=tmp_path / "ci.sqlite3", out=print
            )

    @pytest.mark.parametrize(
        ("flags", "why"),
        [
            ({"days": "seven"}, "--days wants a whole number, got 'seven'."),
            ({"days": "0"}, "--days must be 1 or more, got 0"),
            ({"limit": "many"}, "--limit wants a whole number, got 'many'."),
        ],
    )
    def test_a_flag_that_is_not_its_value_is_misasked(self, tmp_path, flags, why):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "PASS"}])

        with pytest.raises(MisaskedError) as refused:
            commands.report(**flags, db=db, out=print)

        assert str(refused.value) == why

    def test_a_baseline_of_a_window_is_misasked(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "FAIL", "signature": "boom"}])

        with pytest.raises(MisaskedError) as refused:
            commands.report(mark_seen=True, days="400", db=db, out=print)

        assert refused.value.code == 2

    def test_no_database_is_unanswerable_and_creates_none(self, tmp_path):
        db = tmp_path / "ci.sqlite3"

        with pytest.raises(UnanswerableError):
            commands.report(db=db, out=print)

        assert not db.exists()

    def test_a_test_name_in_no_result_is_unanswerable_with_what_it_may_mean(
        self, tmp_path
    ):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.Login Works", "status": "PASS"}])

        with pytest.raises(UnanswerableError, match=r"Test\.S\.Login Works"):
            commands.report(test="Test.S.Login Work", db=db, out=print)

    def test_a_test_that_never_failed_gets_one_line_and_no_files(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "PASS"}])
        said: list[str] = []

        commands.report(test="Test.S.T", db=db, out=said.append)

        assert said == ["'Test.S.T' ran 1 time in all history: 0 failures, 0 skips."]
        assert not workspace.page(db).exists()

    def test_a_test_that_failed_is_printed_as_the_document(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "FAIL", "signature": "boom"}])
        said: list[str] = []

        commands.report(test="Test.S.T", db=db, out=said.append)

        (document,) = said
        assert [g["test"] for g in json.loads(document)["test_failures"]] == [
            "Test.S.T"
        ]
        assert not workspace.page(db).exists()

    def test_by_default_the_page_is_written_beside_the_database_and_opened(
        self, tmp_path
    ):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "FAIL", "signature": "boom"}])
        said: list[str] = []
        opened: list = []

        commands.report(db=db, open_it=True, out=said.append, open_page=opened.append)

        assert said == [f"Wrote {workspace.page(db)}"]
        assert opened == [workspace.page(db)]

    def test_json_alone_writes_no_page(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "FAIL", "signature": "boom"}])
        said: list[str] = []

        commands.report(db=db, json=tmp_path / "r.json", out=said.append)

        assert said == [f"Wrote {tmp_path / 'r.json'}"]
        assert not workspace.page(db).exists()

    def test_a_baseline_is_recorded_before_the_renderings_are_written(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "Test.S.T", "status": "FAIL", "signature": "boom"}])
        said: list[str] = []

        commands.report(db=db, mark_seen=True, out=said.append)

        assert said[0].startswith("Baseline recorded at ")
        assert said[1:] == [f"Wrote {workspace.page(db)}"]
