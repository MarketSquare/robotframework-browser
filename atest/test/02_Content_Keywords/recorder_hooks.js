// A JS extension whose recorder hooks the Recorder Hooks suite drives: a select
// is recorded by the labels of its options, and a pick is narrowed to the first
// element it finds.

exports.__recordedAction = async ({ action, page }) => {
  if (action.name === "pick") {
    return { ...action, selector: `${action.selector} >> nth=0` };
  }
  if (action.name !== "select") return undefined;
  const labels = await page
    .locator(action.selector)
    .evaluate(
      (select, values) =>
        values.map(
          (value) =>
            [...select.options].find((option) => option.value === value).label,
        ),
      action.options,
    );
  return { ...action, options: labels.map((label) => ({ label })) };
};
