import { sendUnaryData, status, Metadata } from 'grpc';
import { Page, errors } from 'playwright';

export async function waitUntilElementExists<T>(page: Page | undefined, callback: sendUnaryData<T>, selector: string) {
    await invokeOnPageWithSelector(page, callback, 'waitForSelector', selector, { state: 'attached' });
}

export async function invokeOnPage(page: Page | undefined, callback: any, methodName: string, ...args: any[]) {
    exists(page, callback, `Tried to do playwright action '${methodName}', but no open page.`);
    const fn: any = (page as { [key: string]: any })[methodName].bind(page);
    try {
        return await fn(...args);
    } catch (e) {
        console.log(`Error invoking Playwright action '${methodName}': ${e}`);
        callback(e, null);
    }
}

/**
 * Resolve the playwright method on page or frame and invoke it.
 * With a normal selector, invokes the `methodName` on the given `page`.
 * If the selector is a frame piercing selector, first find the corresponding
 * frame on the `page`, and then invoke the `methodName` on the resolved frame.
 *
 * @param page Existing Playwright Page object.
 * @param callback GRPC callback to make response.
 * @param methodName Which Playwright method to invoke.
 * @param selector Selector of the element to operate on,
 *  or a frame piercing selector in format `<frame selector> >>> <element selector>
 * @param args Additional args to the Playwirght method.
 */
export async function invokeOnPageWithSelector<T>(
    page: Page | undefined,
    callback: sendUnaryData<T>,
    methodName: string,
    selector: string,
    ...args: any[]
) {
    exists(page, callback, `Tried to do playwright action '${methodName}', but no open browser.`);
    const { elementSelector, fn } = await determineFunctionAndSelector(page, methodName, selector, callback);
    try {
        return await fn(elementSelector, ...args);
    } catch (e) {
        if (e instanceof errors.TimeoutError) {
            const errorMetadata = new Metadata();
            errorMetadata.add('reason', `Could not find element with selector \`${selector}\` within timeout.`);
            callback(
                {
                    code: status.INVALID_ARGUMENT,
                    name: e.name,
                    message: '',
                    details: `Error invoking Playwright action ${methodName}:\n${e.toString()}`,
                    metadata: errorMetadata,
                },
                null,
            );
        }
    }
}

async function determineFunctionAndSelector<T>(
    page: Page,
    methodName: string,
    selector: string,
    callback: sendUnaryData<T>,
) {
    if (isFramePiercingSelector(selector)) {
        const { frameSelector, elementSelector } = splitFrameAndElementSelector(selector);
        const frame = await findFrame(page, frameSelector, callback);
        const fn = (frame as { [key: string]: any })[methodName].bind(frame);
        return { elementSelector, fn };
    } else {
        return { elementSelector: selector, fn: (page as { [key: string]: any })[methodName].bind(page) };
    }
}

function isFramePiercingSelector(selector: string) {
    return selector.match('>>>');
}

function splitFrameAndElementSelector(selector: string) {
    const parts = selector.split('>>>');
    return {
        frameSelector: parts[0].trim(),
        elementSelector: parts[1].trim(),
    };
}

async function findFrame<T>(page: Page, frameSelector: string, callback: sendUnaryData<T>) {
    const frameHandle = await page.$(frameSelector);
    exists(frameHandle, callback, `Could not find frame with selector ${frameSelector}`);
    return await frameHandle.contentFrame();
}

// This is necessary for improved typescript inference
/*
 * If obj is not trueish call callback with new Error containing message
 */
export function exists<T1, T2>(obj: T1, callback: sendUnaryData<T2>, message: string): asserts obj is NonNullable<T1> {
    if (!obj) {
        callback(new Error(message), null);
    }
}
