"""Which CI tests fail, how often, and with which error.

Everything in the database comes from `output.xml`, except the link back to the
GitHub artifact, which cannot be in `output.xml` because the artifact is uploaded
after it is written. Anything else worth looking at - screenshots, the Playwright
log - is fetched from that link when a specific failure is worth a closer look.

A maintainers' tool, excluded from the wheel and not part of the Browser library.
See `README.md` for how to run it and `CONTEXT.md` for what the words mean.
"""
