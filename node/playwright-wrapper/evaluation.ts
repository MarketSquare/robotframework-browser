import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Page } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import { Response, Request } from './generated/playwright_pb';
import { invokeOnPage, invokePlaywirghtMethod, waitUntilElementExists } from './playwirght-util';
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
    const handle = await invokeOnPage(state.getActivePage(), callback, '$', call.request.getSelector());
    const id = uuidv4();
    state.addElement(id, handle);
    callback(null, stringResponse(id));
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
