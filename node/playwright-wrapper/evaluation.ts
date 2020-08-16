import { ElementHandle, Page } from 'playwright';
import { Server, ServerUnaryCall, sendUnaryData } from 'grpc';
import { v4 as uuidv4 } from 'uuid';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { determineElement, invokeOnPage, invokePlaywrightMethod, waitUntilElementExists } from './playwirght-invoke';
import { emptyWithLog, jsResponse, stringResponse } from './response-util';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

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
    const handle = await invokePlaywrightMethod(state, callback, '$', call.request.getSelector());
    const id = uuidv4();
    state.addElement(id, handle);
    callback(null, stringResponse(`element=${id}`, 'Element found successfully.'));
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
    const handles: ElementHandle[] = await invokePlaywrightMethod(state, callback, '$$', call.request.getSelector());

    const response: string[] = handles.map((handle) => {
        const id = uuidv4();
        state.addElement(id, handle);
        return `element=${id}`;
    });
    callback(null, stringResponse(JSON.stringify(response), 'Elements found succesfully.'));
}

export async function executeJavascript(
    call: ServerUnaryCall<Request.JavascriptCode>,
    callback: sendUnaryData<Response.JavascriptExecutionResult>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    let script = call.request.getScript();
    let elem;
    if (selector) {
        elem = await determineElement(state, selector, callback);
        script = eval(script);
    }

    const result = await invokeOnPage(state.getActivePage(), callback, 'evaluate', script, elem);
    callback(null, jsResponse(result, 'JavaScript executed successfully.'));
}

export async function getPageState(callback: sendUnaryData<Response.JavascriptExecutionResult>, page?: Page) {
    const result = await invokeOnPage(page, callback, 'evaluate', () => window.__RFBROWSER__);
    callback(null, jsResponse(result, 'Page state evaluated successfully.'));
}

export async function waitForElementState(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const options = JSON.parse(call.request.getOptions());
    await invokePlaywrightMethod(state, callback, 'waitForSelector', selector, options);
    callback(null, emptyWithLog('Wait for Element with selector: ' + selector));
}

export async function waitForFunction(
    call: ServerUnaryCall<Request.WaitForFunctionOptions>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
): Promise<void> {
    let script = call.request.getScript();
    const selector = call.request.getSelector();
    const options = JSON.parse(call.request.getOptions());
    logger.info(`unparsed args: ${script}, ${call.request.getSelector()}, ${call.request.getOptions()}`);

    let elem;
    if (selector) {
        elem = await determineElement(state, selector, callback);
        script = eval(script);
    }

    // TODO: This might behave weirdly if element selector points to a different page
    const result = await invokeOnPage(state.getActivePage(), callback, 'waitForFunction', script, elem, options);
    callback(null, stringResponse(JSON.stringify(result.jsonValue), ''));
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
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const duration = call.request.getDuration();
    const width = call.request.getWidth();
    const style = call.request.getStyle();
    const color = call.request.getColor();
    const highlighter = (elements: Array<Element>, options: any) => {
        elements.forEach((e: Element) => {
            const d = document.createElement('div');
            d.className = 'robotframework-browser-highlight';
            d.appendChild(document.createTextNode(''));
            d.style.position = 'fixed';
            const rect = e.getBoundingClientRect();
            d.style.top = `${rect.top}px`;
            d.style.left = `${rect.left}px`;
            d.style.width = `${rect.width}px`;
            d.style.height = `${rect.height}px`;
            d.style.border = `${options.wdt} ${options.stl} ${options.clr}`;
            document.body.appendChild(d);
            setTimeout(() => {
                d.remove();
            }, options.dur);
        });
    };
    await invokePlaywrightMethod(state, callback, '$$eval', selector, highlighter, {
        dur: duration,
        wdt: width,
        stl: style,
        clr: color,
    });
    callback(null, emptyWithLog(`Highlighted elements for ${duration}.`));
}

export async function download(
    call: ServerUnaryCall<Request.Url>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
) {
    const urlString = call.request.getUrl();
    const script = (urlString: string) => {
        console.log('1. Download script started');
        console.log(urlString);
        return fetch(urlString)
            .then((resp) => {
                console.log('2. Download scriptus');
                return resp.blob();
            })
            .then((blob) => {
                console.log('3. Download scriptus');
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = '';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                console.log('4. Download scriptus');
                return a.download;
            });
    };
    const result = await state.getActivePage()?.evaluate(script, urlString);
    callback(null, stringResponse(result ?? '', 'Url content downloaded to a file'));
}
