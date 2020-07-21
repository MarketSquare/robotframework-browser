import { sendUnaryData, ServerUnaryCall } from 'grpc';

import { Response, Request } from './generated/playwright_pb';
import { invokePlaywirghtMethod } from './playwirght-invoke';
import { emptyWithLog } from './response-util';
import { PlaywrightState } from './playwright-state';

export async function selectOption(
    call: ServerUnaryCall<Request.SelectElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const matcher = JSON.parse(call.request.getMatcherjson());
    const result = await invokePlaywirghtMethod(state, callback, 'selectOption', selector, matcher);

    if (result.length == 0) {
        console.log("Couldn't select any options");
        const error = new Error(`No options matched ${matcher}`);
        callback(error, null);
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
    await invokePlaywirghtMethod(state, callback, 'selectOption', selector, []);
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
    await invokePlaywirghtMethod(state, callback, methodName, selector, inputText);
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
        await invokePlaywirghtMethod(state, callback, 'fill', selector, '');
    }
    await invokePlaywirghtMethod(state, callback, 'type', selector, text, { delay: delay });
    callback(null, emptyWithLog('Typed text: ' + text));
}

export async function fillText(
    call: ServerUnaryCall<Request.FillText>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const text = call.request.getText();
    await invokePlaywirghtMethod(state, callback, 'fill', selector, text);
    callback(null, emptyWithLog('Fill text: ' + text));
}

export async function clearText(
    call: ServerUnaryCall<Request.ClearText>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywirghtMethod(state, callback, 'fill', selector, '');
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
        await invokePlaywirghtMethod(state, callback, 'press', selector, i);
    }
    callback(null, emptyWithLog('Pressed keys: ' + keyList));
}

export async function click(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywirghtMethod(state, callback, 'click', selector);
    callback(null, emptyWithLog('Clicked element: ' + selector));
}

export async function clickWithOptions(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    const options = call.request.getOptions();
    await invokePlaywirghtMethod(state, callback, 'click', selector, JSON.parse(options));
    callback(null, emptyWithLog('Clicked element: ' + selector + ' \nWith options: ' + options));
}

export async function focus(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywirghtMethod(state, callback, 'focus', selector);
    callback(null, emptyWithLog('Focused element: ' + selector));
}

export async function checkCheckbox(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywirghtMethod(state, callback, 'check', selector);
    callback(null, emptyWithLog('Checked checkbox: ' + selector));
}

export async function uncheckCheckbox(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const selector = call.request.getSelector();
    await invokePlaywirghtMethod(state, callback, 'uncheck', selector);
    callback(null, emptyWithLog('Unchecked checkbox: ' + selector));
}
