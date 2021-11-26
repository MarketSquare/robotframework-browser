#!/usr/bin/python3
"""
Script that outputs a changelog for the repository in the current directory and its submodules.

Manual actions needed to clean up for changelog:
    - Remove commits that are not meaningful for end users.
"""

import shlex
import re
from typing import Optional, Tuple, List
from subprocess import run as _run, STDOUT, PIPE
from dataclasses import dataclass


class CommitMsg:
    type: str
    subtype: str
    msg: str


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
            r"[^(-]https://github.com/MarketSquare/([\-\w\d]+)/(issues|pulls)/(\d+)",
            r"[#\3](https://github.com/MarketSquare/\1/issues/\3)",
            s,
        )
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

    def parse_type(self) -> Optional[Tuple[str, str]]:
        # Needs to handle '!' indicating breaking change

        if self.msg.startswith(
            "docs: update .all-contributorsrc"
        ) or self.msg.startswith("docs: update README.md [skip ci]"):
            return "ci", ""
        elif self.msg.startswith("Bump "):
            return "bump", ""
        elif self.msg.startswith("docs:"):
            return "docs", ""
        elif self.msg.startswith("Fix "):
            return "fix", ""

        return None

    @property
    def type(self) -> Optional[str]:
        type, _ = self.parse_type() or (None, None)
        return type

    @property
    def subtype(self) -> Optional[str]:
        _, subtype = self.parse_type() or (None, None)
        return subtype

    def type_str(self) -> str:
        type, subtype = self.parse_type() or (None, None)
        return f"{type}" + (f"({subtype})" if subtype else "")

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


def summary_repo(path: str, commitrange: str, filter_types: List[str]) -> str:
    if commitrange.endswith("0000000"):
        # Happens when a submodule has been removed
        return ""
    dirname = run("bash -c 'basename $(pwd)'", cwd=path).strip()
    out = f"\n## {dirname}"

    feats = ""
    fixes = ""
    docs = ""
    misc = ""

    summary_bundle = run(f"git log {commitrange} --oneline --no-decorate", cwd=path)
    for line in summary_bundle.split("\n"):
        if line:
            commit = Commit(
                id=line.split(" ")[0],
                msg=" ".join(line.split(" ")[1:]),
                repo=dirname,
            )

            entry = f"\n - {commit.format()}"
            if commit.type == "feat":
                feats += entry
            elif commit.type == "fix":
                fixes += entry
            elif commit.type == "docs":
                docs += entry
            elif commit.type not in filter_types:
                misc += entry

    for name, entries in (
        ("✨ Features", feats),
        ("🐛 Fixes", fixes),
        ("📝 Docs", docs),
        ("🔨 Misc", misc),
    ):
        if entries:
            _count = len(entries.strip().split("\n"))
            title = f"{name} ({_count})"
            if "Misc" in name or "Fixes" in name:
                out += wrap_details(title, entries)
            else:
                out += f"\n\n#### {title}"
                out += entries
        else:
            title = f"{name} (0)"
            out += f"\n\n#### {title}"

    return out


def generate_release_notes(filter_types=["bump", "ci"]):
    # FIXME: figure this out dynamically
    prev_release = run("git describe --tags --abbrev=0").strip()
    # prev_release = "v10.0.3"
    next_release = "main"
    output = summary_repo(
        ".", commitrange=f"{prev_release}...{next_release}", filter_types=filter_types
    )
    print(output)


if __name__ == "__main__":
    generate_release_notes()
