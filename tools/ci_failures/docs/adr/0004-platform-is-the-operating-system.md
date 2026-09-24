# A Leg's Platform is its operating system, and nothing finer

`leg.platform` held two kinds of value in one column. Legs from before 2026-09-04 carry the
`sys.platform` that Robot Framework's generator line gives (`linux`, `win32`, `darwin`), and
later ones the `platform.platform()` string the suite has recorded since then. Counted by that
column, one runner read as up to five platforms, and every per-Configuration rate, every
Inconclusive Zero and the per-leg summary were split along lines that are not machines.

The full string turned out to carry nothing a Configuration does not already. Measured over the
750 Legs that have it: one value across every Linux Leg. On Windows, `Windows-10-…` against
`Windows-2025Server-…` on the same build, `10.0.26100`, decided entirely by the Python version,
which is already its own part of the Configuration. On macOS, a `-Mach-O` suffix that is
Python 3.14 again, and a runner image update (26.5.2 to 26.6.2), which is a date and which each
Occurrence already carries. So the **Platform** is the operating system alone, read from the
start of the full string, and the full string is kept as the **OS Release**. It is detail on an
Occurrence, where "it began with the image update" is a real kind of answer, and is never
counted by.

The processor architecture is deliberately left out. The `testing` Legs never vary it (x86_64
Linux, arm64 macOS), and Legs before 2026-09-04 did not record it, so adding it would either
leave three thousand Legs unknown or hard-code which architecture each operating system
"usually" has. Only two scheduled BrowserBatteries runners vary it (`macos-15-intel`,
`ubuntu-24.04-arm`), which is too few Runs to carry a rate. The Leg's name still shows the
runner, and if they ever build up a rate, the architecture can be read out of the stored OS
Release without downloading anything.
