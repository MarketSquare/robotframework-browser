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
import { Frame, FrameLocator, Locator, Page } from 'playwright';

import { logger } from './browser_logger';
import * as pb from './generated/playwright';
import { _waitForDownload } from './network';
import { exists, findLocator } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import {
    emptyWithLog,
    intResponse,
    jsonResponse,
    jsResponse,
    parseRegExpOrKeepString,
    stringResponse,
} from './response-util';

/** Resolve an Locator, create global UUID for it, and store the reference
 * in global state. Enables using special selector syntax `element=<uuid>` in
 * RF keywords.
 */
export async function getElement(
    request: pb.Request_ElementSelector,
    state: PlaywrightState,
): Promise<pb.Response_String> {
    const strictMode = request.strict;
    const selector = request.selector;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.waitFor({ state: 'attached' });

    // @ts-ignore
    return stringResponse(locator._selector, 'Locator found successfully.');
}

/** Resolve a list of Locator, create global UUIDs for them, and store the
 * references in global state. Enables using special selector syntax `element=<uuid>`
 * in RF keywords.
 */
export async function getElements(
    request: pb.Request_ElementSelector,
    state: PlaywrightState,
): Promise<pb.Response_Json> {
    const selector = request.selector;
    const locator = await findLocator(state, selector, false, undefined, false);
    logger.info(`Wait element to reach attached state.`);
    try {
        await locator.first().waitFor({ state: 'attached' });
    } catch (e) {
        logger.debug(`Attached state not reached, suppress error: ${String(e)}.`);
    }
    const allLocators = await locator.all();
    logger.info(`Found ${allLocators.length} elements.`);

    // @ts-ignore
    const allSelectors = allLocators.map((locator) => locator._selector);
    return jsonResponse(JSON.stringify(allSelectors), `Found ${allLocators.length} Locators successfully.`);
}

type AriaRole =
    | 'alert'
    | 'alertdialog'
    | 'application'
    | 'article'
    | 'banner'
    | 'blockquote'
    | 'button'
    | 'caption'
    | 'cell'
    | 'checkbox'
    | 'code'
    | 'columnheader'
    | 'combobox'
    | 'complementary'
    | 'contentinfo'
    | 'definition'
    | 'deletion'
    | 'dialog'
    | 'directory'
    | 'document'
    | 'emphasis'
    | 'feed'
    | 'figure'
    | 'form'
    | 'generic'
    | 'grid'
    | 'gridcell'
    | 'group'
    | 'heading'
    | 'img'
    | 'insertion'
    | 'link'
    | 'list'
    | 'listbox'
    | 'listitem'
    | 'log'
    | 'main'
    | 'marquee'
    | 'math'
    | 'meter'
    | 'menu'
    | 'menubar'
    | 'menuitem'
    | 'menuitemcheckbox'
    | 'menuitemradio'
    | 'navigation'
    | 'none'
    | 'note'
    | 'option'
    | 'paragraph'
    | 'presentation'
    | 'progressbar'
    | 'radio'
    | 'radiogroup'
    | 'region'
    | 'row'
    | 'rowgroup'
    | 'rowheader'
    | 'scrollbar'
    | 'search'
    | 'searchbox'
    | 'separator'
    | 'slider'
    | 'spinbutton'
    | 'status'
    | 'strong'
    | 'subscript'
    | 'superscript'
    | 'switch'
    | 'tab'
    | 'table'
    | 'tablist'
    | 'tabpanel'
    | 'term'
    | 'textbox'
    | 'time'
    | 'timer'
    | 'toolbar'
    | 'tooltip'
    | 'tree'
    | 'treegrid'
    | 'treeitem';

export async function getByX(request: pb.Request_GetByOptions, state: PlaywrightState): Promise<pb.Response_Json> {
    const strategy = request.strategy;
    const text = parseRegExpOrKeepString(request.text);
    const options = JSON.parse(request.options);
    const strictMode = request.strict;
    const allElements = request.all;
    const frameSelector = request.frameSelector;
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    let document: Page | FrameLocator = activePage;
    if (frameSelector) {
        document = activePage.frameLocator(frameSelector);
        if (!strictMode) {
            document = document.first();
        }
    }
    let locator: Locator;
    switch (strategy) {
        case 'AltText': {
            locator = document.getByAltText(text, options);
            break;
        }
        case 'Label': {
            locator = document.getByLabel(text, options);
            break;
        }
        case 'Placeholder': {
            locator = document.getByPlaceholder(text, options);
            break;
        }
        case 'Role': {
            if (options?.name) {
                options.name = parseRegExpOrKeepString(options.name);
            }
            locator = document.getByRole(text as AriaRole, options);
            break;
        }
        case 'TestId': {
            locator = document.getByTestId(text);
            break;
        }
        case 'Text': {
            locator = document.getByText(text, options);
            break;
        }
        case 'Title': {
            locator = document.getByTitle(text, options);
            break;
        }
        default: {
            throw new Error(`Strategy ${strategy} not supported.`);
        }
    }
    if (!allElements) {
        if (!strictMode) {
            locator = locator.first();
        }
        await locator.waitFor({ state: 'attached' });

        // @ts-ignore
        return jsonResponse(JSON.stringify(locator._selector), 'Locator found successfully.');
    }
    let allSelectors: string[] = [];
    try {
        await locator.first().waitFor({ state: 'attached' });

        // @ts-ignore
        allSelectors = await locator.all().then((locators) => locators.map((loc) => loc._selector));
    } catch (e) {
        logger.debug(`Attached state not reached, suppress error: ${String(e)}.`);
    }
    return jsonResponse(JSON.stringify(allSelectors), `${allSelectors.length} locators found successfully.`);
}

