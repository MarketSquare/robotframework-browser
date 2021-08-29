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

import * as path from 'path';
import { ElementHandle, Frame, Page } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { determineElement, invokePlaywrightMethod, waitUntilElementExists } from './playwirght-invoke';
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
export async function getElement(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.String> {
    await waitUntilElementExists(state, request.getSelector());
    const handle = await invokePlaywrightMethod(state, '$', request.getSelector());
    const id = uuidv4();
    state.addElement(id, handle);
    return stringResponse(`element=${id}`, 'Element found successfully.');
}

/** Resolve a list of elementHandles, create global UUIDs for them, and store the
 * references in global state. Enables using special selector syntax `element=<uuid>`
 * in RF keywords.
 */
export async function getElements(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Json> {
    await waitUntilElementExists(state, request.getSelector());
    const handles: ElementHandle[] = await invokePlaywrightMethod(state, '$$', request.getSelector());

    const response: string[] = handles.map((handle) => {
        const id = uuidv4();
        state.addElement(id, handle);
        return `element=${id}`;
    });
    return jsonResponse(JSON.stringify(response), 'Elements found successfully.');
}

export async function executeJavascript(
    request: Request.JavascriptCode,
    state: PlaywrightState,
    page: Page,
): Promise<Response.JavascriptExecutionResult> {
    const selector = request.getSelector();
    let script = request.getScript();
    let elem;
    try {
        script = eval(script);
    } catch (error) {
        logger.info(`On executeJavascript, supress ${error} for eval.`);
    }
    if (selector) {
        elem = await determineElement(state, selector);
    }
    const result = await page.evaluate(script, elem);
    return jsResponse(result as string, 'JavaScript executed successfully.');
}

export async function getPageState(page: Page): Promise<Response.JavascriptExecutionResult> {
    const result = await page.evaluate(() => window.__RFBROWSER__);
    return jsResponse(result, 'Page state evaluated successfully.');
}

export async function waitForElementState(
    request: Request.ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const options = JSON.parse(request.getOptions());
    await invokePlaywrightMethod(state, 'waitForSelector', selector, options);
    return emptyWithLog('Wait for Element with selector: ' + selector);
}

export async function waitForFunction(
    request: Request.WaitForFunctionOptions,
    state: PlaywrightState,
    page: Page,
): Promise<Response.Json> {
    let script = request.getScript();
    const selector = request.getSelector();
    const options = JSON.parse(request.getOptions());
    logger.info(`unparsed args: ${script}, ${request.getSelector()}, ${request.getOptions()}`);

    let elem;
    try {
        script = eval(script);
    } catch (error) {
        logger.info(`On waitForFunction, supress ${error} for eval.`);
    }
    if (selector) {
        elem = await determineElement(state, selector);
        script = eval(script);
    }

    // TODO: This might behave weirdly if element selector points to a different page
    const result = await page.waitForFunction(script, elem, options);
    return jsonResponse(JSON.stringify(result.jsonValue), 'Wait For Function completed succesfully.');
}

export async function addStyleTag(request: Request.StyleTag, page: Page): Promise<Response.Empty> {
    const content = request.getContent();
    await page.addStyleTag({ content });
    return emptyWithLog('added Style: ' + content);
}

export async function recordSelector(
    request: Request.RecordingParams,
    state: PlaywrightState,
): Promise<Response.JavascriptExecutionResult> {
    const page = state.getActivePage() as Page;
    await page.bringToFront();
    const frameSelector = request.getSelector();
    let result = '';
    if (frameSelector && frameSelector.length) {
        const frameHandle = await determineElement(state, frameSelector);
        const frame = await frameHandle?.contentFrame();
        if (!frame) {
            return jsResponse('', 'Frame selection fails');
        }
        result = frameSelector + ' >>> ' + (await recordSelectorIterator(request.getLabel(), frame));
    } else {
        result = await recordSelectorIterator(request.getLabel(), page);
    }
    return jsResponse(result, 'Selector recorded.');
}

async function recordSelectorIterator(label: string, frame: Frame | Page): Promise<string> {
    await frame.addScriptTag({
        type: 'module',
        path: path.join(__dirname, '/static/selector-finder.js'),
    });
    return await frame.evaluate((label) => {
        function rafAsync() {
            return new Promise((resolve) => {
                requestAnimationFrame(resolve); //faster than set time out
            });
        }

        // @ts-ignore
        function waitUntilRecorderAvailable() {
            // @ts-ignore
            if (!window.selectorRecorderFindSelector) {
                return rafAsync().then(() => waitUntilRecorderAvailable());
            } else {
                // @ts-ignore
                return Promise.resolve(window.selectorRecorderFindSelector(label));
            }
        }

        return waitUntilRecorderAvailable();
    }, label);
}

export async function highlightElements(
    request: Request.ElementSelectorWithDuration,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const duration = request.getDuration();
    const width = request.getWidth();
    const style = request.getStyle();
    const color = request.getColor();
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
            d.style.border = `${options?.wdt ?? '1px'} ${options?.stl ?? `dotted`} ${options?.clr ?? `blue`}`;
            document.body.appendChild(d);
            setTimeout(() => {
                d.remove();
            }, options?.dur ?? 5000);
        });
    };
    await invokePlaywrightMethod(state, '$$eval', selector, highlighter, {
        dur: duration,
        wdt: width,
        stl: style,
        clr: color,
    });
    return emptyWithLog(`Highlighted elements for ${duration}.`);
}

export async function download(request: Request.Url, state: PlaywrightState): Promise<Response.Json> {
    const browserState = state.activeBrowser;
    if (browserState === undefined) {
        throw new Error('Download requires an active browser');
    }
    const context = browserState.context;
    if (context === undefined) {
        throw new Error('Download requires an active context');
    }
    if (!(context.options?.acceptDownloads ?? false)) {
        throw new Error('Context acceptDownloads is false');
    }
    const page = state.getActivePage();
    if (page === undefined) {
        throw new Error('Download requires an active page');
    }
    const urlString = request.getUrl();
    const script = (urlString: string): Promise<string | void> => {
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
    const fileName = (await downloadStarted).suggestedFilename();
    logger.info('Suggested file name: ' + fileName + ' and save as path: ' + path);
    return jsonResponse(
        JSON.stringify({ saveAs: path, suggestedFilename: fileName }),
        'Url content downloaded to a file: ' + path,
    );
}
