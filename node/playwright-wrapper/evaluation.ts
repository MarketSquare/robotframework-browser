import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Page } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import * as pb from './generated/playwright_pb';
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
    call: ServerUnaryCall<pb.Request.ElementSelector>,
    callback: sendUnaryData<pb.Response.String>,
    state: PlaywrightState,
) {
    await waitUntilElementExists(state, callback, call.request.getSelector());
    const handle = await invokePlaywirghtMethod(state, callback, '$', call.request.getSelector());
    const id = uuidv4();
    state.addElement(id, handle);
    callback(null, stringResponse(id));
}

export async function executeJavascriptOnPage(
    call: ServerUnaryCall<pb.Request.JavascriptCode>,
    callback: sendUnaryData<pb.Response.JavascriptExecutionResult>,
    page?: Page,
) {
    const result = await invokeOnPage(page, callback, 'evaluate', call.request.getScript());
    callback(null, jsResponse(result));
}

export async function getPageState(callback: sendUnaryData<pb.Response.JavascriptExecutionResult>, page?: Page) {
    const result = await invokeOnPage(page, callback, 'evaluate', () => window.__RFBROWSER__);
    callback(null, jsResponse(result));
}

export async function waitForElementState(
    call: ServerUnaryCall<pb.Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<pb.Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const options = JSON.parse(call.request.getOptions());
    await invokePlaywirghtMethod(state, callback, 'waitForSelector', selector, options);
    callback(null, emptyWithLog('Wait for Element with selector: ' + selector));
}

export async function addStyleTag(
    call: ServerUnaryCall<pb.Request.StyleTag>,
    callback: sendUnaryData<pb.Response.Empty>,
    page?: Page,
) {
    const content = call.request.getContent();
    await invokeOnPage(page, callback, 'addStyleTag', { content: content });
    callback(null, emptyWithLog('added Style: ' + content));
}

export async function highlightElements(
    call: ServerUnaryCall<pb.Request.ElementSelectorWithDuration>,
    callback: sendUnaryData<pb.Response.JavascriptExecutionResult>,
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

export async function httpRequest(
    call: ServerUnaryCall<pb.Request.HttpRequest>,
    callback: sendUnaryData<pb.Response.String>,
    page?: Page,
) {
    const opts: { [k: string]: any } = {
        method: call.request.getMethod(),
        url: call.request.getUrl(),
        headers: JSON.parse(call.request.getHeaders()),
    };
    if (opts.method != 'GET') {
        opts.body = call.request.getBody();
    }
    try {
        const response = await page?.evaluate(({ url, method, body, headers }) => {
            return fetch(url, { method, body, headers }).then((data: Response) => {
                return data.text().then((body) => {
                    const headers: { [k: string]: any } = {};
                    data.headers.forEach((value, name) => (headers[name] = value));
                    return {
                        status: data.status,
                        body: body,
                        headers: JSON.stringify(headers),
                        type: data.type,
                        statusText: data.statusText,
                        url: data.url,
                        ok: data.ok,
                        redirected: data.redirected,
                    };
                });
            });
        }, opts);
        callback(null, stringResponse(JSON.stringify(response)));
    } catch (e) {
        callback(e, null);
    }
}
