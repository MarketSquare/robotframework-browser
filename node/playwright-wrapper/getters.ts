import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Page, ElementHandle } from 'playwright';

import { Response, Request, Types } from './generated/playwright_pb';
import { invokeOnPage, invokePlaywirghtMethod, waitUntilElementExists } from './playwirght-invoke';
import { stringResponse, boolResponse, intResponse } from './response-util';
import { PlaywrightState } from './playwright-state';

export async function getTitle(callback: sendUnaryData<Response.String>, page?: Page) {
    const title = await invokeOnPage(page, callback, 'title');
    callback(null, stringResponse(title));
}

export async function getUrl(callback: sendUnaryData<Response.String>, page?: Page) {
    const url = await invokeOnPage(page, callback, 'url');
    callback(null, stringResponse(url));
}

export async function getElementCount(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Int>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const response: Array<ElementHandle> = await invokePlaywirghtMethod(state, callback, '$$', selector);
    callback(null, intResponse(response.length));
}

export async function getSelectContent(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Select>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await waitUntilElementExists(state, callback, selector);

    type Value = [string, string, boolean];
    const content: Value[] = await invokePlaywirghtMethod(
        state,
        callback,
        '$$eval',
        selector + ' option',
        (elements: any) => (elements as HTMLOptionElement[]).map((elem) => [elem.label, elem.value, elem.selected]),
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
    callback(null, response);
}

export async function getDomProperty(
    call: ServerUnaryCall<Request.ElementProperty>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
) {
    const content = await getProperty(call, callback, state);
    callback(null, stringResponse(content));
}

export async function getBoolProperty(
    call: ServerUnaryCall<Request.ElementProperty>,
    callback: sendUnaryData<Response.Bool>,
    state: PlaywrightState,
) {
    const content = await getProperty(call, callback, state);
    callback(null, boolResponse(content || false));
}

async function getProperty<T>(
    call: ServerUnaryCall<Request.ElementProperty>,
    callback: sendUnaryData<T>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const element = await waitUntilElementExists(state, callback, selector);
    try {
        const propertyName = call.request.getProperty();
        const property = await element.getProperty(propertyName);
        const content = await property.jsonValue();
        console.log(`Retrieved dom property for element ${selector} containing ${content}`);
        return content;
    } catch (e) {
        console.log(e);
        callback(e, null);
    }
}

export async function getStyle(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
): Promise<void> {
    const selector = call.request.getSelector();

    console.log('Getting css of element on page');
    const result = await invokePlaywirghtMethod(state, callback, '$eval', selector, function (element: Element) {
        const rawStyle = window.getComputedStyle(element);
        const mapped: Record<string, string> = {};
        // This is necessary because JSON.stringify doesn't handle CSSStyleDeclarations correctly
        for (let i = 0; i < rawStyle.length; i++) {
            const name = rawStyle[i];
            mapped[name] = rawStyle.getPropertyValue(name);
        }
        return JSON.stringify(mapped);
    });
    console.log(result);
    const response = stringResponse(result);
    callback(null, response);
}

export async function getViewportSize(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.String>,
    page?: Page,
): Promise<void> {
    const result = await invokeOnPage(page, callback, 'viewportSize');
    callback(null, stringResponse(JSON.stringify(result)));
}
