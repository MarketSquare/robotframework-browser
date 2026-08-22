"""Proof of concept: which CI tests fail, how often, and with which error.

Deliberately small. Everything in the database comes from `output.xml`, except
the link back to the GitHub artifact, which cannot be in `output.xml` because the
artifact is uploaded after it is written. Anything else worth looking at -
screenshots, the Playwright log - is fetched from that link when a specific
failure is worth a closer look.

Not part of the Browser library. See `0012_flaky_test_analysis.md`.
"""
