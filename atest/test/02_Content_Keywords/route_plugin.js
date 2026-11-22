async function addPluginRoute(matcher, page) {
    await page.route(matcher, (route) => route.fulfill({ status: 200, contentType: 'text/plain', body: 'plugin' }));
}

exports.__esModule = true;
exports.addPluginRoute = addPluginRoute;
