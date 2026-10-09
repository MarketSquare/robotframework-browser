"""How often one pabot worker disposes another worker's highlights.

Throwaway. Reads a playwright-log.txt from any pabot run and counts, for every
highlight added with no timeout, whether some *other* test's `disposeAll` landed
before its owner's did. That is the window in which a screenshot comes out
undecorated, which is the whole of the `Screenshot On Failure` flake.

    python measure_highlight_theft.py atest/output/playwright-log.txt

Caveat worth keeping in mind while reading the number: the `test_name` stamped
on each line comes from a module-global context on the node side, which is
itself known to misattribute across workers (see 0012 section 11). It is good
enough to separate "my dispose" from "someone else's" in bulk and not good
enough to trust line by line.
"""

import json
import sys
from pathlib import Path


def events(log: Path):
    """Highlight adds and disposes, in the order the node process saw them."""
    found = []
    with log.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if "ighlight" not in line:
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            message = entry.get("msg", "")
            if "Adding highlight to cache" in message:
                kind = "ADD"
            elif "Dispose all highlights" in message:
                kind = "DISPOSE"
            else:
                continue
            found.append(
                {
                    "seq": entry.get("seq") or 0,
                    "time": entry.get("time"),
                    "test": entry.get("test_name") or "",
                    "kind": kind,
                }
            )
    found.sort(key=lambda e: e["seq"])
    return found


def stolen(found):
    """Every highlight a different test disposed before its owner could."""
    losses = []
    for index, event in enumerate(found):
        if event["kind"] != "ADD":
            continue
        for later in found[index + 1 :]:
            if later["kind"] != "DISPOSE":
                continue
            if later["test"] == event["test"]:
                break  # its owner got there first, as intended
            losses.append((event, later))
            break
    return losses


EXPECTED_ARGUMENTS = 2


def main() -> int:
    if len(sys.argv) != EXPECTED_ARGUMENTS:
        print(__doc__)
        return 2
    log = Path(sys.argv[1])
    found = events(log)
    adds = [e for e in found if e["kind"] == "ADD"]
    losses = stolen(found)
    for owner, thief in losses:
        print(
            f"{owner['time']} -> {thief['time']}  "
            f"{owner['test'][-60:]}  disposed by  {(thief['test'] or '(unstamped)')[-60:]}"
        )
    if not adds:
        print(f"No highlights in {log}. Was this a pabot run with debug logging on?")
        return 1
    share = len(losses) / len(adds)
    print(
        f"\n{len(losses)} of {len(adds)} highlights ({share:.0%}) were disposed by a "
        f"different test before their owner disposed them."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
