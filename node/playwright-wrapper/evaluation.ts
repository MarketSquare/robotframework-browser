import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Page, ElementHandle } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import { Request, Response } from './generated/playwright_pb';
import { invokeOnPage, invokePlaywirghtMethod, waitUntilElementExists } from './playwirght-invoke';
import { emptyWithLog, jsResponse, stringResponse } from './response-util';
import { PlaywrightState } from './playwright-state';

declare global {
    interface Window {
        __SET_RFBROWSER_STATE__: <T>(a: T) => T;
        __RFBROWSER__: any;
    }
}

/** Resolve an elementHandle, create global UUID for it, and store the reference
 * in global state. Enables using special selector syntax `element=<uuid>` in
 * RF keywords.
 */
export async function getElement(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
) {
    await waitUntilElementExists(state, callback, call.request.getSelector());
    const handle = await invokePlaywirghtMethod(state, callback, '$', call.request.getSelector());
    const id = uuidv4();
    state.addElement(id, handle);
    callback(null, stringResponse(`element=${id}`));
}

/** Resolve a list of elementHandles, create global UUIDs for them, and store the
 * references in global state. Enables using special selector syntax `element=<uuid>`
 * in RF keywords.
 */
export async function getElements(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
) {
    await waitUntilElementExists(state, callback, call.request.getSelector());
    const handles = await invokePlaywirghtMethod(state, callback, '$$', call.request.getSelector());

    const response = handles.map((handle: ElementHandle) => {
        const id = uuidv4();
        state.addElement(id, handle);
        return `element=${id}`;
    });
    callback(null, stringResponse(JSON.stringify(response)));
}

export async function executeJavascriptOnPage(
    call: ServerUnaryCall<Request.JavascriptCode>,
    callback: sendUnaryData<Response.JavascriptExecutionResult>,
    page?: Page,
) {
    const result = await invokeOnPage(page, callback, 'evaluate', call.request.getScript());
    callback(null, jsResponse(result));
}

export async function getPageState(callback: sendUnaryData<Response.JavascriptExecutionResult>, page?: Page) {
    const result = await invokeOnPage(page, callback, 'evaluate', () => window.__RFBROWSER__);
    callback(null, jsResponse(result));
}

export async function waitForElementState(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const options = JSON.parse(call.request.getOptions());
    await invokePlaywirghtMethod(state, callback, 'waitForSelector', selector, options);
    callback(null, emptyWithLog('Wait for Element with selector: ' + selector));
}

export async function waitForFunction(
    call: ServerUnaryCall<Request.WaitForFunctionOptions>,
    callback: sendUnaryData<Response.String>,
    page?: Page,
): Promise<void> {
    const script = call.request.getScript();
    const args = call.request.getArgs();
    const options = JSON.parse(call.request.getOptions());
    const result = await invokeOnPage(page, callback, 'waitForFunction', script, args || undefined, options);
    callback(null, stringResponse(result.jsonValue()));
    return;
}

export async function addStyleTag(
    call: ServerUnaryCall<Request.StyleTag>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const content = call.request.getContent();
    await invokeOnPage(page, callback, 'addStyleTag', { content: content });
    callback(null, emptyWithLog('added Style: ' + content));
}

export async function highlightElements(
    call: ServerUnaryCall<Request.ElementSelectorWithDuration>,
    callback: sendUnaryData<Response.JavascriptExecutionResult>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const duration = call.request.getDuration();
    const highlighter = (elements: Array<Element>, duration: number) => {
        elements.forEach((e: Element) => {
            const d = document.createElement('div');
            d.appendChild(document.createTextNode(''));
            d.style.position = 'fixed';
            const rect = e.getBoundingClientRect();
            d.style.top = '' + rect.top + 'px';
            d.style.left = '' + rect.left + 'px';
            d.style.width = '' + rect.width + 'px';
            d.style.height = '' + rect.height + 'px';
            d.style.border = '1px solid red';
            document.body.appendChild(d);
            setTimeout(() => {
                d.remove();
            }, duration);
        });
    };
    await invokePlaywirghtMethod(state, callback, '$$eval', selector, highlighter, duration);
}
