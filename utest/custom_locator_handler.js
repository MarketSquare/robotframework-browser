async function customLocatorHandler(locator, clickLocator, page) {
    console.log("Adding custom locator handler for: " + locator);
    const pageLocator = page.locator(locator).first();
    await page.addLocatorHandler(
        pageLocator,
        async () => {
            console.log("Handling custom locator: " + clickLocator);
            await page.locator(clickLocator).click();
            // Return the element that was clicked
        }
    );
}
exports.__esModule = true;
exports.customLocatorHandler = customLocatorHandler;
