async function mouseWheel(x, y, logger, page) {
    logger(`Mouse wheel at ${x}, ${y}`);
    await page.mouse.wheel(x, y);
    logger("Returning a funny string");
    return await page.evaluate("document.scrollingElement.scrollTop");
}

async function getLargePayload() {
    return {
        prefix: "chunk-prefix",
        payload: "\u20AC".repeat(350000),
        suffix: "chunk-suffix",
    };
}

exports.__esModule = true;
exports.mouseWheel = mouseWheel;
exports.getLargePayload = getLargePayload;
