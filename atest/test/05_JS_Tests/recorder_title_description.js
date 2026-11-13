// A JS extension that uses the recorder hooks of Record Keyword(s): a click on
// an element whose title equals its text and is unique on the page is recorded
// as `role=<role>[description="<title>"s]` instead of by its name.
//
// The recorded Action carries only Playwright's selector, so the page reports
// each press on such an element (`__titledPress`) when it happens, and
// `__recordedSelector` matches the click to it by the element's label.

const MAX_PRESSES = 10;
const PRESS_MS = 10000;
const TEXT_LIMIT = 1000;
const presses = new WeakMap();

// Runs in the page. Presses on Browser's toolbar and Playwright's overlay, both
// inside an `x-pw-glass` element, are skipped.
function reportTitledPresses() {
  if (window.top !== window || window.__titledPressInstalled) return;
  window.__titledPressInstalled = true;
  const flat = (text) => (text || "").replace(/\s+/g, " ").trim();
  const titled = (scope, title, found = []) => {
    for (const element of scope.querySelectorAll("*")) {
      if (
        element.hasAttribute("title") &&
        flat(element.getAttribute("title")) === title
      )
        found.push(element);
      if (element.shadowRoot) titled(element.shadowRoot, title, found);
    }
    return found;
  };
  const label = (element) => {
    const root = element.getRootNode();
    const labelledBy = (element.getAttribute("aria-labelledby") || "")
      .split(/\s+/)
      .map((id) => id && root.getElementById && root.getElementById(id))
      .filter(Boolean)
      .map((ref) => ref.textContent)
      .join(" ");
    return (
      flat(labelledBy) ||
      flat(element.getAttribute("aria-label")) ||
      flat(element.textContent)
    );
  };
  window.addEventListener(
    "pointerdown",
    (event) => {
      const path = event
        .composedPath()
        .filter((node) => node instanceof Element);
      if (
        !event.isTrusted ||
        path.some((element) => element.localName === "x-pw-glass")
      )
        return;
      const element =
        path.find((e) => e.matches("button, a, [role=button], [role=link]")) ||
        path[0];
      if (
        !element ||
        element.hasAttribute("aria-describedby") ||
        element.hasAttribute("aria-description")
      )
        return;
      const title = flat(element.getAttribute("title"));
      if (!title || title !== flat(element.textContent)) return;
      const matches = titled(document, title);
      if (matches.length !== 1 || matches[0] !== element) return;
      window.__titledPress({ title, label: label(element) || title });
    },
    true,
  );
}

exports.__recordingStarted = async ({ context }) => {
  const list = [];
  presses.set(context, list);
  await context.exposeBinding("__titledPress", ({ page }, press) => {
    const { title, label } = press || {};
    if (typeof title !== "string" || typeof label !== "string") return;
    if (!title || title.length > TEXT_LIMIT || label.length > TEXT_LIMIT)
      return;
    list.push({ page, title, label, at: Date.now() });
    if (list.length > MAX_PRESSES) list.shift();
  });
  await context.addInitScript(reportTitledPresses);
  for (const page of context.pages())
    await page.evaluate(reportTitledPresses).catch(() => undefined);
};

// Playwright's whole selector for a named element, with the description or
// `>> nth=N` it adds when the name is not unique.
const NAMED_ROLE =
  /^internal:role=([a-z]+)\[name=("(?:[^"\\]|\\.)*")([is])\](?:\[description="(?:[^"\\]|\\.)*"[is]\])?(?: >> nth=\d+)?$/;

exports.__recordedSelector = ({ selector, action, page, context }) => {
  // A pick has no Action; only a click has a press to match.
  if (!action || action.name !== "click") return undefined;
  const match = NAMED_ROLE.exec(selector);
  if (!match) return undefined;
  const [, role, quoted, flag] = match;
  const name = JSON.parse(quoted);
  const named = (label) =>
    flag === "s"
      ? label === name
      : label.toLowerCase().includes(name.toLowerCase());
  const now = Date.now();
  const press = [...(presses.get(context) || [])]
    .reverse()
    .find((p) => p.page === page && now - p.at <= PRESS_MS && named(p.label));
  if (!press) return undefined;
  return `role=${role}[description="${press.title.replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"s]`;
};