const tryToTransformStringToFunction = (str: string): string | (() => unknown) => {
    try {
        // eslint-disable-next-line @typescript-eslint/no-implied-eval
        return new Function('return ' + str)();
    } catch (ignored) {
        logger.debug(`Failed to transform string to function: ${String(ignored)}`);
        return str;
    }
};

export async function evaluateJavascript(
    request: pb.Request_EvaluateAll,
    state: PlaywrightState,
    page: Page,
): Promise<pb.Response_JavascriptExecutionResult> {
    const selector = request.selector;
    const script = tryToTransformStringToFunction(request.script);
    const strictMode = request.strict;
    const arg = JSON.parse(request.arg);
    const allElements = request.allElements;

    async function getJSResult() {
        if (selector !== '') {
            const locator = await findLocator(state, selector, strictMode, undefined, !allElements);
            if (allElements) {
                return await locator.evaluateAll(script, arg);
            }
            return await locator.evaluate(script, arg);
        }
        return await page.evaluate(script, arg);
    }

    return jsResponse((await getJSResult()) as string, 'JavaScript executed successfully.');
}

export async function waitForElementState(
    request: pb.Request_ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const { state: elementState, timeout } = JSON.parse(request.options);
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    if (
        elementState === 'detached' ||
        elementState === 'attached' ||
        elementState === 'hidden' ||
        elementState === 'visible'
    ) {
        await locator.waitFor({ state: elementState, timeout: timeout });
    } else {
        const element = await locator.elementHandle({ timeout: timeout });
        await element?.waitForElementState(elementState, { timeout: timeout });
    }
    return emptyWithLog(`Waited for Element with selector ${selector} at state ${elementState}`);
}

export async function waitForFunction(
    request: pb.Request_WaitForFunctionOptions,
    state: PlaywrightState,
    page: Page,
): Promise<pb.Response_Json> {
    const script = tryToTransformStringToFunction(request.script);
    const selector = request.selector;
    const options = JSON.parse(request.options);
    const strictMode = request.strict;
    logger.info(`unparsed args: ${request.script}, ${request.selector}, ${request.options}`);

    let elem;
    if (selector) {
        const locator = await findLocator(state, selector, strictMode, undefined, true);
        elem = await locator.elementHandle();
    }

    // TODO: This might behave weirdly if element selector points to a different page
    const result = await page.waitForFunction(script, elem, options);
    return jsonResponse(JSON.stringify(await result.jsonValue()), 'Wait For Function completed successfully.');
}

export async function addStyleTag(request: pb.Request_StyleTag, page: Page): Promise<pb.Response_Empty> {
    const content = request.content;
    await page.addStyleTag({ content });
    return emptyWithLog('added Style: ' + content);
}

const selectorsForPage: { [key: string]: unknown[] } = {};

export async function recordSelector(
    request: pb.Request_Label,
    state: PlaywrightState,
): Promise<pb.Response_JavascriptExecutionResult> {
    if (state.getActiveBrowser().headless) {
        throw Error('Record Selector works only with visible browser. Use Open Browser or New Browser  headless=False');
    }
    const activeBrowser = state.activeBrowser;
    if (!activeBrowser) {
        throw Error('No active browser.');
    }
    const indexedPage = activeBrowser.page;
    if (!indexedPage) {
        throw Error('No active page.');
    }
    const page = indexedPage.p;
    await page.bringToFront();
    // If the page already has recorder then skipping creation
    if (!(indexedPage.id in selectorsForPage)) {
        const myselectors: unknown[] = [];
        selectorsForPage[indexedPage.id] = myselectors;
        await page.exposeFunction('setRecordedSelector', (index: number, item: unknown) => {
            while (myselectors.length > index) {
                myselectors.pop();
            }
            myselectors.push(item);
        });
        await page.exposeFunction('getRecordedSelectors', () => {
            return myselectors;
        });
        await page.exposeFunction('highlightPWSelector', (selector: string) => {
            void highlightAll(selector, 1000, '3px', 'dotted', 'blue', false, state);
        });
    }

    const result = await recordSelectorIterator(request.label, page.mainFrame());
    // clean old recording array for the next run on the page
    while (selectorsForPage[indexedPage.id].length) {
        selectorsForPage[indexedPage.id].pop();
    }
    return jsResponse(result, 'Selector recorded.');
}

