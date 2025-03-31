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
    let count = 0;
    try {
        count = await locator.count();
    } catch (e) {
        if (!(e instanceof Error && e.message.includes('failed to find frame for selector'))) {
            throw e;
        }
    }
    return intResponse(count, `Found ${count} element(s).`);
}

export async function getSelections(locator: Locator) {
    const response = new Response.Select();
    const selectElement = await locator.elementHandle();
    const selectOptions = await selectElement?.evaluate((e) => {
        return Array.from((e as HTMLSelectElement).options).map((option) => ({
            label: option.label,
            value: option.value,
            index: option.index,
            selected: option.selected,
        }));
    });
    if (selectOptions) {
        const entries = selectOptions.map((e) => {
            const entry = new Types.SelectEntry();
            entry.setLabel(e.label);
            entry.setValue(e.value);
            entry.setIndex(e.index);
            entry.setSelected(e.selected);
            return entry;
        });
        logger.info(`Option entries: ${entries.length}`);
        logger.info(`Selected entries: ${entries.filter((e) => e.getSelected()).length}`);
        entries.forEach((e) => response.addEntry(e));
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

async function getProperty(request: Request.ElementProperty, state: PlaywrightState) {
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
        const disabled = await locator.getAttribute('disabled');
        try {
            const editable = await locator.isEditable();
            if (editable && disabled === null) {
                logger.info(`Element ${selector} is editable: ${editable}`);
                states += stateEnum.editable;
            } else if (!editable && disabled !== null) {
                logger.info(`Element ${selector} is disabled: ${disabled}`);
                states += stateEnum.readonly;
            } else {
                logger.info(`Element ${selector} is readonly: ${!editable}`);
                states += stateEnum.readonly;
            }
        } catch (error) {
            logger.info(`Element ${selector} is not editable: ${error}`);
            if (disabled !== null) {
                logger.info(`Element ${selector} is disabled: ${disabled} and therefore readonly`);
                states += stateEnum.readonly;
            }
        }
        logger.info('Checking checked state');
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

export async function getStyle(request: Request.ElementStyle, state: PlaywrightState): Promise<Response.Json> {
    const selector = request.getSelector();
    const option = {
        styleKey: request.getStylekey() || null,
        pseudoElement: request.getPseudo() || null,
    };
    const strictMode = request.getStrict();

    logger.info('Getting css of element on page');
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    const result = await locator.evaluate((element: Element, option) => {
        const cssStyleDeclaration = window.getComputedStyle(element, option.pseudoElement);
        if (option.styleKey) {
            return cssStyleDeclaration.getPropertyValue(option.styleKey);
        } else {
            return Object.fromEntries(
                Array.from(cssStyleDeclaration).map((key) => [key, cssStyleDeclaration.getPropertyValue(key)]),
            );
        }
    }, option);
    return jsonResponse(JSON.stringify(result), 'Style get successfully.');
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
    const locator = await findLocator(state, selector, strictMode, undefined, true);
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
    const locator = await findLocator(state, selector, strictMode, undefined, true);
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
        let rows = element.querySelectorAll(':scope > * > tr');
        if (rows.length == 0) {
            rows = element.querySelectorAll(':scope > tr');
        }
        if (rows.length == 0) {
            throw Error(
                `Table rows could not be found. ChildNodes are: ${Array.prototype.slice
                    .call(element.childNodes)
                    .map((e) => `${e.nodeName}.${e.className}`)}`,
            );
        }
        return Array.prototype.indexOf.call(rows, table_row);
    });
    return intResponse(count, `Row index in table is ${count}.`);
}
