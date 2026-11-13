// A JS extension that uses the recorder hook of Record Keyword(s) and Record
// Selector to record an element with an explicit `role` and `aria-label` by
// both, instead of by its id or CSS.
//
// SAP Fiori gives every input field a value help icon,
// `<span role="button" aria-label="Wertehilfe einblenden">`, so the name alone
// is rarely unique and Playwright falls back to the generated id
// `#APD_\:\:SalesOrderType-inner-vhi`. The extension records it instead by
//
// - its role and aria-label, when that finds only it:
//   `internal:role=button[name="Wertehilfe einblenden"s]`;
// - otherwise the one named form control that sits next to it, such as the
//   input the value help belongs to:
//   `internal:role=combobox[name="Kundenauftragsart"s] >> xpath=.. >>
//   internal:role=button[name="Wertehilfe einblenden"s]`;
// - otherwise its role and aria-label with an `nth=`.
//
// The hook runs after the click, when the value help dialog may already hide
// the form behind it with `aria-hidden`. The selectors are therefore checked
// with `include-hidden`, and the control's name is read from the DOM. A
// selector is used only when it finds the recorded element. Why the extension
// keeps Playwright's selector is logged in playwright-log.txt.

const TIMEOUT_MS = 500;
const ENTER_FRAME = "internal:control=enter-frame";
const CONTROLS =
  "input:not([type=hidden]), textarea, select, [role=combobox], " +
  "[role=textbox], [role=searchbox], [role=spinbutton]";

const join = (parts) => parts.join(" >> ");
const roleSelector = ({ role, name }, hidden = false) =>
  `internal:role=${role}${hidden ? "[include-hidden=true]" : ""}` +
  `[name=${JSON.stringify(name)}s]`;
const parentSelector = (levels) =>
  levels === 1 ? "xpath=.." : `xpath=ancestor::*[${levels}]`;
const log = (message) => console.log(`recorder_aria_label: ${message}`);

// Runs in the page: the role and aria-label of `element`, and the role and
// name of the closest form control beside it. The neighbour is found in the
// closest ancestor that holds exactly one control besides `element`, with how
// many `levels` that ancestor is above the control.
function describe(element, controls) {
  const flat = (text) => (text || "").replace(/\s+/g, " ").trim();
  const explicitRole = (e) =>
    (e.getAttribute("role") || "").trim().split(/\s+/)[0];
  const roleOf = (e) => {
    if (explicitRole(e)) return explicitRole(e);
    if (e.localName === "select") return e.multiple ? "listbox" : "combobox";
    if (e.localName === "textarea") return "textbox";
    const type = (e.getAttribute("type") || "text").toLowerCase();
    if (type === "number") return "spinbutton";
    if (type === "search")
      return e.hasAttribute("list") ? "combobox" : "searchbox";
    return e.hasAttribute("list") ? "combobox" : "textbox";
  };
  const nameOf = (e) => {
    const root = e.getRootNode();
    const labelledBy = (e.getAttribute("aria-labelledby") || "")
      .split(/\s+/)
      .map((id) => id && root.getElementById && root.getElementById(id))
      .filter(Boolean)
      .map(
        (ref) => flat(ref.getAttribute("aria-label")) || flat(ref.textContent),
      )
      .join(" ");
    return (
      flat(labelledBy) ||
      flat(e.getAttribute("aria-label")) ||
      flat([...(e.labels || [])].map((label) => label.textContent).join(" "))
    );
  };

  const own = {
    role: explicitRole(element),
    name: flat(element.getAttribute("aria-label")),
  };
  if (!own.role || !own.name || element.hasAttribute("aria-labelledby"))
    return null;
  for (
    let ancestor = element.parentElement;
    ancestor && ancestor !== element.ownerDocument.body;
    ancestor = ancestor.parentElement
  ) {
    const found = [...ancestor.querySelectorAll(controls)].filter(
      (control) => control !== element && !control.contains(element),
    );
    if (found.length > 1) break;
    if (found.length === 1) {
      const control = found[0];
      let levels = 0;
      for (let e = control; e !== ancestor; e = e.parentElement) levels++;
      const name = nameOf(control);
      return {
        own,
        neighbour: name ? { role: roleOf(control), name, levels } : null,
      };
    }
  }
  return { own, neighbour: null };
}

// How many elements `selector` finds, and the index of `element` among them.
async function matchOf(page, selector, element) {
  const [count, index] = await page
    .locator(selector)
    .evaluateAll(
      (found, target) => [found.length, found.indexOf(target)],
      element,
    );
  return { count, index };
}

async function rewrite(page, selector) {
  const parts = selector.split(" >> ");
  const frames = parts.slice(0, parts.lastIndexOf(ENTER_FRAME) + 1);
  const last = parts.at(-1);
  if (last.startsWith("internal:role=") && last.includes("[name="))
    return undefined;
  const recorded = page.locator(selector);
  const found = await recorded.count();
  if (found !== 1) {
    log(`${selector} finds ${found} elements, kept`);
    return undefined;
  }
  const element = await recorded.elementHandle({ timeout: TIMEOUT_MS });
  try {
    const described = await element.evaluate(describe, CONTROLS);
    if (!described) return undefined;
    const { own, neighbour } = described;
    // Each candidate as it is recorded and as it is checked now.
    const check = async (build) => {
      const match = await matchOf(page, join(build(true)), element);
      return { ...match, selector: join(build(false)) };
    };

    const alone = await check((hidden) => [
      ...frames,
      roleSelector(own, hidden),
    ]);
    if (alone.index === -1) {
      log(
        `${roleSelector(own)} does not find the element of ${selector}, kept`,
      );
      return undefined;
    }
    if (alone.count === 1) return alone.selector;

    if (neighbour) {
      const scoped = await check((hidden) => [
        ...frames,
        roleSelector(neighbour, hidden),
        parentSelector(neighbour.levels),
        roleSelector(own, hidden),
      ]);
      if (scoped.count === 1 && scoped.index === 0) return scoped.selector;
      log(`${scoped.selector} finds ${scoped.count} elements, using nth=`);
    }
    return `${alone.selector} >> nth=${alone.index}`;
  } finally {
    await element.dispose();
  }
}

// Every recorded Action and every pick. A failure keeps Playwright's selector.
exports.__recordedSelector = ({ selector, page }) =>
  rewrite(page, selector).catch((error) => {
    log(`${selector} kept: ${error}`);
    return undefined;
  });
