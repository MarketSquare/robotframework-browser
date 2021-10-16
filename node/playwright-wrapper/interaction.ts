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
import { v4 as uuidv4 } from 'uuid';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, jsonResponse, stringResponse } from './response-util';
import {
    findLocator,
    findLocatorCount,
    invokeOnKeyboard,
    invokeOnMouse,
    invokePlaywrightMethod,
} from './playwirght-invoke';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

export async function selectOption(
    request: Request.SelectElementSelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const matcher = JSON.parse(request.getMatcherjson());
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    const result = await locator.selectOption(matcher);
    if (result.length == 0) {
        logger.info("Couldn't select any options");
        throw new Error(`No options matched ${matcher}`);
    }
    return emptyWithLog(`Selected options ${result} in element ${selector}`);
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
    const delay = request.getDelay();
    const clear = request.getClear();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    if (clear) {
        await locator.fill('');
    }
    await locator.type(text, { delay: delay });
    return emptyWithLog(`Typed text "${text}" on ${selector}`);
}

export async function fillText(request: Request.FillText, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const text = request.getText();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.fill(text);
    return emptyWithLog(`Fill text ${text} on ${selector}`);
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
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.click(JSON.parse(options));
    return emptyWithLog(`Clicked element: '${selector}' with options: '${options}'`);
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
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.check();
    return emptyWithLog(`Checked checkbox: ${selector}`);
}

export async function uncheckCheckbox(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const strictMode = request.getStrict();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    await locator.uncheck();
    return emptyWithLog(`Unchecked checkbox: ${selector}`);
}

export async function uploadFile(request: Request.FilePath, page: Page): Promise<Response.Empty> {
    const path = request.getPath();
    const fileChooser = await page.waitForEvent('filechooser');
    await fileChooser.setFiles(path);
    return emptyWithLog('Succesfully uploaded file');
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

export async function waitForAlert(request: Request.AlertAction, page: Page): Promise<Response.String> {
    const alertAction = request.getAlertaction() as 'accept' | 'dismiss';
    const promptInput = request.getPromptinput();
    const dialogObject = await page.waitForEvent('dialog');
    const message = dialogObject.message();
    if (alertAction === 'accept' && promptInput) {
        dialogObject.accept(promptInput);
    } else if (alertAction === 'accept') {
        dialogObject.accept();
    } else {
        dialogObject.dismiss();
    }
    return stringResponse(message, 'Next alert was handeled succesfully.');
}

export async function mouseButton(request: Request.MouseButtonOptions, page?: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'click' | 'up' | 'down';
    const params = JSON.parse(request.getJson());
    await invokeOnMouse(page, action, params);
    return emptyWithLog(`Succesfully executed ${action}`);
}

export async function mouseMove(request: Request.Json, page?: Page): Promise<Response.Empty> {
    const params = JSON.parse(request.getBody());
    await invokeOnMouse(page, 'move', params);
    return emptyWithLog(`Succesfully moved mouse to ${params.x}, ${params.y}`);
}
export async function keyboardKey(request: Request.KeyboardKeypress, page: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'down' | 'up' | 'press';
    const key = request.getKey();
    await invokeOnKeyboard(page, action, key);
    return emptyWithLog(`Succesfully did ${action} for ${key}`);
}

export async function keyboardInput(request: Request.KeyboardInputOptions, page: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'insertText' | 'type';
    const delay = request.getDelay();
    const input = request.getInput();

    await invokeOnKeyboard(page, action, input, { delay: delay });
    return emptyWithLog(`Succesfully did virtual keyboard action ${action} with input ${input}`);
}

export async function tidii(
    request: Request.ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const options = request.getOptions();
    const strictMode = request.getStrict();
    const locator = findLocator(state, selector, strictMode, undefined, true);
    await (await locator).click(JSON.parse(options));
    return emptyWithLog(`Clicked element: '${selector}' with options: '${options}'`);
}

export async function tidiiGetElement(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.String> {
    const strictMode = request.getStrict();
    const selector = request.getSelector();
    const locator = await findLocator(state, selector, strictMode, undefined, true);
    const id = uuidv4();
    state.addLocator(id, locator, 0);
    return stringResponse(`element=${id}`, 'Element found successfully.');
}

export async function tidiiGetElements(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Json> {
    const strictMode = request.getStrict();
    const selector = request.getSelector();
    const count = await findLocatorCount(state, selector);
    const response: string[] = [];
    for (let i = 0; i < count; i++) {
        const id = uuidv4();
        const locator = await findLocator(state, selector, strictMode, i, true);
        state.addLocator(id, locator, i);
        response.push(`element=${id}`);
    }
    return jsonResponse(JSON.stringify(response), `Found ${count} elements successfully.`);
}
