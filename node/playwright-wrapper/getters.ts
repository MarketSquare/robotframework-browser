import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Page, ElementHandle } from 'playwright';

import { Response, Request, Types } from './generated/playwright_pb';
import { invokeOnPage, invokeOnPageWithSelector, waitUntilElementExists } from './playwirght-util';
import { stringResponse, boolResponse, intResponse } from './response-util';

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
    page?: Page,
) {
    const selector = call.request.getSelector();
    const response: Array<ElementHandle> = await invokeOnPageWithSelector(page, callback, '$$', selector);
    callback(null, intResponse(response.length));
}

export async function getSelectContent(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Select>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    await waitUntilElementExists(page, callback, selector);

    type Value = [string, string, boolean];
    const content: Value[] = await invokeOnPageWithSelector(
        page,
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
    page?: Page,
) {
    const content = await getProperty(call, callback, page);
    callback(null, stringResponse(content));
}

export async function getBoolProperty(
    call: ServerUnaryCall<Request.ElementProperty>,
    callback: sendUnaryData<Response.Bool>,
    page?: Page,
) {
    const content = await getProperty(call, callback, page);
    callback(null, boolResponse(content || false));
}

async function getProperty<T>(call: ServerUnaryCall<Request.ElementProperty>, callback: sendUnaryData<T>, page?: Page) {
    const selector = call.request.getSelector();
    await waitUntilElementExists(page, callback, selector);
    const element = await invokeOnPageWithSelector(page, callback, '$', selector);
    try {
        const propertyName = call.request.getProperty();
        const property = await element.getProperty(propertyName);
        const content = await property.jsonValue();
        console.log(`Retrieved dom property for element ${selector} containing ${content}`);
        return content;
    } catch (e) {
        callback(e, null);
    }
}

export async function getViewportSize<T>(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.String>,
    page?: Page,
): Promise<void> {
    const result = await invokeOnPage(page, callback, 'viewportSize');
    callback(null, stringResponse(JSON.stringify(result)));
}
