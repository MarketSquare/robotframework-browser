const playwright = require('playwright');

async function myFunkyKeyword(page, args) {
    const h = await page.$(args[0]);
    return await h.evaluate((e) => e.textContent = "Funk yeah!");
}

let browserServer;

async function createRemoteBrowser(page, args) {
    browserServer = await playwright.chromium.launchServer({headless: false});
    return browserServer.wsEndpoint();
}

async function closeRemoteBrowser() {
    return browserServer.kill();
}

exports.__esModule = true;
exports.myFunkyKeyword = myFunkyKeyword;
exports.createRemoteBrowser = createRemoteBrowser;
exports.closeRemoteBrowser = closeRemoteBrowser;