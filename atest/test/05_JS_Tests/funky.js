async function myFunkyKeyword(page, args, logger) {
    const h = await page.$(args[0]);
    logger("Logging something funky");
    return await h.evaluate((e) => e.textContent = "Funk yeah!");
}

let browserServer;

async function createRemoteBrowser(page, args, logger, playwright) {
    logger("Launching chromium server");
    browserServer = await playwright.chromium.launchServer({headless: false});
    logger("Returning server address");
    return browserServer.wsEndpoint();
}

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
