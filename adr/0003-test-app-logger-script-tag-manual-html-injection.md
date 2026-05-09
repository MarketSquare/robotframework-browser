# Logger script tag is injected by editing HTML files directly, not via Express middleware

The `<script src="/test-app-logger.js"></script>` tag is added manually to each of the ~35 static HTML files in `node/dynamic-test-app/static/`. It is not injected dynamically by an Express middleware that rewrites HTML responses.

## Considered Options

- **Manual HTML file edits (chosen):** Each HTML file is edited once. The injection is visible in source, auditable in git, and requires no runtime HTML rewriting.
- **Express middleware (rejected):** A middleware could intercept `text/html` responses and inject the script tag on the fly. This would avoid touching the HTML files but introduces invisible runtime behaviour — the served HTML differs from the source HTML. Debugging a test failure related to missing script injection would be harder because the source files look fine.

## Consequences

All ~35 static HTML files must include the tag explicitly. New HTML files added to `static/` must include it manually — this is documented in `node/dynamic-test-app/README.md`. The approach is explicit over clever.
