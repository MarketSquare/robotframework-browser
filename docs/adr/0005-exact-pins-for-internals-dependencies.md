# Dependencies whose internals we use are pinned exactly; the rest keep ranges

`robotframework-pythonlibcore` and `robotframework-assertion-engine` are declared with exact `==` pins in `pyproject.toml`, joining `grpcio`, `grpcio-tools` and `protobuf`, while `wrapt`, `overrides`, `click`, `seedir`, `psutil` and `PyYAML` keep `>=` ranges. The rule is **we pin exactly what we depend on the internals of, and we range what we only use the public API of** — not "shared leaves get ranges", which would argue for a range on PythonLibCore, the most widely shared leaf in the Robot Framework library ecosystem. Browser reads `HybridCore.attributes` (`robotlibcore/core/hybrid.py`), a PythonLibCore internal with no public-API guarantee, and `AssertionOperator`'s member list appears verbatim in error messages the test suite asserts on; a minor release of either package can change those without breaking any promise it made.

In the same change the `robotframework` floor was raised from `>= 6.1.1` to `>= 7.1.1` — the oldest version the CI matrix in `.github/workflows/on-push.yml` actually runs — so that the declared floor is a statement about what is verified rather than about what happens not to have broken yet.

## Considered Options

- **Exact pins (chosen).** Converts a silent semantic break in a dependency's internals into a resolver error at install time. Co-installation with other Robot Framework libraries survives in practice because those libraries declare `>=` floors on PythonLibCore, which an exact pin inside that range satisfies; it only hard-fails against a library that pins a *different* exact version.
- **Floor raise plus a runtime assertion.** Keep `>= 4.5.0, < 5.0.0` and have the library check at construction that `self.attributes` exists, failing loudly otherwise. Rejected: an assertion catches removal but not the case that actually matters — `attributes` still existing while no longer holding every keyword.
- **`~= 4.5` (patch-level freedom).** Rejected as neither one thing nor the other: it still blocks co-installation against a conflicting exact pin, while leaving the internals free to move in the releases it does allow.

## Consequences

Dependabot watches the `pip` ecosystem at `/` daily and these two pins sit outside the `grpc` group, so each gets its own update PR — which is the intent. But such a PR is only as safe as the tests covering the internal the pin exists to protect, and until the Python-usage test suite lands there are none: a green CI run on a `robotframework-pythonlibcore` bump says nothing about whether `attributes` still behaves as assumed. Review those two PRs against the upstream diff, not against CI.

The upper bound `robotframework < 9.0.0` is deliberately looser than the tested range (7.1.1 and 7.4.2) and is *not* being tightened to match the floor's honesty. The two ends fail differently: a too-generous ceiling fails soft — an RF 8 user installs and may hit a bug fixable in a patch release — while a too-tight ceiling fails hard, locking every user out on the day RF 8 ships until a Browser release is cut. For the same reason there is no import-time Robot Framework version check: the package manager is the right place to enforce the floor, and a user who deliberately overrides the resolver owns the outcome — if it happens to work for them, nothing here should stop it.

Both changes are backwards incompatible and belong in a major release.
