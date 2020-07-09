import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { invokePlaywright } from './playwirght-util';
import { emptyWithLog, jsResponse } from './response-util';

export async function selectOption(
    call: ServerUnaryCall<Request.SelectElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    const matcher = JSON.parse(call.request.getMatcherjson());
    const result = await invokePlaywright(page, callback, 'selectOption', selector, matcher);

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
    page?: Page,
) {
    const selector = call.request.getSelector();
    await invokePlaywright(page, callback, 'selectOption', selector, []);
    callback(null, emptyWithLog(`Deselected options in element ${selector}`));
}

export async function inputText(
    call: ServerUnaryCall<Request.TextInput>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const inputText = call.request.getInput();
    const selector = call.request.getSelector();
    const type = call.request.getType();
    const methodName = type ? 'type' : 'fill';
    await invokePlaywright(page, callback, methodName, selector, inputText);
    callback(null, emptyWithLog('Input text: ' + inputText));
}

export async function typeText(
    call: ServerUnaryCall<Request.TypeText>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    const text = call.request.getText();
    const delay = call.request.getDelay();
    const clear = call.request.getClear();
    if (clear) {
        await invokePlaywright(page, callback, 'fill', selector, '');
    }
    await invokePlaywright(page, callback, 'type', selector, text, { delay: delay });
    callback(null, emptyWithLog('Typed text: ' + text));
}

export async function fillText(
    call: ServerUnaryCall<Request.FillText>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    const text = call.request.getText();
    await invokePlaywright(page, callback, 'fill', selector, text);
    callback(null, emptyWithLog('Fill text: ' + text));
}

export async function clearText(
    call: ServerUnaryCall<Request.ClearText>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    await invokePlaywright(page, callback, 'fill', selector, '');
    callback(null, emptyWithLog('Text field cleared.'));
}

export async function press(
    call: ServerUnaryCall<Request.PressKeys>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    const keyList = call.request.getKeyList();
    for (const i of keyList) {
        await invokePlaywright(page, callback, 'press', selector, i);
    }
    callback(null, emptyWithLog('Pressed keys: ' + keyList));
}

export async function click(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    await invokePlaywright(page, callback, 'click', selector);
    callback(null, emptyWithLog('Clicked element: ' + selector));
}

export async function clickWithOptions(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    const options = call.request.getOptions();
    await invokePlaywright(page, callback, 'click', selector, JSON.parse(options));
    callback(null, emptyWithLog('Clicked element: ' + selector + ' \nWith options: ' + options));
}

export async function focus(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    await invokePlaywright(page, callback, 'focus', selector);
    callback(null, emptyWithLog('Focused element: ' + selector));
}

export async function checkCheckbox(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    await invokePlaywright(page, callback, 'check', selector);
    callback(null, emptyWithLog('Checked checkbox: ' + selector));
}

export async function uncheckCheckbox(
    call: ServerUnaryCall<Request.ElementSelector>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    await invokePlaywright(page, callback, 'uncheck', selector);
    callback(null, emptyWithLog('Unchecked checkbox: ' + selector));
}

export async function waitForElementState(
    call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const selector = call.request.getSelector();
    const options = JSON.parse(call.request.getOptions());
    await invokePlaywright(page, callback, 'waitForSelector', selector, options);
    callback(null, emptyWithLog('Wait for Element with selector: ' + selector));
}

export async function executeJavascriptOnPage(
    call: ServerUnaryCall<Request.JavascriptCode>,
    callback: sendUnaryData<Response.JavascriptExecutionResult>,
    page?: Page,
) {
    const result = await invokePlaywright(page, callback, 'evaluate', call.request.getScript());
    callback(null, jsResponse(result));
}

export async function getPageState(callback: sendUnaryData<Response.JavascriptExecutionResult>, page?: Page) {
    const result = await invokePlaywright(page, callback, 'evaluate', () => window.__RFBROWSER__);
    callback(null, jsResponse(result));
}
