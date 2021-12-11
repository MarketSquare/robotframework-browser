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

import { Frame, FrameLocator, Locator, Page } from 'playwright';

import { LocatorCount, PlaywrightState } from './playwright-state';

import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

/**
 * Resolve the playwright Locator on active page, frame or elementHandle.
 *
 * @param state A reference to current PlaywrightState object.
 * @param selector A valid Playwright selector, Frame piercing selector "#iframe >>> //button"
 *  or selector containing Locator handle in the front. element=123-456-789 >> css=input
 * @param strictMode Used with combination on firstOnly param. When strictMode is false, firstOnly is applied.
 * @param nthLocator Find nth locator from the page, frame, locator: https://playwright.dev/docs/api/class-locator#locator-nth
 * @param firstOnly If True locator matching to first element returned else locator can point to multiple elements.
 * */

export async function findLocator(
    state: PlaywrightState,
    selector: string,
    strictMode: boolean,
    nthLocator: number | undefined,
    firstOnly: boolean,
): Promise<Locator> {
    const activePage = state.getActivePage();
    let locator = undefined;
    exists(activePage, 'Could not find active page');
    if (isElementHandleSelector(selector)) {
        const { elementHandleId, subSelector } = splitElementHandleAndElementSelector(selector);
        locator = state.getLocator(elementHandleId);
        selector = subSelector;
        if (!selector) {
            logger.info('Only locator handle defined, return cached Locator.');
            return locator.locator;
        }
    }
    if (isFramePiercingSelector(selector)) {
        return await findInFrames(activePage, selector, strictMode, nthLocator, firstOnly);
    }
    if (nthLocator !== undefined) {
        return await findNthLocator(activePage, selector, nthLocator, locator);
    } else if (strictMode) {
        if (locator?.locator) {
            logger.info(`Strict mode is enabled, find Locator with ${selector} within locator.`);
            return locator.locator.locator(selector);
        } else {
            logger.info(`Strict mode is enabled, find Locator with ${selector} in page.`);
            return activePage.locator(selector);
        }
    } else {
        return await findLocatorNotStrict(activePage, selector, firstOnly, locator);
    }
}

async function findInFrames(
    activePage: Page,
    selector: string,
    strictMode: boolean,
    nthLocator: number | undefined,
    firstOnly: boolean,
): Promise<Locator> {
    let selectors = splitFrameAndElementSelector(selector);
    let frame = await findFrameLocator(activePage, selectors.frameSelector, strictMode);
    while (isFramePiercingSelector(selectors.elementSelector)) {
        selectors = splitFrameAndElementSelector(selectors.elementSelector);
        frame = await findFrameLocator(frame, selectors.frameSelector, strictMode);
    }
    if (nthLocator) {
        logger.info(`Find ${nthLocator} locator in frame.`);
        return frame.locator(selectors.elementSelector).nth(nthLocator);
    } else if (strictMode) {
        logger.info(`Strict mode is enabled, find with ${selector} in frame.`);
        return frame.locator(selectors.elementSelector);
    } else {
        if (firstOnly) {
            logger.info(
                `Strict mode is disabled and firstOnly is enabled, return first Locator: ${selector} in frame.`,
            );
            return frame.locator(selectors.elementSelector).first();
        } else {
            logger.info(`Strict mode is disabled and firstOnly is disabled, return Locator: ${selector} in frame.`);
            return frame.locator(selectors.elementSelector);
        }
    }
}

async function findNthLocator(
    activePage: Page,
    selector: string,
    nthLocator: number,
    locator?: LocatorCount,
): Promise<Locator> {
    if (locator?.locator) {
        logger.info(`Find ${nthLocator} Locator within locator.`);
        return locator.locator.locator(selector).nth(nthLocator);
    } else {
        logger.info(`Find ${nthLocator} Locator in page.`);
        return activePage.locator(selector).nth(nthLocator);
    }
}

async function findLocatorNotStrict(
    activePage: Page,
    selector: string,
    firstOnly: boolean,
    locator?: LocatorCount,
): Promise<Locator> {
    if (locator?.locator) {
        if (firstOnly) {
            logger.info(`Strict mode is disabled, return first Locator: ${selector} with locator.`);
            return locator.locator.locator(selector).first();
        } else {
            logger.info(`Strict mode is disabled, return Locator: ${selector} with locator.`);
            return locator.locator.locator(selector);
        }
    } else {
        if (firstOnly) {
            logger.info(`Strict mode is disabled, return first Locator: ${selector} in page.`);
            return (locator?.locator || activePage).locator(selector).first();
        } else {
            logger.info(`Strict mode is disabled, return Locator: ${selector} in page.`);
            return (locator?.locator || activePage).locator(selector);
        }
    }
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
        logger.info(`element=${parts[1]} selector parsed without children`);
        return {
            elementHandleId: parts[1],
            subSelector: '',
        };
    }
    throw new Error(`Invalid element selector \`${selector}\`.`);
}

async function findFrameLocator<T>(
    parent: Page | FrameLocator,
    frameSelector: string,
    strictMode: boolean,
): Promise<FrameLocator> {
    if (strictMode) {
        return parent.frameLocator(frameSelector);
    } else {
        return parent.frameLocator(frameSelector).first();
    }
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