async function attachSelectorFinderScript(frame: Frame): Promise<void> {
    try {
        await frame.addScriptTag({
            type: 'module',
            path: path.join(__dirname, '/static/selector-finder.js'),
        });
    } catch (e) {
        throw new Error(
            `Adding selector recorder to page failed.\nTry New Context  bypassCSP=True and retry recording.`,
            { cause: e },
        );
    }
    await Promise.all(frame.childFrames().map((child) => attachSelectorFinderScript(child)));
}

async function attachSubframeListeners(subframe: Frame, index: number): Promise<void> {
    await subframe.evaluate((index) => {
        function rafAsync() {
            return new Promise((resolve) => {
                requestAnimationFrame(resolve); //faster than set time out
            });
        }

        // @ts-ignore
        function waitUntilRecorderAvailable() {
            // @ts-ignore
            if (!window.subframeSelectorRecorderFindSelector) {
                // @ts-ignore
                return rafAsync().then(() => waitUntilRecorderAvailable());
            } else {
                // @ts-ignore
                return Promise.resolve(window.subframeSelectorRecorderFindSelector(index));
            }
        }

        return waitUntilRecorderAvailable();
    }, index);
    await Promise.all(
        subframe
            .childFrames()
            .filter((f) => f.parentFrame() === subframe)
            .map((child) => attachSubframeListeners(child, index + 1)),
    );
}

async function recordSelectorIterator(label: string, frame: Frame): Promise<string> {
    await attachSelectorFinderScript(frame);
    await Promise.all(
        frame
            .childFrames()
            .filter((f) => f.parentFrame() === frame)
            .map((child) => attachSubframeListeners(child, 1)),
    );
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
                // @ts-ignore
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
    request: pb.Request_ElementSelectorWithDuration,
    state: PlaywrightState,
): Promise<pb.Response_Int> {
    const selector = request.selector;
    const duration = request.duration;
    const width = request.width;
    const style = request.style;
    const color = request.color;
    const strictMode = request.strict;
    const mode = request.mode;
    const count = await highlightAll(
        selector,
        duration,
        width,
        style,
        color,
        strictMode,
        state,
        mode as 'border' | 'playwright' | 'both',
    );
    const message = duration ? `Highlighted ${count} elements for ${duration} ms.` : `Highlighting ${count} elements`;
    return intResponse(count, message);
}

type EvaluationOptions = {
    dur: number;
    wdt: string;
    stl: string;
    clr: string;
};

async function highlightAll(
    selector: string,
    duration: number,
    width: string,
    style: string,
    color: string,
    strictMode: boolean,
    state: PlaywrightState,
    mode: 'border' | 'playwright' | 'both' = 'border',
): Promise<number> {
    const locator = await findLocator(state, selector, strictMode, undefined, false);
    let count: number;
    try {
        count = await locator.count();
    } catch (e) {
        logger.info(e);
        return 0;
    }
    logger.info(`Locator count is ${count}`);
    if (['playwright', 'both'].includes(mode)) {
        void locator.highlight();
        if (duration !== 0) {
            setTimeout(() => {
                void state.getActivePage()?.locator('none.highlight-no-element').highlight();
            }, duration);
        }
        if (mode === 'playwright') {
            return count;
        }
    }
    await locator.evaluateAll(
        (elements: Array<Element>, options: EvaluationOptions) => {
            elements.forEach((e: Element) => {
                const d = document.createElement('div');
                d.className = 'robotframework-browser-highlight';
                d.appendChild(document.createTextNode(''));
                d.style.position = 'fixed';
                const rect = e.getBoundingClientRect();
                d.style.zIndex = '2147483647';
                d.style.top = `calc(${rect.top}px - ${options?.wdt ?? '1px'})`;
                d.style.left = `calc(${rect.left}px - ${options?.wdt ?? '1px'})`;
                d.style.width = `${rect.width}px`;
                d.style.height = `${rect.height}px`;
                d.style.border = `${options?.wdt ?? '1px'} ${options?.stl ?? `dotted`} ${options?.clr ?? `blue`}`;
                d.style.boxSizing = 'content-box';
                document.body.appendChild(d);
                if (options?.dur !== 0) {
                    setTimeout(() => {
                        d.remove();
                    }, options?.dur ?? 5000);
                }
            });
        },
        { dur: duration, wdt: width, stl: style, clr: color },
    );
    return count;
}

export async function download(request: pb.Request_DownloadOptions, state: PlaywrightState): Promise<pb.Response_Json> {
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
    const urlString = request.url;
    const saveAs = request.path;
    const downloadTimeout = request.downloadTimeout;
    const waitForFinish = request.waitForFinish;
    const fromUrl = page.url();
    if (fromUrl === 'about:blank') {
        throw new Error('Download requires that the page has been navigated to an url');
    }
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
    const downloadStarted = _waitForDownload(page, state, saveAs, downloadTimeout, waitForFinish);
    logger.info(`Starting download from ${urlString} to ${saveAs}`);
    await page.evaluate(script, urlString);
    return await downloadStarted;
}
