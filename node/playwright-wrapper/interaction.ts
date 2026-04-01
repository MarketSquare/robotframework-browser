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

import { Dialog, Page } from 'playwright';

import { logger } from './browser_logger';
import * as pb from './generated/playwright';
import { getSelections } from './getters';
import { exists } from './playwright-invoke';
import { findLocator, invokeOnKeyboard, invokeOnMouse } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog } from './response-util';

export async function selectOption(
    request: pb.Request_SelectElementSelector,
    state: PlaywrightState,
): Promise<pb.Response_Select> {
    const selector = request.selector;
    const matcher = JSON.parse(request.matcherJson);
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    const result = await locator.selectOption(matcher);
    if (result.length == 0) {
        logger.info("Couldn't select any options");
        throw new Error(`No options matched ${matcher}`);
    }
    return await getSelections(locator);
}

export async function deSelectOption(
    request: pb.Request_ElementSelector,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const strictMode = request.strict;
    const locator = findLocator(state, selector, strictMode, undefined, true);
    await (await locator).selectOption([]);
    return emptyWithLog(`Deselected options in element ${selector}`);
}

export async function typeText(request: pb.Request_TypeText, state: PlaywrightState): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const text = request.text;
    const delayValue = request.delay;
    const clear = request.clear;
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    if (clear) {
        await locator.fill('');
    }
    await locator.type(text, { delay: delayValue });
    return emptyWithLog(`Typed text "${text}" on "${selector}"`);
}

export async function fillText(request: pb.Request_FillText, state: PlaywrightState): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const text = request.text;
    const strictMode = request.strict;
    const force = request.force;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.fill(text, { force: force });
    return emptyWithLog(`Fill text ${text} on ${selector} with force: ${force}`);
}

export async function clearText(request: pb.Request_ClearText, state: PlaywrightState): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.fill('');
    return emptyWithLog(`Text ${selector} field cleared.`);
}

export async function press(request: pb.Request_PressKeys, state: PlaywrightState): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const keyList = request.key;
    const strictMode = request.strict;
    const pressDelay = request.pressDelay;
    const keyDelay = request.keyDelay;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    for (const i of keyList) {
        await locator.press(i, { delay: pressDelay });
        if (keyDelay > 0) {
            await new Promise((r) => setTimeout(r, keyDelay));
        }
    }
    return emptyWithLog(`Pressed keys: "${keyList.join(', ')}" on ${selector} `);
}

export async function click(
    request: pb.Request_ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const options = request.options;
    const strictMode = request.strict;
    const result = await internalClick(selector, strictMode, options, state);
    if (result) {
        return emptyWithLog(`Clicked element: '${selector}' with options: '${options}' successfully.`);
    }
    return emptyWithLog(
        `Clicked element: '${selector}' with options: '${options}' but silenced: "Target closed error".`,
    );
}

export async function tap(
    request: pb.Request_ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const options = request.options;
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.tap(JSON.parse(options));
    return emptyWithLog(`Tap element: '${selector}' with options: '${options}'`);
}

export async function internalClick(
    selector: string,
    strictMode: boolean,
    options: string,
    state: PlaywrightState,
): Promise<boolean> {
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    try {
        await locator.click(JSON.parse(options));
        return true;
    } catch (error: unknown) {
        if (
            error instanceof Error &&
            error.message.startsWith('locator.click: Target page, context or browser has been closed')
        ) {
            logger.warn('Supress locator.click: Target page, context or browser has been closed error');
            return false;
        }
        throw error;
    }
}

export async function hover(
    request: pb.Request_ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const options = request.options;
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.hover(JSON.parse(options));
    return emptyWithLog(`Hovered element: '${selector}' With options: '${options}'`);
}

export async function focus(request: pb.Request_ElementSelector, state: PlaywrightState): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.focus();
    return emptyWithLog(`Focused element: ${selector}`);
}

export async function checkCheckbox(
    request: pb.Request_ElementSelector,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const strictMode = request.strict;
    const force = request.force;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.waitFor({ state: 'attached' });
    await locator.check({ force: force });
    return emptyWithLog(`Checked checkbox: ${selector} with force: ${force}`);
}

export async function uncheckCheckbox(
    request: pb.Request_ElementSelector,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const strictMode = request.strict;
    const force = request.force;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.waitFor({ state: 'attached' });
    await locator.uncheck({ force: force });
    return emptyWithLog(`Unchecked checkbox: ${selector} with force: ${force}`);
}

