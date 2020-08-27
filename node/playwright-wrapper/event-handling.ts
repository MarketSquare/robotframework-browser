import { Dialog, FileChooser, Page } from 'playwright';
import { Request, Response } from './generated/playwright_pb';
import { Server, ServerUnaryCall, sendUnaryData } from 'grpc';

import { IndexedPage, PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';
import { invokeOnPage } from './playwirght-invoke';

export async function waitForDownload(
    call: ServerUnaryCall<Request.FilePath>,
    callback: sendUnaryData<Response.Json>,
    page?: Page,
) {
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
    page?: IndexedPage,
) {
    const path = call.request.getPath();

    const currentFileChooser = page?.latestFilechooser;
    if (currentFileChooser) {
        const path = call.request.getPath();
        await currentFileChooser.setFiles(path);
        callback(null, emptyWithLog('Succesfully uploaded file'));
    } else {
        const fn = async (fileChooser: FileChooser) => await fileChooser.setFiles(path);
        await invokeOnPage(page?.p, callback, 'waitForEvent', 'filechooser', fn);
        callback(null, emptyWithLog('Succesfully uploaded file'));
    }
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
    const action = call.request.getAction() as 'accept' | 'dismiss' | 'ignore';
    const promptInput = call.request.getPromptinput();

    if (action === 'ignore') {
        callback(null, emptyWithLog('cleared dialog handlers'));
        return;
    }

    const currentDialog = page?.latestDialog;
    if (currentDialog) {
        await actOnDialog(action, promptInput)(currentDialog);
        callback(null, emptyWithLog('Handled dialog'));
    } else {
        await invokeOnPage(page?.p, callback, 'waitForEvent', 'dialog', actOnDialog(action, promptInput));
        callback(null, emptyWithLog('Handled dialog'));
    }
}

export async function handleFutureDialogs(
    call: ServerUnaryCall<Request.DialogAction>,
    callback: sendUnaryData<Response.Empty>,
    state: PlaywrightState,
) {
    const action = call.request.getAction() as 'accept' | 'dismiss' | 'ignore';
    const promptInput = call.request.getPromptinput();

    if (action === 'ignore') {
        callback(null, emptyWithLog('cleared dialog handlers'));
        return;
    } else {
        state.dialogHandler = actOnDialog(action, promptInput);
    }
}
