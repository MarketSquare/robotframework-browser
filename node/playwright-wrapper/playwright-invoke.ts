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

import { Locator, Page } from 'playwright';

import { PlaywrightState } from './playwright-state';

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
    exists(activePage, 'Could not find active page');
    if (strictMode) {
        selector = selector.replaceAll(' >>> ', ' >> internal:control=enter-frame >> ');
    } else {
        selector = selector.replaceAll(' >>> ', ' >> nth=0 >> internal:control=enter-frame >> ');
    }
    if (nthLocator !== undefined) {
        return await findNthLocator(activePage, selector, nthLocator);
    } else if (strictMode) {
        logger.info(`Strict mode is enabled, find Locator with ${selector} in page.`);
        return activePage.locator(selector);
    } else {
        return await findLocatorNotStrict(activePage, selector, firstOnly);
    }
}

async function findNthLocator(activePage: Page, selector: string, nthLocator: number): Promise<Locator> {
    logger.info(`Find ${nthLocator} Locator in page.`);
    return activePage.locator(selector).nth(nthLocator);
}

async function findLocatorNotStrict(activePage: Page, selector: string, firstOnly: boolean): Promise<Locator> {
    if (firstOnly) {
        logger.info(`Strict mode is disabled, return first Locator: ${selector} in page.`);
        return activePage.locator(selector).first();
    } else {
        logger.info(`Strict mode is disabled, return Locator: ${selector} in page.`);
        return activePage.locator(selector);
    }
}

export async function invokeOnMouse(
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

export async function invokeOnKeyboard(
    page: Page,
    methodName: 'down' | 'up' | 'press' | 'insertText' | 'type',
    ...args: any[]
) {
    logger.info(`Invoking keyboard action ${methodName} with params ${JSON.stringify(args)}`);
    const fn: any = page.keyboard[methodName].bind(page.keyboard);
    exists(fn, `Bind failure with '${fn}'`);
    return await fn(...Object.values(args));
}

// This is necessary for improved typescript inference
/*
 * If obj is not trueish call callback with new Error containing message
 */
export function exists<T1>(obj: T1, message: string): asserts obj is NonNullable<T1> {
    if (!obj) {
        throw new Error(message);
    }
}