export async function uploadFileBySelector(
    request: pb.Request_FileBySelector,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const strictMode = request.strict;
    const path = request.path;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    if (path.length === 0) {
        const name = request.name;
        const mimeType = request.mimeType;
        const buffer = request.buffer;
        logger.info(`Uploading file ${name} as buffer to ${selector}`);
        await locator.setInputFiles({ name: name, mimeType: mimeType, buffer: Buffer.from(buffer) });
        return emptyWithLog('Successfully uploaded buffer as file');
    } else {
        logger.info(`Uploading file(s) ${path.join(', ')} to ${selector}`);
        await locator.setInputFiles(path);
        return emptyWithLog('Successfully uploaded file(s)');
    }
}

export async function uploadFile(request: pb.Request_FilePath, page: Page): Promise<pb.Response_Empty> {
    const path = request.path;
    const fileChooser = await page.waitForEvent('filechooser');
    await fileChooser.setFiles(path);
    return emptyWithLog('Successfully uploaded file');
}

export async function handleAlert(request: pb.Request_AlertAction, page: Page): Promise<pb.Response_Empty> {
    const alertAction = request.alertAction as 'accept' | 'dismiss';
    const promptInput = request.promptInput;
    const fn = async (dialog: Dialog) => {
        const dialogueText = dialog.message();
        if (promptInput) await dialog[alertAction](promptInput);
        else await dialog[alertAction]();
        logger.info(`Alert text: ${dialogueText}`);
    };
    page.on('dialog', fn);
    return emptyWithLog('Set event handler for next alert');
}

export async function waitForAlerts(request: pb.Request_AlertActions, page: Page): Promise<pb.Response_ListString> {
    const alertActions = request.items;
    const alertMessages = [];
    for (let index = 0; index < alertActions.length; index++) {
        const alertAction = alertActions[index];
        const promptInput = alertAction.promptInput;
        const timeout = alertAction.timeout;
        const action = alertAction.alertAction;
        logger.info(`Waiting for alert with action: ${action}, promptInput: "${promptInput}" and timeout: ${timeout}`);
        const dialogObject = await page.waitForEvent('dialog', { timeout: timeout });
        alertMessages.push(dialogObject.message());
        if (action === 'accept' && promptInput) {
            void dialogObject.accept(promptInput);
        } else if (alertAction.alertAction === 'accept') {
            void dialogObject.accept();
        } else {
            void dialogObject.dismiss();
        }
    }
    return { items: alertMessages };
}

export async function mouseButton(request: pb.Request_MouseButtonOptions, page?: Page): Promise<pb.Response_Empty> {
    const action = request.action as 'click' | 'up' | 'down';
    const params = JSON.parse(request.json);
    await invokeOnMouse(page, action, params);
    return emptyWithLog(`Successfully executed ${action}`);
}

export async function mouseMove(request: pb.Request_Json, page?: Page): Promise<pb.Response_Empty> {
    const params = JSON.parse(request.body);
    await invokeOnMouse(page, 'move', params);
    return emptyWithLog(`Successfully moved mouse to ${params.x}, ${params.y}`);
}

export async function mouseWheel(request: pb.Request_MouseWheel, page?: Page): Promise<pb.Response_Empty> {
    const deltaX = request.deltaX;
    const deltaY = request.deltaY;
    exists(page, `but no open page`);
    await page?.mouse.wheel(deltaX, deltaY);
    return emptyWithLog(`Successfully scrolled mouse wheel with ${deltaX}, ${deltaY}`);
}

export async function keyboardKey(request: pb.Request_KeyboardKeypress, page: Page): Promise<pb.Response_Empty> {
    const action = request.action as 'down' | 'up' | 'press';
    const key = request.key;
    await invokeOnKeyboard(page, action, key);
    return emptyWithLog(`Successfully did ${action} for ${key}`);
}

export async function keyboardInput(request: pb.Request_KeyboardInputOptions, page: Page): Promise<pb.Response_Empty> {
    const action = request.action as 'insertText' | 'type';
    const delay = request.delay;
    const input = request.input;

    await invokeOnKeyboard(page, action, input, { delay: delay });
    return emptyWithLog(`Successfully did virtual keyboard action ${action} with input ${input}`);
}

export async function scrollToElement(
    request: pb.Request_ElementSelector,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const selector = request.selector;
    const strictMode = request.strict;
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.scrollIntoViewIfNeeded();
    return emptyWithLog(`Scrolled to ${selector} field if needed.`);
}
