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

import { PlaywrightState } from './playwright-state';
import { Request, Response, Types } from './generated/playwright_pb';
import { boolResponse, intResponse, jsonResponse, stringResponse } from './response-util';
import {
    determineElement,
    exists,
    findLocator,
    findLocatorCount,
    invokePlaywrightMethod,
    waitUntilElementExists,
} from './playwirght-invoke';

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
    const count: number = await findLocatorCount(state, selector);
    return intResponse(count, `Found ${count} element(s).`);
}

export async function getSelectContent(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Select> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.elementHandle();
    const locatorOptions = locator.locator('option');
    const locatorOptionsCount = await locatorOptions.count();
    const response = new Response.Select();

    for (let i = 0; i < locatorOptionsCount; i++) {
        const element = await locatorOptions.nth(i).elementHandle();
        exists(element, `The ${i} option element did not exist.`);
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

export async function getStyle(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Json> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();

    logger.info('Getting css of element on page');
    const element = await findLocator(state, selector, strictMode, undefined, false);
    logger.info(`HERE:::${strictMode}`);
    await element.elementHandle();
    const result = await element.evaluate(function (element: Element) {
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
    const locator = await findLocator(state, selector, strictMode, undefined, false);
    const boundingBox = await locator.boundingBox();
    return jsonResponse(JSON.stringify(boundingBox), 'Got bounding box succesfully.');
}

export async function getPageSource(page: Page): Promise<Response.String> {
    const result = await page.content();
    logger.info(result);
    return stringResponse(JSON.stringify(result), 'Page source obtained succesfully.');
}
