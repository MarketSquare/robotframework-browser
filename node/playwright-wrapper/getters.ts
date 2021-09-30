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

import { ElementHandle, Page } from 'playwright';

import { PlaywrightState } from './playwright-state';
import { Request, Response, Types } from './generated/playwright_pb';
import { boolResponse, intResponse, jsonResponse, stringResponse } from './response-util';
import { determineElement, invokePlaywrightMethod, waitUntilElementExists } from './playwirght-invoke';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

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
    const response: Array<ElementHandle> = await invokePlaywrightMethod(state, '$$', selector, strictMode);
    return intResponse(response.length, 'Found ' + response.length + 'element(s).');
}

export async function getSelectContent(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Select> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    await waitUntilElementExists(state, selector, strictMode);

    type Value = [string, string, boolean];

    const content: Value[] = await invokePlaywrightMethod(
        state,
        '$eval',
        selector,
        strictMode,
        (select: HTMLSelectElement) => {
            const options: Value[] = [];
            for (let i = 0; i < select.options.length; i++) {
                const elem: HTMLOptionElement = select.options[i];
                options.push([elem.label, elem.value, elem.selected]);
            }
            return options;
        },
    );

    const response = new Response.Select();
    content.forEach((option) => {
        const [label, value, selected] = [option[0], option[1], option[2]];
        const entry = new Types.SelectEntry();
        entry.setLabel(label);
        entry.setValue(value);
        entry.setSelected(selected);
        response.addEntry(entry);
    });
    return response;
}

export async function getDomProperty(
    request: Request.ElementProperty,
    state: PlaywrightState,
): Promise<Response.String> {
    const content = await getProperty(request, state);
    return stringResponse(JSON.stringify(content), 'Property received successfully.');
}

async function getTextContent(element: ElementHandle<Node>): Promise<string> {
    const tag = await (await element.getProperty('tagName')).jsonValue();
    if (tag === 'INPUT' || tag === 'TEXTAREA') {
        return await (await element.getProperty('value')).jsonValue();
    }
    return await element.innerText();
}

export async function getText(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.String> {
    const selector = request.getSelector();
    const strict = request.getStrict();
    const element = await waitUntilElementExists(state, selector, strict);
    let content: string;
    try {
        content = await getTextContent(element);
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
    const element = await waitUntilElementExists(state, selector, strictMode);
    try {
        const propertyName = request.getProperty();
        const property = await element.getProperty(propertyName);
        const content = await property.jsonValue();
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
    const element = await waitUntilElementExists(state, selector, strictMode);
    const attributeName = request.getProperty();
    const attribute = await element.getAttribute(attributeName);
    logger.info(`Retrieved attribute for element ${selector} containing ${attribute}`);
    return attribute;
}

export async function getStyle(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Json> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();

    logger.info('Getting css of element on page');
    const result = await invokePlaywrightMethod(state, '$eval', selector, strictMode, function (element: Element) {
        const rawStyle = window.getComputedStyle(element);
        const mapped: Record<string, string> = {};
        // This is necessary because JSON.stringify doesn't handle CSSStyleDeclarations correctly
        for (let i = 0; i < rawStyle.length; i++) {
            const name = rawStyle[i];
            mapped[name] = rawStyle.getPropertyValue(name);
        }
        return JSON.stringify(mapped);
    });
    return jsonResponse(result, 'Style get succesfully.');
}

export async function getViewportSize(page: Page): Promise<Response.Json> {
    const result = page.viewportSize();
    return jsonResponse(JSON.stringify(result), 'View port size received sucesfully from page.');
}

export async function getBoundingBox(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Json> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const elem = await determineElement(state, selector, strictMode);
    if (!elem) {
        throw new Error(`No element matching ${selector} found`);
    }
    const boundingBox = await elem.boundingBox();
    return jsonResponse(JSON.stringify(boundingBox), 'Got bounding box succesfully.');
}

export async function getPageSource(page: Page): Promise<Response.String> {
    const result = await page.content();
    logger.info(result);
    return stringResponse(JSON.stringify(result), 'Page source obtained succesfully.');
}
