// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { BrowserContext, ElementHandle, Frame, Page, errors } from 'playwright';
import { Metadata, sendUnaryData, status } from 'grpc';

import { PlaywrightState } from './playwright-state';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

export async function waitUntilElementExists<T>(
    state: PlaywrightState,
    callback: sendUnaryData<T>,
    selector: string,
): Promise<ElementHandle> {
    const { elementSelector, context } = await determineContextAndSelector(state, selector, callback);
    if (elementSelector === undefined) {
        // This type cast is safe because elementSelector is only undefined when an ElementHandle gets returned
        return context as ElementHandle;
    } else if ('waitForSelector' in context) {
        try {
            await context.waitForSelector(elementSelector, { state: 'attached' });
        } catch (e) {
            callback(getErrorDetails(e, selector, 'waitForSelector'), null);
            throw e;
        }
    }
    const element = await context.$(elementSelector);
    exists(element, callback, `Could not find element with selector \`${elementSelector}\` within timeout.`);
    return element;
}

async function invokeFunction<T>(callback: sendUnaryData<T>, method: any, ...args: any[]) {
    exists(method, callback, `Bind failure with '${method}'`);
    try {
        return await method(...Object.values(args));
    } catch (e) {
        logger.error(`Error invoking Playwright action '${method}': ${e}`);
        return callback(e, null);
    }
}

export async function invokeOnMouse<T>(
    page: Page | undefined,
    callback: sendUnaryData<T>,
    methodName: 'move' | 'down' | 'up' | 'click' | 'dblclick',
    args: Record<any, any>,
) {
    exists(page, callback, `Tried to execute mouse action '${methodName}' but no open page`);
    logger.info(`Invoking mouse action ${methodName} with params ${JSON.stringify(args)}`);
    const fn: any = page?.mouse[methodName].bind(page.mouse);
    return await invokeFunction(callback, fn, ...Object.values(args));
}

export async function invokeOnKeyboard<T>(
    page: Page | undefined,
    callback: sendUnaryData<T>,
    methodName: 'down' | 'up' | 'press' | 'insertText' | 'type',
    ...args: any[]
) {
    exists(page, callback, `Tried to execute keyboard action '${methodName}' but no open page`);
    logger.info(`Invoking keyboard action ${methodName} with params ${JSON.stringify(args)}`);
    const fn: any = page?.keyboard[methodName].bind(page.keyboard);
    return await invokeFunction(callback, fn, ...args);
}

export async function invokeOnPage<T>(
    page: Page | undefined,
    callback: sendUnaryData<T>,
    methodName: string,
    ...args: any[]
) {
    exists(page, callback, `Tried to do playwright action '${methodName}', but no open page.`);
    const fn: any = (page as { [key: string]: any })[methodName].bind(page);
    return await invokeFunction(callback, fn, ...args);
}

