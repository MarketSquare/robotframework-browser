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
import { exists } from './playwright-invoke';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog } from './response-util';
import { findLocator, invokeOnKeyboard, invokeOnMouse } from './playwright-invoke';
import { getSelections } from './getters';

import pino from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function selectOption(
    request: Request.SelectElementSelector,
    state: PlaywrightState,
): Promise<Response.Select> {
    const selector = request.getSelector();
    const matcher = JSON.parse(request.getMatcherjson());
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    const result = await locator.selectOption(matcher);
    if (result.length == 0) {
        logger.info("Couldn't select any options");
        throw new Error(`No options matched ${matcher}`);
    }
    return await getSelections(locator);
}

export async function deSelectOption(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = findLocator(state, selector, strictMode, undefined, true);
    await (await locator).selectOption([]);
    return emptyWithLog(`Deselected options in element ${selector}`);
}

export async function typeText(request: Request.TypeText, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const text = request.getText();
    const delayValue = request.getDelay();
    const clear = request.getClear();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    if (clear) {
        await locator.fill('');
    }
    await locator.type(text, { delay: delayValue });
    return emptyWithLog(`Typed text "${text}" on "${selector}"`);
}

export async function fillText(request: Request.FillText, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const text = request.getText();
    const strictMode = request.getStrict();
    const force = request.getForce();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.fill(text, { force: force });
    return emptyWithLog(`Fill text ${text} on ${selector} with force: ${force}`);
}

export async function clearText(request: Request.ClearText, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.fill('');
    return emptyWithLog(`Text ${selector} field cleared.`);
}

export async function press(request: Request.PressKeys, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const keyList = request.getKeyList();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    for (const i of keyList) {
        await locator.press(i);
    }
    return emptyWithLog(`Pressed keys: "${keyList}" on ${selector} `);
}

export async function click(
    request: Request.ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const options = request.getOptions();
    const strictMode = request.getStrict();
    const result = await internalClick(selector, strictMode, options, state);
    if (result) {
        return emptyWithLog(`Clicked element: '${selector}' with options: '${options}' successfully.`);
    }
    return emptyWithLog(
        `Clicked element: '${selector}' with options: '${options}' but silenced: "Target closed error".`,
    );
}

export async function tap(
    request: Request.ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const options = request.getOptions();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.tap(JSON.parse(options));
    return emptyWithLog(`Tab element: '${selector}' with options: '${options}'`);
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
    request: Request.ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const options = request.getOptions();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.hover(JSON.parse(options));
    return emptyWithLog(`Hovered element: '${selector}' With options: '${options}'`);
}

export async function focus(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.focus();
    return emptyWithLog(`Focused element: ${selector}`);
}

export async function checkCheckbox(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const force = request.getForce();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.waitFor({ state: 'attached' });
    await locator.check({ force: force });
    return emptyWithLog(`Checked checkbox: ${selector} with force: ${force}`);
}

export async function uncheckCheckbox(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const force = request.getForce();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.waitFor({ state: 'attached' });
    await locator.uncheck({ force: force });
    return emptyWithLog(`Unchecked checkbox: ${selector} with force: ${force}`);
}

export async function uploadFileBySelector(
    request: Request.FileBySelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const path = request.getPath();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.setInputFiles(path);
    return emptyWithLog('Successfully uploaded file');
}

export async function uploadFile(request: Request.FilePath, page: Page): Promise<Response.Empty> {
    const path = request.getPath();
    const fileChooser = await page.waitForEvent('filechooser');
    await fileChooser.setFiles(path);
    return emptyWithLog('Successfully uploaded file');
}

export async function handleAlert(request: Request.AlertAction, page: Page): Promise<Response.Empty> {
    const alertAction = request.getAlertaction() as 'accept' | 'dismiss';
    const promptInput = request.getPromptinput();
    const fn = async (dialog: Dialog) => {
        const dialogueText = dialog.message();
        if (promptInput) await dialog[alertAction](promptInput);
        else await dialog[alertAction]();
        logger.info(`Alert text: ${dialogueText}`);
    };
    page.on('dialog', fn);
    return emptyWithLog('Set event handler for next alert');
}

export async function waitForAlerts(request: Request.AlertActions, page: Page): Promise<Response.ListString> {
    const response = new Response.ListString();
    const alertActions = request.getItemsList();
    const alertMessages = [];
    for (let index = 0; index < alertActions.length; index++) {
        const alertAction = alertActions[index];
        const promptInput = alertAction.getPromptinput();
        const timeout = alertAction.getTimeout();
        const action = alertAction.getAlertaction();
        logger.info(`Waiting for alert with action: ${action}, promptInput: "${promptInput}" and timeout: ${timeout}`);
        const dialogObject = await page.waitForEvent('dialog', { timeout: timeout });
        alertMessages.push(dialogObject.message());
        if (action === 'accept' && promptInput) {
            dialogObject.accept(promptInput);
        } else if (alertAction.getAlertaction() === 'accept') {
            dialogObject.accept();
        } else {
            dialogObject.dismiss();
        }
    }
    response.setItemsList(alertMessages);
    return response;
}

export async function mouseButton(request: Request.MouseButtonOptions, page?: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'click' | 'up' | 'down';
    const params = JSON.parse(request.getJson());
    await invokeOnMouse(page, action, params);
    return emptyWithLog(`Successfully executed ${action}`);
}

export async function mouseMove(request: Request.Json, page?: Page): Promise<Response.Empty> {
    const params = JSON.parse(request.getBody());
    await invokeOnMouse(page, 'move', params);
    return emptyWithLog(`Successfully moved mouse to ${params.x}, ${params.y}`);
}

export async function mouseWheel(request: Request.MouseWheel, page?: Page): Promise<Response.Empty> {
    const deltaX = request.getDeltax();
    const deltaY = request.getDeltay();
    exists(page, `but no open page`);
    await page?.mouse.wheel(deltaX, deltaY);
    return emptyWithLog(`Successfully scrolled mouse wheel with ${deltaX}, ${deltaY}`);
}

export async function keyboardKey(request: Request.KeyboardKeypress, page: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'down' | 'up' | 'press';
    const key = request.getKey();
    await invokeOnKeyboard(page, action, key);
    return emptyWithLog(`Successfully did ${action} for ${key}`);
}

export async function keyboardInput(request: Request.KeyboardInputOptions, page: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'insertText' | 'type';
    const delay = request.getDelay();
    const input = request.getInput();

    await invokeOnKeyboard(page, action, input, { delay: delay });
    return emptyWithLog(`Successfully did virtual keyboard action ${action} with input ${input}`);
}

export async function scrollToElement(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.scrollIntoViewIfNeeded();
    return emptyWithLog(`Scrolled to ${selector} field if needed.`);
}
