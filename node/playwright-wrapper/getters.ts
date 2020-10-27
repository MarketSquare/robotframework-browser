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
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { PlaywrightState } from './playwright-state';
import { Request, Response, Types } from './generated/playwright_pb';
import { boolResponse, intResponse, jsonResponse, stringResponse } from './response-util';
import { determineElement, invokeOnPage, invokePlaywrightMethod, waitUntilElementExists } from './playwirght-invoke';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

export async function getTitle(callback: sendUnaryData<Response.String>, page?: Page) {
    const title = await invokeOnPage(page, 'title');
    callback(null, stringResponse(title, 'Active page title is: ' + title));
}

export async function getUrl(callback: sendUnaryData<Response.String>, page?: Page) {
    const url = await invokeOnPage(page, 'url');
    callback(null, stringResponse(url, url));
}

export async function getElementCount(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Int>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const response: Array<ElementHandle> = await invokePlaywrightMethod(state, '$$', selector);
    callback(null, intResponse(response.length, 'Found ' + response.length + 'element(s).'));
}

export async function getSelectContent(
    call: ServerUnaryCall<Request.ElementSelector>,
    state: PlaywrightState,
): Promise<Response.Select> {
    const selector = call.request.getSelector();
    await waitUntilElementExists(state, selector);

    type Value = [string, string, boolean];
    const content: Value[] = await invokePlaywrightMethod(state, '$$eval', selector + ' option', (elements: any) =>
        (elements as HTMLOptionElement[]).map((elem) => [elem.label, elem.value, elem.selected]),
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
    call: ServerUnaryCall<Request.ElementProperty>,
    state: PlaywrightState,
): Promise<Response.String> {
    const content = await getProperty(call, state);
    return stringResponse(JSON.stringify(content), 'Property received successfully.');
}

export async function getBoolProperty(
    call: ServerUnaryCall<Request.ElementProperty>,
    state: PlaywrightState,
): Promise<Response.Bool> {
    const selector = call.request.getSelector();
    const content = await getProperty(call, state);
    return boolResponse(content || false, 'Retrieved dom property for element ' + selector + ' containing ' + content);
}

async function getProperty<T>(call: ServerUnaryCall<Request.ElementProperty>, state: PlaywrightState) {
    const selector = call.request.getSelector();
    const element = await waitUntilElementExists(state, selector);
    try {
        const propertyName = call.request.getProperty();
        const property = await element.getProperty(propertyName);
        const content = await property.jsonValue();
        logger.info(`Retrieved dom property for element ${selector} containing ${content}`);
        return content;
    } catch (e) {
        logger.error(e);
        throw e;
    }
}

export async function getElementAttribute(
    call: ServerUnaryCall<Request.ElementProperty>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
) {
    const content = await getAttributeValue(call, callback, state);
    callback(null, stringResponse(JSON.stringify(content), 'Property received successfully.'));
}

async function getAttributeValue<T>(
    call: ServerUnaryCall<Request.ElementProperty>,
    callback: sendUnaryData<T>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const element = await waitUntilElementExists(state, selector);
    try {
        const attributeName = call.request.getProperty();
        const attribute = await element.getAttribute(attributeName);
        logger.info(`Retrieved attribute for element ${selector} containing ${attribute}`);
        return attribute;
    } catch (e) {
        logger.error(e);
        return callback(e, null);
    }
}

export async function getStyle(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Json>,
    state: PlaywrightState,
): Promise<void> {
    const selector = call.request.getSelector();

    logger.info('Getting css of element on page');
    const result = await invokePlaywrightMethod(state, '$eval', selector, function (element: Element) {
        const rawStyle = window.getComputedStyle(element);
        const mapped: Record<string, string> = {};
        // This is necessary because JSON.stringify doesn't handle CSSStyleDeclarations correctly
        for (let i = 0; i < rawStyle.length; i++) {
            const name = rawStyle[i];
            mapped[name] = rawStyle.getPropertyValue(name);
        }
        return JSON.stringify(mapped);
    });
    const response = jsonResponse(result, 'Style get succesfully.');
    callback(null, response);
}

export async function getViewportSize(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.Json>,
    page?: Page,
): Promise<void> {
    const result = await invokeOnPage(page, 'viewportSize');
    callback(null, jsonResponse(JSON.stringify(result), 'View port size received sucesfully from page.'));
}

export async function getBoundingBox(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Json>,
    state: PlaywrightState,
): Promise<void> {
    const selector = call.request.getSelector();
    const elem = await determineElement(state, selector);
    if (!elem) {
        callback(new Error(`No element matching ${selector} found`), null);
        return;
    }
    const boundingBox = await elem.boundingBox();
    callback(null, jsonResponse(JSON.stringify(boundingBox), ''));
}

export async function getPageSource(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.String>,
    page?: Page,
): Promise<void> {
    const result = await invokeOnPage(page, 'content');
    logger.info(result);
    callback(null, stringResponse(JSON.stringify(result), 'Page source obtained succesfully.'));
}
