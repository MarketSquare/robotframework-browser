async function myFunkyKeyword(page, args, logger) {
    const h = await page.$(args[0]);
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

exports.__esModule = true;
exports.myFunkyKeyword = myFunkyKeyword;
exports.createRemoteBrowser = createRemoteBrowser;
exports.closeRemoteBrowser = closeRemoteBrowser;
exports.crashKeyword = crashKeyword;
exports.withDefaultValue = withDefaultValue;
exports.myNewStyleFunkyKeyword = myNewStyleFunkyKeyword;
