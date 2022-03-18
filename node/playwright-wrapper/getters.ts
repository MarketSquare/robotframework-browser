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

import { ElementHandle, Locator, Page } from 'playwright';
import { errors } from 'playwright';

import { PlaywrightState } from './playwright-state';
import { Request, Response, Types } from './generated/playwright_pb';
import { boolResponse, intResponse, jsonResponse, stringResponse } from './response-util';
import { exists, findLocator } from './playwright-invoke';

import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function getTitle(page: Page): Promise<Response.String> {
    const title = await page.title();
    return stringResponse(title, 'Active page title is: ' + title);
}

export async function getUrl(page: Page): Promise<Response.String> {
    const url = page.url();
    return stringResponse(url, url);
}

export async function getElementCount(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Int> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, false);
    const count = await locator.count();
    return intResponse(count, `Found ${count} element(s).`);
}

export async function getSelections(locator: Locator) {
    const locatorOptions = locator.locator('option');
    const locatorOptionsCount = await locatorOptions.count();
    const response = new Response.Select();

    for (let i = 0; i < locatorOptionsCount; i++) {
        const element = await locatorOptions.nth(i).elementHandle();
        exists(element, `The ${i}. option element does not longer exist.`);
        const label = await element.getProperty('label');
        const value = await element.getProperty('value');
        const selected = await element.getProperty('selected');
        const entry = new Types.SelectEntry();
        entry.setLabel(String(label));
        entry.setValue(String(value));
        entry.setSelected(JSON.parse(String(selected)));
        response.addEntry(entry);
    }
    return response;
}

export async function getSelectContent(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Select> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.elementHandle();
    return await getSelections(locator);
}

export async function getDomProperty(
    request: Request.ElementProperty,
    state: PlaywrightState,
): Promise<Response.String> {
    const content = await getProperty(request, state);
    return stringResponse(JSON.stringify(content), 'Property received successfully.');
}

async function getTextContent(locator: Locator): Promise<string> {
    const element = await locator.elementHandle();
    exists(element, 'Locator did not resolve to elementHandle.');
    const tag = await (await element.getProperty('tagName')).jsonValue();
    if (tag === 'INPUT' || tag === 'TEXTAREA') {
        return await (await element.getProperty('value')).jsonValue();
    }
    return await element.innerText();
}

