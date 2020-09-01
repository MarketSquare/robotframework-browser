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
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog } from './response-util';
import { invokeOnKeyboard, invokeOnMouse, invokeOnPage, invokePlaywrightMethod } from './playwirght-invoke';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

export async function selectOption(
    call: ServerUnaryCall<Request.SelectElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const matcher = JSON.parse(call.request.getMatcherjson());
    const result = await invokePlaywrightMethod(state, callback, 'selectOption', selector, matcher);

    if (result.length == 0) {
        logger.info("Couldn't select any options");
        const error = new Error(`No options matched ${matcher}`);
        return callback(error, null);
    }
    const response = emptyWithLog(`Selected options ${result} in element ${selector}`);
    callback(null, response);
}

export async function deSelectOption(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywrightMethod(state, callback, 'selectOption', selector, []);
    callback(null, emptyWithLog(`Deselected options in element ${selector}`));
}

export async function inputText(
    call: ServerUnaryCall<Request.TextInput>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const inputText = call.request.getInput();
    const selector = call.request.getSelector();
    const type = call.request.getType();
    const methodName = type ? 'type' : 'fill';
    await invokePlaywrightMethod(state, callback, methodName, selector, inputText);
    callback(null, emptyWithLog('Input text: ' + inputText));
}

export async function typeText(
    call: ServerUnaryCall<Request.TypeText>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const text = call.request.getText();
    const delay = call.request.getDelay();
    const clear = call.request.getClear();
    if (clear) {
        await invokePlaywrightMethod(state, callback, 'fill', selector, '');
    }
    await invokePlaywrightMethod(state, callback, 'type', selector, text, { delay: delay });
    callback(null, emptyWithLog('Typed text: ' + text));
}

export async function fillText(
    call: ServerUnaryCall<Request.FillText>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const text = call.request.getText();
    await invokePlaywrightMethod(state, callback, 'fill', selector, text);
    callback(null, emptyWithLog('Fill text: ' + text));
}

export async function clearText(
    call: ServerUnaryCall<Request.ClearText>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywrightMethod(state, callback, 'fill', selector, '');
    callback(null, emptyWithLog('Text field cleared.'));
}

export async function press(
    call: ServerUnaryCall<Request.PressKeys>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const keyList = call.request.getKeyList();
    for (const i of keyList) {
        await invokePlaywrightMethod(state, callback, 'press', selector, i);
    }
    callback(null, emptyWithLog('Pressed keys: ' + keyList));
}

export async function click(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywrightMethod(state, callback, 'click', selector);
    callback(null, emptyWithLog('Clicked element: ' + selector));
}

export async function clickWithOptions(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const options = call.request.getOptions();
    await invokePlaywrightMethod(state, callback, 'click', selector, JSON.parse(options));
    callback(null, emptyWithLog(`Clicked element: '${selector}' With options: '${options}'`));
}

export async function hover(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const options = call.request.getOptions();
    await invokePlaywrightMethod(state, callback, 'hover', selector, JSON.parse(options));
    callback(null, emptyWithLog(`Hovered element: '${selector}' With options: '${options}'`));
}

export async function focus(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywrightMethod(state, callback, 'focus', selector);
    callback(null, emptyWithLog('Focused element: ' + selector));
}

export async function checkCheckbox(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywrightMethod(state, callback, 'check', selector);
    callback(null, emptyWithLog('Checked checkbox: ' + selector));
}

export async function uncheckCheckbox(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywrightMethod(state, callback, 'uncheck', selector);
    callback(null, emptyWithLog('Unchecked checkbox: ' + selector));
}

export async function uploadFile(
    call: ServerUnaryCall<Request.FilePath>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const path = call.request.getPath();
    const fn = async (fileChooser: FileChooser) => await fileChooser.setFiles(path);
    await invokeOnPage(page, callback, 'on', 'filechooser', fn);
    callback(null, emptyWithLog('Succesfully uploaded file'));
}

export async function handleAlert(
    call: ServerUnaryCall<Request.AlertAction>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const alertAction = call.request.getAlertaction() as 'accept' | 'dismiss';
    const promptInput = call.request.getPromptinput();
    const fn = async (dialog: Dialog) => {
        if (promptInput) await dialog[alertAction](promptInput);
        else await dialog[alertAction]();
    };
    await invokeOnPage(page, callback, 'on', 'dialog', fn);
    callback(null, emptyWithLog('Set event handler for next alert'));
}

export async function mouseButton(
    call: ServerUnaryCall<Request.MouseButtonOptions>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
): Promise<void> {
    const action = call.request.getAction() as 'click' | 'up' | 'down';
    const params = JSON.parse(call.request.getJson());
    await invokeOnMouse(page, callback, action, params);
    callback(null, emptyWithLog(`Succesfully executed ${action}`));
}

export async function mouseMove(
    call: ServerUnaryCall<Request.Json>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
): Promise<void> {
    const params = JSON.parse(call.request.getBody());
    await invokeOnMouse(page, callback, 'move', params);
    callback(null, emptyWithLog(`Succesfully moved mouse to ${params.x}, ${params.y}`));
}
export async function keyboardKey(
    call: ServerUnaryCall<Request.KeyboardKeypress>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
): Promise<void> {
    const action = call.request.getAction() as 'down' | 'up' | 'press';
    const key = call.request.getKey();
    await invokeOnKeyboard(page, callback, action, key);
    callback(null, emptyWithLog(`Succesfully did ${action} for ${key}`));
}

export async function keyboardInput(
    call: ServerUnaryCall<Request.KeyboardInputOptions>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
): Promise<void> {
    const action = call.request.getAction() as 'insertText' | 'type';
    const delay = call.request.getDelay();
    const input = call.request.getInput();

    await invokeOnKeyboard(page, callback, action, input, { delay: delay });
    callback(null, emptyWithLog(`Succesfully did virtual keyboard action ${action} with input ${input}`));
}
