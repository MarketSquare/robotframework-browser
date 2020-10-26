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
import { Server, ServerUnaryCall, sendUnaryData } from 'grpc';
import { v4 as uuidv4 } from 'uuid';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { determineElement, invokeOnPage, invokePlaywrightMethod, waitUntilElementExists } from './playwirght-invoke';
import { emptyWithLog, jsResponse, jsonResponse, stringResponse } from './response-util';

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
    try {
        await waitUntilElementExists(state, call.request.getSelector());
        const handle = await invokePlaywrightMethod(state, '$', call.request.getSelector());
        const id = uuidv4();
        state.addElement(id, handle);
        callback(null, stringResponse(`element=${id}`, 'Element found successfully.'));
    } catch (e) {
        callback(e, null);
    }
}

/** Resolve a list of elementHandles, create global UUIDs for them, and store the
 * references in global state. Enables using special selector syntax `element=<uuid>`
 * in RF keywords.
 */
export async function getElements(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Json>,
    state: PlaywrightState,
) {
    try {
        await waitUntilElementExists(state, call.request.getSelector());
        const handles: ElementHandle[] = await invokePlaywrightMethod(state, '$$', call.request.getSelector());

        const response: string[] = handles.map((handle) => {
            const id = uuidv4();
            state.addElement(id, handle);
            return `element=${id}`;
        });
        callback(null, jsonResponse(JSON.stringify(response), 'Elements found succesfully.'));
    } catch (e) {
        callback(e, null);
    }
}

export async function executeJavascript(
    call: ServerUnaryCall<Request.JavascriptCode>,
    callback: sendUnaryData<Response.JavascriptExecutionResult>,
    state: PlaywrightState,
) {
    try {
        const selector = call.request.getSelector();
        let script = call.request.getScript();
        let elem;
        if (selector) {
            elem = await determineElement(state, selector);
            script = eval(script);
        }
        const result = await invokeOnPage(state.getActivePage(), 'evaluate', script, elem);
        callback(null, jsResponse(result, 'JavaScript executed successfully.'));
    } catch (e) {
        callback(e, null);
    }
}

export async function getPageState(callback: sendUnaryData<Response.JavascriptExecutionResult>, page?: Page) {
    const result = await invokeOnPage(page, 'evaluate', () => window.__RFBROWSER__);
    callback(null, jsResponse(result, 'Page state evaluated successfully.'));
}

export async function waitForElementState(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    try {
        const selector = call.request.getSelector();
        const options = JSON.parse(call.request.getOptions());
        await invokePlaywrightMethod(state, 'waitForSelector', selector, options);
        callback(null, emptyWithLog('Wait for Element with selector: ' + selector));
    } catch (e) {
        callback(e, null);
    }
}

export async function waitForFunction(
    call: ServerUnaryCall<Request.WaitForFunctionOptions>,
    state: PlaywrightState,
): Promise<Response.Json> {
    let script = call.request.getScript();
    const selector = call.request.getSelector();
    const options = JSON.parse(call.request.getOptions());
    logger.info(`unparsed args: ${script}, ${call.request.getSelector()}, ${call.request.getOptions()}`);

    let elem;
    if (selector) {
        elem = await determineElement(state, selector);
        script = eval(script);
    }

    // TODO: This might behave weirdly if element selector points to a different page
    const result = await invokeOnPage(state.getActivePage(), 'waitForFunction', script, elem, options);
    return jsonResponse(JSON.stringify(result.jsonValue), 'Wait For Fcuntion completed succesfully.');
}

export async function addStyleTag(
    call: ServerUnaryCall<Request.StyleTag>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const content = call.request.getContent();
    await invokeOnPage(page, 'addStyleTag', { content: content });
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
    await invokePlaywrightMethod(state, '$$eval', selector, highlighter, {
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
    const browserState = state.activeBrowser;
    if (browserState === undefined) {
        callback(Error('Download requires an active browser'), stringResponse('', 'No browser is active'));
        return;
    }
    const context = browserState.context;
    if (context === undefined) {
        callback(Error('Download requires an active context'), stringResponse('', 'No context is active'));
        return;
    }
    if (!(context.options?.acceptDownloads ?? false)) {
        callback(Error('Context acceptDownloads is false'), stringResponse('', 'Context does not allow downloads'));
        return;
    }
    const page = state.getActivePage();
    if (page === undefined) {
        callback(Error('Download requires an active page'), stringResponse('', 'No page is active'));
        return;
    }
    const urlString = call.request.getUrl();
    const script = (urlString: string) => {
        return fetch(urlString)
            .then((resp) => {
                return resp.blob();
            })
            .then((blob) => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = urlString;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                return a.download;
            });
    };
    const downloadStarted = page.waitForEvent('download');
    await page.evaluate(script, urlString);
    const path = await (await downloadStarted).path();
    callback(null, stringResponse(path || '', 'Url content downloaded to a file'));
}