export async function getText(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.String> {
    const selector = request.getSelector();
    const strict = request.getStrict();
    const locator = await findLocator(state, selector, strict, undefined, true);
    let content: string;
    try {
        content = await getTextContent(locator);
        logger.info(`Retrieved text for element ${selector} containing ${content}`);
    } catch (e) {
        if (e instanceof Error) {
            logger.error(e);
        }
        throw e;
    }
    return stringResponse(content, 'Text received successfully.');
}

export async function getBoolProperty(
    request: Request.ElementProperty,
    state: PlaywrightState,
): Promise<Response.Bool> {
    const selector = request.getSelector();
    const content = await getProperty(request, state);
    return boolResponse(content || false, 'Retrieved dom property for element ' + selector + ' containing ' + content);
}

async function getProperty<T>(request: Request.ElementProperty, state: PlaywrightState) {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = findLocator(state, selector, strictMode, undefined, true);
    try {
        const element = await (await locator).elementHandle();
        const propertyName = request.getProperty();
        const property = await element?.getProperty(propertyName);
        const content = await property?.jsonValue();
        logger.info(`Retrieved dom property for element ${selector} containing ${content}`);
        return content;
    } catch (e) {
        if (e instanceof Error) {
            logger.error(e);
        }
        throw e;
    }
}

export async function getElementAttribute(
    request: Request.ElementProperty,
    state: PlaywrightState,
): Promise<Response.String> {
    const content = await getAttributeValue(request, state);
    return stringResponse(JSON.stringify(content), 'Property received successfully.');
}

async function getAttributeValue(request: Request.ElementProperty, state: PlaywrightState) {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const attributeName = request.getProperty();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.elementHandle();
    const attribute = await locator.getAttribute(attributeName);
    logger.info(`Retrieved attribute for element ${selector} containing ${attribute}`);
    return attribute;
}

const stateEnum = {
    attached: 1,
    detached: 2,
    visible: 4,
    hidden: 8,
    enabled: 16,
    disabled: 32,
    editable: 64,
    readonly: 128,
    selected: 256,
    deselected: 512,
    focused: 1024,
    defocused: 2048,
    checked: 4096,
    unchecked: 8192,
    stable: 16384,
};

async function getCheckedState(locator: Locator) {
    try {
        return (await locator.isChecked()) ? stateEnum.checked : stateEnum.unchecked;
    } catch {
        return 0;
    }
}

async function getSelectState(element: ElementHandle) {
    if (await element.evaluate((e) => 'selected' in e)) {
        return (await element.evaluate((e) => (e as HTMLOptionElement).selected))
            ? stateEnum.selected
            : stateEnum.deselected;
    } else {
        return 0;
    }
}

export async function getElementStates(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Json> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    let states = 0;
    try {
        await locator.waitFor({ state: 'attached', timeout: 250 });
        states = stateEnum.attached;
        states += (await locator.isVisible()) ? stateEnum.visible : stateEnum.hidden;
        states += (await locator.isEnabled()) ? stateEnum.enabled : stateEnum.disabled;
        states += (await locator.isEditable()) ? stateEnum.editable : stateEnum.readonly;
        states += await getCheckedState(locator);
        try {
            const element = await locator.elementHandle();
            exists(element, 'Locator did not resolve to elementHandle.');
            states += await getSelectState(element);
            states += (await element.evaluate((e) => document.activeElement === e))
                ? stateEnum.focused
                : stateEnum.defocused;
        } catch {}
    } catch (e) {
        if (e instanceof errors.TimeoutError) {
            states = stateEnum.detached;
        } else {
            logger.error(e);
            throw e;
        }
    }
    return jsonResponse(JSON.stringify(states), 'Returned state.');
}

export async function getStyle(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Json> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();

    logger.info('Getting css of element on page');
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.elementHandle();
    const result = await locator.evaluate(function (element: Element) {
        const rawStyle = window.getComputedStyle(element);
        const mapped: Record<string, string> = {};
        // This is necessary because JSON.stringify doesn't handle CSSStyleDeclarations correctly
        for (let i = 0; i < rawStyle.length; i++) {
            const name = rawStyle[i];
            mapped[name] = rawStyle.getPropertyValue(name);
        }
        return JSON.stringify(mapped);
    });
    return jsonResponse(result, 'Style get successfully.');
}

export async function getViewportSize(page: Page): Promise<Response.Json> {
    const result = page.viewportSize();
    return jsonResponse(JSON.stringify(result), 'View port size received sucesfully from page.');
}

export async function getBoundingBox(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Json> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    const boundingBox = await locator.boundingBox();
    return jsonResponse(JSON.stringify(boundingBox), 'Got bounding box successfully.');
}

export async function getPageSource(page: Page): Promise<Response.String> {
    const result = await page.content();
    logger.info(result);
    return stringResponse(JSON.stringify(result), 'Page source obtained successfully.');
}

export async function getTableCellIndex(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Int> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, false);
    const element = await locator.elementHandle();
    exists(element, 'Locator did not resolve to elementHandle.');
    const count = await element.evaluate((element) => {
        while (!['TD', 'TH'].includes(element.nodeName)) {
            const parent = element.parentElement;
            if (!parent) {
                throw Error('Selector does not select a table cell!');
            }
            element = parent;
        }
        return Array.prototype.indexOf.call(element.parentNode?.children, element);
    });
    return intResponse(count, `Cell index in row is ${count}.`);
}

export async function getTableRowIndex(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Int> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, false);
    const element = await locator.elementHandle();
    exists(element, 'Locator did not resolve to elementHandle.');
    const count = await element.evaluate((element) => {
        let table_row = null;
        while (element.nodeName !== 'TABLE') {
            if (element.nodeName === 'TR') {
                table_row = element;
            }
            const parent = element.parentElement;
            if (!parent) {
                throw Error('Selector does not select a table cell!');
            }
            element = parent;
        }
        return Array.prototype.indexOf.call(element.querySelectorAll(':scope > * > tr'), table_row);
    });
    return intResponse(count, `Row index in table is ${count}.`);
}
