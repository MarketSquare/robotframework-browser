// A JS extension whose recorder hook the Recorder Hooks suite drives.
//
// __rewriteAction runs in the page, when the Action happens: the text filled
// into an element with data-record-text is recorded as that text; an element
// with data-record-by-text is recorded by its text, one with data-rewrite-to
// by that selector, and any other by Playwright's selector narrowed with >> nth=0.
// The hook is a named function: its name tells in the log which hook a line
// comes from.
exports.__rewriteAction = function recorderHooksSuite({ action, element }) {
  if (action.name === "fill" && element.hasAttribute("data-record-text")) {
    return { text: element.getAttribute("data-record-text") };
  }
  if (element.hasAttribute("data-record-by-text")) {
    return { selector: `text="${element.textContent.trim()}"` };
  }
  if (element.hasAttribute("data-rewrite-to")) {
    return { selector: element.getAttribute("data-rewrite-to") };
  }
  return { selector: `${action.selector} >> nth=0` };
};
