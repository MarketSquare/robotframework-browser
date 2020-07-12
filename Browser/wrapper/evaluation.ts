import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { invokeOnPage, invokeOnPageWithSelector } from './playwirght-util';
import { emptyWithLog, jsResponse } from './response-util';

declare global {
    interface Window {
        __SET_RFBROWSER_STATE__: <T>(a: T) => T;
        __RFBROWSER__: any;
    }
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
    page?: Page,
) {
    const selector = call.request.getSelector();
    const options = JSON.parse(call.request.getOptions());
    await invokeOnPageWithSelector(page, callback, 'waitForSelector', selector, options);
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
    page?: Page,
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
    await invokeOnPageWithSelector(page, callback, '$$eval', selector, highlighter, duration);
}
