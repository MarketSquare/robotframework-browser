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

async function adoptedContextIsClosed() {
    return adoptedContextClosed;
}

async function adoptedContextOnCloseWasCalled() {
    return onCloseCalled;
}

exports.__esModule = true;
exports.openAdoptedPersistentContext = openAdoptedPersistentContext;
exports.adoptedContextIsClosed = adoptedContextIsClosed;
exports.adoptedContextOnCloseWasCalled = adoptedContextOnCloseWasCalled;
