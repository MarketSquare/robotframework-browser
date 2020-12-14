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

import { Dialog, FileChooser, Page } from 'playwright';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, stringResponse } from './response-util';
import { invokeOnKeyboard, invokeOnMouse, invokeOnPage, invokePlaywrightMethod } from './playwirght-invoke';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

export async function selectOption(
    request: Request.SelectElementSelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const matcher = JSON.parse(request.getMatcherjson());
    const result = await invokePlaywrightMethod(state, 'selectOption', selector, matcher);

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
    await invokePlaywrightMethod(state, 'selectOption', selector, []);
    return emptyWithLog(`Deselected options in element ${selector}`);
}

export async function inputText(request: Request.TextInput, state: PlaywrightState): Promise<Response.Empty> {
    const inputText = request.getInput();
    const selector = request.getSelector();
    const type = request.getType();
    const methodName = type ? 'type' : 'fill';
    await invokePlaywrightMethod(state, methodName, selector, inputText);
    return emptyWithLog('Input text: ' + inputText);
}

export async function typeText(request: Request.TypeText, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const text = request.getText();
    const delay = request.getDelay();
    const clear = request.getClear();
    if (clear) {
        await invokePlaywrightMethod(state, 'fill', selector, '');
    }
    await invokePlaywrightMethod(state, 'type', selector, text, { delay: delay });
    return emptyWithLog('Typed text: ' + text);
}

export async function fillText(request: Request.FillText, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const text = request.getText();
    await invokePlaywrightMethod(state, 'fill', selector, text);
    return emptyWithLog('Fill text: ' + text);
}

export async function clearText(request: Request.ClearText, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    await invokePlaywrightMethod(state, 'fill', selector, '');
    return emptyWithLog('Text field cleared.');
}

export async function press(request: Request.PressKeys, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    const keyList = request.getKeyList();
    for (const i of keyList) {
        await invokePlaywrightMethod(state, 'press', selector, i);
    }
    return emptyWithLog('Pressed keys: ' + keyList);
}

export async function click(
    request: Request.ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const options = request.getOptions();
    await invokePlaywrightMethod(state, 'click', selector, JSON.parse(options));
    return emptyWithLog(`Clicked element: '${selector}' with options: '${options}'`);
}

export async function hover(
    request: Request.ElementSelectorWithOptions,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    const options = request.getOptions();
    await invokePlaywrightMethod(state, 'hover', selector, JSON.parse(options));
    return emptyWithLog(`Hovered element: '${selector}' With options: '${options}'`);
}

export async function focus(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    await invokePlaywrightMethod(state, 'focus', selector);
    return emptyWithLog('Focused element: ' + selector);
}

export async function checkCheckbox(request: Request.ElementSelector, state: PlaywrightState): Promise<Response.Empty> {
    const selector = request.getSelector();
    await invokePlaywrightMethod(state, 'check', selector);
    return emptyWithLog('Checked checkbox: ' + selector);
}

export async function uncheckCheckbox(
    request: Request.ElementSelector,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const selector = request.getSelector();
    await invokePlaywrightMethod(state, 'uncheck', selector);
    return emptyWithLog('Unchecked checkbox: ' + selector);
}

export async function uploadFile(request: Request.FilePath, page?: Page): Promise<Response.Empty> {
    const path = request.getPath();
    const fn = async (fileChooser: FileChooser) => await fileChooser.setFiles(path);
    await invokeOnPage(page, 'on', 'filechooser', fn);
    return emptyWithLog('Succesfully uploaded file');
}

export async function handleAlert(request: Request.AlertAction, page?: Page): Promise<Response.String> {
    const alertAction = request.getAlertaction() as 'accept' | 'dismiss';
    const promptInput = request.getPromptinput();
    const fn = async (dialog: Dialog) => {
        if (promptInput) await dialog[alertAction](promptInput);
        else await dialog[alertAction]();
    };
    const dialog = await invokeOnPage(page, 'on', 'dialog', fn);
    // TODO, expecting dialog but getting page
    return stringResponse(dialog.message, 'Set event handler for next alert');
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
export async function keyboardKey(request: Request.KeyboardKeypress, page?: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'down' | 'up' | 'press';
    const key = request.getKey();
    await invokeOnKeyboard(page, action, key);
    return emptyWithLog(`Succesfully did ${action} for ${key}`);
}

export async function keyboardInput(request: Request.KeyboardInputOptions, page?: Page): Promise<Response.Empty> {
    const action = request.getAction() as 'insertText' | 'type';
    const delay = request.getDelay();
    const input = request.getInput();

    await invokeOnKeyboard(page, action, input, { delay: delay });
    return emptyWithLog(`Succesfully did virtual keyboard action ${action} with input ${input}`);
}
