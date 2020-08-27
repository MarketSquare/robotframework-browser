import { Dialog, FileChooser, Page } from 'playwright';
import { Request, Response } from './generated/playwright_pb';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { IndexedPage, PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';
import { exists, invokeOnPage } from './playwirght-invoke';

export async function waitForDownload(
    call: ServerUnaryCall<Request.FilePath>,
    callback: sendUnaryData<Response.Json>,
    page?: Page,
) {
    exists(page, callback, 'No open page');
    const saveAs = call.request.getPath();
    const downloadObject = await invokeOnPage(page, callback, 'waitForEvent', 'download');

    if (saveAs) {
        await downloadObject.saveAs(saveAs);
    }
    const path = await downloadObject.path();
    callback(null, jsonResponse(JSON.stringify(path), 'Download done successfully to.'));
}

export async function handleUpload(
    call: ServerUnaryCall<Request.FilePath>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const path = call.request.getPath();
    const selector = call.request.getSelector();
    await page?.setInputFiles(selector, path);
    callback(null, emptyWithLog(`Succesfully uploaded files from path ${path}`));
    return;
}

function actOnDialog(action: 'accept' | 'dismiss', promptInput?: string) {
    return async (dialog: Dialog) => {
        if (promptInput) await dialog[action](promptInput);
        else await dialog[action]();
    };
}

export async function handleDialog(
    call: ServerUnaryCall<Request.DialogAction>,
    callback: sendUnaryData<Response.Empty>,
    page?: IndexedPage,
) {
    exists(page, callback, 'No open page');
    const action = call.request.getAction() as 'accept' | 'dismiss' | 'ignore';
    const promptInput = call.request.getPromptinput();

    if (action === 'ignore') {
        callback(null, emptyWithLog('cleared dialog handlers'));
        return;
    }

    const currentDialog = window.__RFBROWSER__;
    if (currentDialog) {
        await actOnDialog(action, promptInput)(currentDialog);
        callback(null, emptyWithLog('Handled dialog'));
    } else {
        await invokeOnPage(page?.p, callback, 'waitForEvent', 'dialog', actOnDialog(action, promptInput));
        callback(null, emptyWithLog('Handled dialog'));
    }
}

const dialogListeners: ((dialog: Dialog) => Promise<void>)[] = [];

export async function handleFutureDialogs(
    call: ServerUnaryCall<Request.DialogAction>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    exists(page, callback, 'No open page');
    const action = call.request.getAction() as 'accept' | 'dismiss' | 'ignore';
    const promptInput = call.request.getPromptinput();

    if (action === 'ignore') {
        dialogListeners.forEach((listener) => {
            page.removeListener('dialog', listener);
        });
        page.on('dialog', () => {});
        callback(null, emptyWithLog('cleared dialog handlers'));
        return;
    } else {
        const actfn = actOnDialog(action, promptInput);
        page.on('dialog', actfn);
        dialogListeners.push(actfn);
        callback(null, emptyWithLog('Set new dialog handler'));
        return;
    }
}
