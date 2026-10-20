let adoptedContextClosed = false;
let onCloseCalled = false;

async function openAdoptedPersistentContext(userDataDir, url, headless, playwright, adoptContext) {
    const context = await playwright.chromium.launchPersistentContext(userDataDir, {
        headless: String(headless).toLowerCase() !== 'false',
    });
    context.on('close', () => (adoptedContextClosed = true));
    await context.pages()[0].goto(url);
    return adoptContext(context, {
        onClose: async () => {
            onCloseCalled = true;
        },
    });
}

async function openAdoptedPersistentContextWithTracingAndDownloads(userDataDir, url, headless, tracing, playwright, adoptContext) {
    const contextOptions = { acceptDownloads: true };
    const context = await playwright.chromium.launchPersistentContext(userDataDir, {
        headless: String(headless).toLowerCase() !== 'false',
        ...contextOptions,
    });
    await context.pages()[0].goto(url);
    return adoptContext(context, { tracing, contextOptions });
}

async function messageOfAFailedWait(page) {
    try {
        await page.waitForSelector('#not-on-the-page');
    } catch (error) {
        return error.message;
    }
    return '';
}

async function adoptedContextIsClosed() {
    return adoptedContextClosed;
}

async function adoptedContextOnCloseWasCalled() {
    return onCloseCalled;
}

async function openAdoptedPersistentContextWithRecording(userDataDir, url, headless, viewport, tracing, recordVideo, tracesDir, playwright, adoptContext) {
    const contextOptions = viewport ? { viewport, recordVideo } : { recordVideo };
    const context = await playwright.chromium.launchPersistentContext(userDataDir, {
        headless: String(headless).toLowerCase() !== 'false',
        tracesDir,
        ...contextOptions,
    });
    await context.pages()[0].goto(url);
    return adoptContext(context, { tracing, contextOptions });
}

exports.__esModule = true;
exports.openAdoptedPersistentContext = openAdoptedPersistentContext;
exports.openAdoptedPersistentContextWithTracingAndDownloads = openAdoptedPersistentContextWithTracingAndDownloads;
exports.messageOfAFailedWait = messageOfAFailedWait;
exports.adoptedContextIsClosed = adoptedContextIsClosed;
exports.adoptedContextOnCloseWasCalled = adoptedContextOnCloseWasCalled;
exports.openAdoptedPersistentContextWithRecording = openAdoptedPersistentContextWithRecording;
