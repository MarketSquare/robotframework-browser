async function mouseWheelAsPlugin(x, y, logger, page) {
    logger(`Mouse wheel at ${x}, ${y}`);
    await page.mouse.wheel(x, y);
    logger("Returning a funny string");
    return await page.evaluate("document.scrollingElement.scrollTop");
}

exports.__esModule = true;
exports.mouseWheelAsPlugin = mouseWheelAsPlugin;
