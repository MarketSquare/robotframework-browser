#!/usr/bin/python3
"""
Script that outputs a changelog for the repository in the current directory and its submodules.

Manual actions needed to clean up for changelog:
    - Remove commits that are not meaningful for end users.
"""

import shlex
import re
import sys
from typing import Optional, Tuple, List, Literal
from subprocess import run as _run, STDOUT, PIPE
from dataclasses import dataclass


class CommitMsg:
    type: str
    subtype: str
    msg: str


CommitType = Literal["ci", "bump", "docs", "fix", "unknown"]


@dataclass
class Commit:
    id: str
    msg: str
    repo: str

    @property
    def msg_processed(self) -> str:
        """Generates links from commit and issue references (like 0c14d77, #123) to correct repo and such"""
        s = self.msg
        s = re.sub(
            r"#(\d+)",
            rf"[#\1](https://github.com/MarketSquare/{self.repo}/issues/\1)",
            s,
        )
        s = re.sub(
            r"[\s\(][0-9a-f]{7}[\s\)]",
            rf"[`\0`](https://github.com/MarketSquare/{self.repo}/issues/\0)",
            s,
        )
        return s

    def parse_type(self) -> CommitType:

        if (
            self.msg.startswith("docs: update .all-contributorsrc")
            or self.msg.startswith("docs: update README.md [skip ci]")
            # TODO: should these by type "skip" instead of type "ci"
        ):
            return "ci"
        elif self.msg.startswith("Bump "):
            return "bump"
        elif (
            self.msg.startswith("docs:")
            or self.msg.startswith("Docs:")
            or self.msg.startswith("Update README.md")
        ):
            return "docs"
        elif self.msg.startswith("Fix "):
            return "fix"

        return "unknown"

    @property
    def type(self) -> CommitType:
        type = self.parse_type()
        return type

    @property
    def labels(self) -> List[str]:

        return [""]

    def format(self) -> str:
        commit_link = commit_linkify(self.id, self.repo) if self.id else ""

        return f"{self.msg_processed}" + (f" ({commit_link})" if commit_link else "")


def run(cmd, cwd=".") -> str:
    p = _run(shlex.split(cmd), stdout=PIPE, stderr=STDOUT, encoding="utf8", cwd=cwd)
    if p.returncode != 0:
        print(p.stdout)
        print(p.stderr)
        raise Exception
    return p.stdout


def pr_linkify(prid: str, repo: str) -> str:
    return f"[#{prid}](https://github.com/MarketSquare/{repo}/pulls/{prid})"


def commit_linkify(commitid: str, repo: str) -> str:
    return f"[`{commitid}`](https://github.com/MarketSquare/{repo}/commit/{commitid})"


def wrap_details(title, body, wraplines=5):
    """Wrap lines into a <details> element if body is longer than `wraplines`"""
    out = f"\n\n### {title}"
    if body.count("\n") > wraplines:
        out += "\n<details><summary>Click to expand</summary>"
    out += f"\n<p>{body}\n</p>\n"
    if body.count("\n") > wraplines:
        out += "</details>"
    return out


def summary_repo(
    title: str, intro: str, path: str, commitrange: str, filter_types: List[str]
) -> str:
    dirname = run("bash -c 'basename $(pwd)'", cwd=path).strip()
    out = f"\n## {title}"
    out += intro

    feats = ""
    fixes = ""
    docs = ""
    unknown = ""

    summary_bundle = run(f"git log {commitrange} --oneline --no-decorate", cwd=path)
    for line in summary_bundle.split("\n"):
        if line:
            commit = Commit(
                id=line.split(" ")[0],
                msg=" ".join(line.split(" ")[1:]),
                repo=dirname,
                # Needed if we need to be able to figure out related PR / issue and labels
                # repo_data=repo,
            )

            entry = f"\n - {commit.format()}"
            if commit.type == "feat":
                feats += entry
            elif commit.type == "fix":
                fixes += entry
            elif commit.type == "docs":
                docs += entry
            elif commit.type not in filter_types:
                unknown += entry

    for name, entries in (
        ("✨ Features", feats),
        ("🐛 Fixes", fixes),
        ("📝 Docs", docs),
        ("🔨 Unknown / Misc", unknown),
    ):
        if entries:
            _count = len(entries.strip().split("\n"))
            title = f"{name} ({_count})"
            if _count > 5:
                out += wrap_details(title, entries)
            else:
                out += f"\n\n#### {title}"
                out += entries
        else:
            title = f"{name} (0)"
            out += f"\n\n#### {title}"

    return out


def generate_release_notes(
    title: str, intro: str, version: str, filter_types=["bump", "ci"]
):
    prev_release = run("git describe --tags --abbrev=0").strip()
    output = summary_repo(
        title,
        intro,
        ".",
        commitrange=f"{prev_release}...main",
        filter_types=filter_types,
    )
    return output


if __name__ == "__main__":
    print(generate_release_notes(sys.argv[1]))
