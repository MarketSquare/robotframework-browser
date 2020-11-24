async function myFunkyKeyword(page, args) {
    const h = await page.$(args[0]);
    return await h.evaluate((e) => e.textContent = "Funk yeah!");
}

exports.__esModule = true;
exports.myFunkyKeyword = myFunkyKeyword;