export async function invokeOnContext<T>(
    context: BrowserContext | undefined,
    callback: sendUnaryData<T>,
    methodName: string,
    ...args: any[]
) {
    exists(context, callback, `Tried to do playwright action '${methodName}', but no open context.`);
    try {
        const fn: any = (context as { [key: string]: any })[methodName].bind(context);
        return await fn(...args);
    } catch (e) {
        logger.info(`Error invoking Playwright action '${methodName}': ${e}`);
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
 * @param methodName Which Playwright method to invoke. The method should take selector as an argument.
 * @param selector Selector of the element to operate on,
 *  or a frame piercing selector in format `<frame selector> >>> <element selector>
 * @param args Additional args to the Playwirght method.
 */

export async function invokePlaywrightMethod<T>(
    state: PlaywrightState,
    callback: sendUnaryData<T>,
    methodName: string,
    selector: string,
    ...args: any[]
) {
    type strDict = { [key: string]: any };
    const { elementSelector, context } = await determineContextAndSelector(state, selector, callback);
    try {
        if (elementSelector) {
            const fn = (context as strDict)[methodName].bind(context);
            return await fn(elementSelector, ...args);
        } else {
            return await (context as strDict)[methodName](...args);
        }
    } catch (e) {
        callback(getErrorDetails(e, selector, methodName), null);
        throw e;
    }
}

async function determineContextAndSelector<T>(
    state: PlaywrightState,
    selector: string,
    callback: sendUnaryData<T>,
): Promise<{ elementSelector: string | undefined; context: ElementHandle | Frame | Page }> {
    const page = state.getActivePage();
    exists(page, callback, `Tried to do playwright action, but no open page.`);
    if (isFramePiercingSelector(selector)) {
        let selectors = splitFrameAndElementSelector(selector);
        let frame = await findFrame(page, selectors.frameSelector, callback);
        while (isFramePiercingSelector(selectors.elementSelector)) {
            selectors = splitFrameAndElementSelector(selectors.elementSelector);
            frame = await findFrame(frame, selectors.frameSelector, callback);
        }
        return { elementSelector: selectors.elementSelector, context: frame };
    } else if (isElementHandleSelector(selector)) {
        const { elementHandleId, subSelector } = splitElementHandleAndElementSelector(selector, callback);

        try {
            const elem = state.getElement(elementHandleId);
            if (subSelector) return { elementSelector: subSelector, context: elem };
            else return { elementSelector: undefined, context: elem };
        } catch (e) {
            callback(e, null);
            // This is purely to appease Typescript compiler, code is never executed since the
            // `callback` breaks the execution. Having a throw doesn't obfuscate the return types.
            throw 'Never executes?';
        }
    } else {
        return { elementSelector: selector, context: page };
    }
}

export async function determineElement<T>(
    state: PlaywrightState,
    selector: string,
    callback: sendUnaryData<T>,
): Promise<ElementHandle | null> {
    const page = state.getActivePage();
    exists(page, callback, `Tried to do playwright action, but no open page.`);
    if (isFramePiercingSelector(selector)) {
        const { frameSelector, elementSelector } = splitFrameAndElementSelector(selector);
        const frame = await findFrame(page, frameSelector, callback);
        return await frame.$(elementSelector);
    } else if (isElementHandleSelector(selector)) {
        const { elementHandleId, subSelector } = splitElementHandleAndElementSelector(selector, callback);
        try {
            const elem = state.getElement(elementHandleId);
            if (subSelector) {
                return await elem.$(subSelector);
            } else return elem;
        } catch (e) {
            callback(e, null);
            return null;
        }
    } else {
        return await page.$(selector);
    }
}

function isFramePiercingSelector(selector: string) {
    return selector.match('>>>');
}

function isElementHandleSelector(selector: string) {
    return selector.startsWith('element=');
}

function splitFrameAndElementSelector(selector: string) {
    const [first, ...rest] = selector.split(' >>> ');
    return {
        frameSelector: first.trim(),
        elementSelector: rest.join(' >>> ').trim(),
    };
}

function splitElementHandleAndElementSelector<T>(
    selector: string,
    callback: sendUnaryData<T>,
): {
    elementHandleId: string;
    subSelector: string;
} {
    // const splitter = /element=([\w-]+)\s*>>\s*(.*)/;
    const splitter = /element=([\w-]+)\s*[>>]*\s*(.*)/;
    const parts = selector.split(splitter);
    if (parts.length == 4 && parts[2]) {
        const splitted = {
            elementHandleId: parts[1],
            subSelector: parts[2],
        };
        logger.info(`Split element= selector into parts: ${JSON.stringify(splitted)}`);
        return splitted;
    } else if (parts[1]) {
        logger.info(`element= selector parsed without children`);
        return {
            elementHandleId: parts[1],
            subSelector: '',
        };
    }
    callback(new Error(`Invalid element selector \`${selector}\`.`), null);
    // This is purely to appease Typescript compiler, code is never executed since the
    // `callback` breaks the execution. Having a throw doesn't obfuscate the return types.
    throw 'Never executes?';
}

async function findFrame<T>(parent: Page | Frame, frameSelector: string, callback: sendUnaryData<T>): Promise<Frame> {
    const contentFrame = await (await parent.$(frameSelector))?.contentFrame();
    exists(contentFrame, callback, `Could not find frame with selector ${frameSelector}`);
    return contentFrame;
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
    if (e.message.match(/DOMException: .* is not a valid selector/)) {
        errorMetadata.add('reason', `Invalid selector \`${selector}\`.`);
    }
    return {
        code: status.INVALID_ARGUMENT,
        name: e.name,
        message: '',
        details: `Error invoking Playwright action ${methodName}:\n${e.toString()}`,
        metadata: errorMetadata,
    };
}
