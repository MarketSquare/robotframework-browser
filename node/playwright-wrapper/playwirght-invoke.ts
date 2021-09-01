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

import { PlaywrightState } from './playwright-state';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

export async function waitUntilElementExists<T>(
    state: PlaywrightState,
    selector: string,
    strictMode: boolean,
): Promise<ElementHandle> {
    const { elementSelector, context } = await determineContextAndSelector(state, selector);
    logger.info(`Strict mode is: ${strictMode}`);
    if (elementSelector === undefined) {
        // This type cast is safe because elementSelector is only undefined when an ElementHandle gets returned
        return context as ElementHandle;
    } else if ('waitForSelector' in context) {
        await context.waitForSelector(elementSelector, { state: 'attached', strict: strictMode });
    }
    const element = await context.$(elementSelector, { strict: strictMode });
    exists(element, `Could not find element with selector \`${elementSelector}\` within timeout.`);
    return element;
}

export async function invokeOnMouse<T>(
    page: Page | undefined,
    methodName: 'move' | 'down' | 'up' | 'click' | 'dblclick',
    args: Record<any, any>,
) {
    exists(page, `Tried to execute mouse action '${methodName}' but no open page`);
    logger.info(`Invoking mouse action ${methodName} with params ${JSON.stringify(args)}`);
    const fn: any = page?.mouse[methodName].bind(page.mouse);
    exists(fn, `Bind failure with '${fn}'`);
    return await fn(...Object.values(args));
}

