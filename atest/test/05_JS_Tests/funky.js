async function myFunkyKeyword(page, args, logger) {
    const h = await page.locator(args[0]);
    logger("Logging something funky");
    return await h.evaluate((e) => e.textContent = "Funk yeah!");
}

async function myNewStyleFunkyKeyword(selector, page, logger) {
    const h = await page.$(selector);
    logger("Logging something funky here");
    return await h.evaluate((e) => e.textContent = "Funk yeah again!");
}

let browserServer;

async function createRemoteBrowser(logger, playwright) {
    logger("Launching chromium server");
    browserServer = await playwright.chromium.launchServer({headless: false});
    logger("Returning server address");
    return browserServer.wsEndpoint();
}

async function withDefaultValue(a = "default") {
    return a.toUpperCase();
}
withDefaultValue.rfdoc = "This function returns the default value if no argument is passed";

async function closeRemoteBrowser() {
    return browserServer.kill();
}

function crashKeyword() {
    throw Error("Crash");
}

async function moreDefaults(bTrue = true,
                            bFalse = false,
                            integer = 123,
                            floater = 1.3,
                            text = "hello",
                            nothing = null,
                            undefineder = undefined) {
    return {
        bTrue,
        bFalse,
        integer,
        floater,
        text,
        nothing,
        "undefineder": undefineder || null
    };
}

async function contextAndBrowserDemo(message, context, browser, logger) {
    logger(`Message: ${message}`);
    logger(`Browser: ${browser}`);
    logger(`Context: ${context}`)
    const pages = context.pages();
    logger(`Number of pages in context: ${pages.length}`);
    return {
        message,
        browserType: browser?.browserType().name() ?? "NO BROWSER",
        pageCount: pages.length
    };
}

exports.__esModule = true;
exports.myFunkyKeyword = myFunkyKeyword;
exports.createRemoteBrowser = createRemoteBrowser;
exports.closeRemoteBrowser = closeRemoteBrowser;
exports.crashKeyword = crashKeyword;
exports.withDefaultValue = withDefaultValue;
exports.moreDefaults = moreDefaults;
exports.myNewStyleFunkyKeyword = myNewStyleFunkyKeyword;
exports.contextAndBrowserDemo = contextAndBrowserDemo;