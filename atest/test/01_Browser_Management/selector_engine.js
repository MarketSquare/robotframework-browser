// Registers `cdp-tag=<css>`, a selector engine that finds elements by CSS, to
// check that a context attached over CDP gets the engines registered before.

async function registerTagEngine(playwright) {
  try {
    await playwright.selectors.register("cdp-tag", {
      content: `({
        query: (root, body) => root.querySelector(body),
        queryAll: (root, body) => [...root.querySelectorAll(body)],
      })`,
    });
  } catch (error) {
    // One Node process serves every suite, so a second suite finds it there.
    if (!String(error).includes("already registered")) throw error;
  }
}
registerTagEngine.rfdoc =
  "Registers the `cdp-tag` selector engine, which finds elements by CSS.";
exports.registerTagEngine = registerTagEngine;