export async function invokeOnKeyboard<T>(
    page: Page,
    methodName: 'down' | 'up' | 'press' | 'insertText' | 'type',
    ...args: any[]
) {
    logger.info(`Invoking keyboard action ${methodName} with params ${JSON.stringify(args)}`);
    const fn: any = page.keyboard[methodName].bind(page.keyboard);
    exists(fn, `Bind failure with '${fn}'`);
    return await fn(...Object.values(args));
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
 * @param methodName Which Playwright method to invoke. The method should take selector as an argument.
 * @param selector Selector of the element to operate on,
 *  or a frame piercing selector in format `<frame selector> >>> <element selector>
 */

export async function invokePlaywrightMethod<T>(
    state: PlaywrightState,
    methodName: string,
    selector: string,
    ...args: any[]
) {
    type strDict = { [key: string]: any };
    const { elementSelector, context } = await determineContextAndSelector(state, selector);
    logger.info(`selector:::: ${selector}`);
    logger.info(`args::: ${args}`);
    if (elementSelector) {
        const fn = (context as strDict)[methodName].bind(context);
        return await fn(elementSelector, ...args);
    } else {
        if (methodName === '$$eval') {
            return state.getActivePage()?.evaluate(args[0], [context]);
        }
        if (methodName === '$eval') {
            return state.getActivePage()?.evaluate(args[0], context);
        }
        return await (context as strDict)[methodName](...args);
    }
}

export async function invokePlaywrightMethodStrict<T>(
    state: PlaywrightState,
    methodName: string,
    selector: string,
    strictMode: boolean,
    ...args: any[]
) {
    type strDict = { [key: string]: any };
    const { elementSelector, context } = await determineContextAndSelectorStrict(state, selector, strictMode);
    logger.info(`Page|Frame|Element resolved elementSelector: ${elementSelector}`);
    if (elementSelector) {
        await context.$(elementSelector, { strict: strictMode });
        const fn = (context as strDict)[methodName].bind(context);
        return await fn(elementSelector, ...args);
    } else {
        if (methodName === '$$eval') {
            return state.getActivePage()?.evaluate(args[0], [context]);
        }
        if (methodName === '$eval') {
            return state.getActivePage()?.evaluate(args[0], context);
        }
        return await (context as strDict)[methodName](...args);
    }
}

async function determineContextAndSelector<T>(
    state: PlaywrightState,
    selector: string,
): Promise<{ elementSelector: string | undefined; context: ElementHandle | Frame | Page }> {
    const page = state.getActivePage();
    exists(page, `Tried to do playwright action, but no open page.`);
    if (isFramePiercingSelector(selector)) {
        let selectors = splitFrameAndElementSelector(selector);
        let frame = await findFrame(page, selectors.frameSelector);
        while (isFramePiercingSelector(selectors.elementSelector)) {
            selectors = splitFrameAndElementSelector(selectors.elementSelector);
            frame = await findFrame(frame, selectors.frameSelector);
        }
        return { elementSelector: selectors.elementSelector, context: frame };
    } else if (isElementHandleSelector(selector)) {
        const { elementHandleId, subSelector } = splitElementHandleAndElementSelector(selector);
        const elem = state.getElement(elementHandleId);
        if (subSelector) return { elementSelector: subSelector, context: elem };
        else return { elementSelector: undefined, context: elem };
    } else {
        return { elementSelector: selector, context: page };
    }
}

async function determineContextAndSelectorStrict<T>(
    state: PlaywrightState,
    selector: string,
    strictMode: boolean,
): Promise<{ elementSelector: string | undefined; context: ElementHandle | Frame | Page }> {
    const page = state.getActivePage();
    exists(page, `Tried to do playwright action, but no open page.`);
    if (isFramePiercingSelector(selector)) {
        let selectors = splitFrameAndElementSelector(selector);
        let frame = await findFrameStrict(page, selectors.frameSelector, strictMode);
        while (isFramePiercingSelector(selectors.elementSelector)) {
            selectors = splitFrameAndElementSelector(selectors.elementSelector);
            frame = await findFrameStrict(frame, selectors.frameSelector, strictMode);
        }
        return { elementSelector: selectors.elementSelector, context: frame };
    } else if (isElementHandleSelector(selector)) {
        const { elementHandleId, subSelector } = splitElementHandleAndElementSelector(selector);
        const elem = state.getElement(elementHandleId);
        if (subSelector) return { elementSelector: subSelector, context: elem };
        else return { elementSelector: undefined, context: elem };
    } else {
        return { elementSelector: selector, context: page };
    }
}

export async function determineElement(state: PlaywrightState, selector: string): Promise<ElementHandle | null> {
    const page = state.getActivePage();
    exists(page, `Tried to do playwright action, but no open page.`);
    if (isFramePiercingSelector(selector)) {
        let selectors = splitFrameAndElementSelector(selector);
        let frame = await findFrame(page, selectors.frameSelector);
        while (isFramePiercingSelector(selectors.elementSelector)) {
            selectors = splitFrameAndElementSelector(selectors.elementSelector);
            frame = await findFrame(frame, selectors.frameSelector);
        }
        return await frame.$(selectors.elementSelector);
    } else if (isElementHandleSelector(selector)) {
        const { elementHandleId, subSelector } = splitElementHandleAndElementSelector(selector);
        const elem = state.getElement(elementHandleId);
        if (subSelector) {
            return await elem.$(subSelector);
        } else return elem;
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

function splitElementHandleAndElementSelector<T>(selector: string): { elementHandleId: string; subSelector: string } {
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
    throw new Error(`Invalid element selector \`${selector}\`.`);
}

async function findFrame<T>(parent: Page | Frame, frameSelector: string): Promise<Frame> {
    const contentFrame = await (await parent.$(frameSelector))?.contentFrame();
    exists(contentFrame, `Could not find frame with selector ${frameSelector}`);
    return contentFrame;
}

async function findFrameStrict<T>(parent: Page | Frame, frameSelector: string, strictMode: boolean): Promise<Frame> {
    const contentFrame = await (await parent.$(frameSelector, { strict: strictMode }))?.contentFrame();
    exists(contentFrame, `Could not find frame with selector ${frameSelector}`);
    return contentFrame;
}

// This is necessary for improved typescript inference
/*
 * If obj is not trueish call callback with new Error containing message
 */
export function exists<T1, T2>(obj: T1, message: string): asserts obj is NonNullable<T1> {
    if (!obj) {
        throw new Error(message);
    }
}
