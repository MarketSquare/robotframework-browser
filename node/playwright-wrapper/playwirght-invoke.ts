import { sendUnaryData, status, Metadata } from 'grpc';
import { Page, errors, ElementHandle } from 'playwright';

import { PlaywrightState } from './playwright-state';

export async function waitUntilElementExists<T>(
    state: PlaywrightState,
    callback: sendUnaryData<T>,
    selector: string,
): Promise<ElementHandle> {
    const { elementSelector, context } = await determineFunctionAndSelector(state, selector, callback);
    exists(context, callback, '');
    if ('waitForSelector' in context) {
        try {
            await context.waitForSelector(elementSelector, { state: 'attached' });
        } catch (e) {
            callback(getErrorDetails(e, selector, 'waitForSelector'), null);
        }
    }
    const element = await context.$(elementSelector);
    exists(element, callback, `Could not find element with selector \`${elementSelector}\` within timeout.`);
    return element;
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
 * Resolve the playwright method on page, frame or elementHandle and invoke it.
 * With a normal selector, invokes the `methodName` on the given `page`.
 * If the selector is a frame piercing selector, first find the corresponding
 * frame on the `page`, and then invoke the `methodName` on the resolved frame.
 * If the selector is an elementHandle selector, first resolve the corresponding e
 * elementHandle, and invoke the method on it.
 *
 * @param state A reference to current PlaywrightState object.
 * @param callback GRPC callback to make response.
 * @param methodName Which Playwright method to invoke.
 * @param selector Selector of the element to operate on,
 *  or a frame piercing selector in format `<frame selector> >>> <element selector>
 * @param args Additional args to the Playwirght method.
 */

export async function invokePlaywirghtMethod<T>(
    state: PlaywrightState,
    callback: sendUnaryData<T>,
    methodName: string,
    selector: string,
    ...args: any[]
) {
    const { elementSelector, context } = await determineFunctionAndSelector(state, selector, callback);
    try {
        const fn = (context as { [key: string]: any })[methodName].bind(context);
        return await fn(elementSelector, ...args);
    } catch (e) {
        callback(getErrorDetails(e, selector, methodName), null);
    }
}

async function determineFunctionAndSelector<T>(state: PlaywrightState, selector: string, callback: sendUnaryData<T>) {
    const page = state.getActivePage();
    exists(page, callback, `Tried to do playwright action, but no open browser.`);
    if (isFramePiercingSelector(selector)) {
        const { frameSelector, elementSelector } = splitFrameAndElementSelector(selector);
        const frame = await findFrame(page, frameSelector, callback);
        return { elementSelector, context: frame };
    } else if (isElementHandleSelector(selector)) {
        const { elementHandleId, elementSelector } = splitElementHandleAndElementSelector(selector, callback);
        try {
            return { elementSelector, context: state.getElement(elementHandleId) };
        } catch (e) {
            callback(e, null);
        }
        return {
            elementSelector: '',
            context: null,
        };
    } else {
        return { elementSelector: selector, context: page };
    }
}

function isFramePiercingSelector(selector: string) {
    return selector.match('>>>');
}

function isElementHandleSelector(selector: string) {
    return selector.startsWith('element=');
}

function splitFrameAndElementSelector(selector: string) {
    const parts = selector.split('>>>');
    return {
        frameSelector: parts[0].trim(),
        elementSelector: parts[1].trim(),
    };
}

function splitElementHandleAndElementSelector<T>(selector: string, callback: sendUnaryData<T>) {
    const splitter = /element=([\w-]+)\s*>>\s*(.*)/;
    const parts = selector.split(splitter);
    if (parts.length == 4) {
        const splitted = {
            elementHandleId: parts[1],
            elementSelector: parts[2],
        };
        console.log(`Split element= selector into parts: ${JSON.stringify(splitted)}`);
        return splitted;
    }
    callback(new Error(`Invalid element selector \`${selector}\`.`), null);
    // This is purely to appease Typescript compiler, code is never executed since the
    // `callback` breaks the execution.
    return {
        elementHandleId: '',
        elementSelector: '',
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

function getErrorDetails(e: Error, selector: string, methodName: string) {
    const errorMetadata = new Metadata();
    if (e instanceof errors.TimeoutError) {
        errorMetadata.add('reason', `Could not find element with selector \`${selector}\` within timeout.`);
    }
    return {
        code: status.INVALID_ARGUMENT,
        name: e.name,
        message: '',
        details: `Error invoking Playwright action ${methodName}:\n${e.toString()}`,
        metadata: errorMetadata,
    };
}
