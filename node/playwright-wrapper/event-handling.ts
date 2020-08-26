import { Dialog, FileChooser, Page } from 'playwright';
import { Request, Response } from './generated/playwright_pb';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

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

export async function handleFutureUpload(
    call: ServerUnaryCall<Request.FilePath>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const path = call.request.getPath();
    const fn = async (fileChooser: FileChooser) => await fileChooser.setFiles(path);
    await invokeOnPage(page, callback, 'on', 'filechooser', fn);
    callback(null, emptyWithLog('Succesfully uploaded file'));
}

export async function handleFutureDialogs(
    call: ServerUnaryCall<Request.DialogAction>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const action = call.request.getAction() as 'accept' | 'dismiss' | 'ignore';
    const promptInput = call.request.getPromptinput();
    if (action === 'ignore') {
        // clear the old event handlers here
        return;
    }
    const fn = async (dialog: Dialog) => {
        if (promptInput) await dialog[action](promptInput);
        else await dialog[action]();
    };
    await invokeOnPage(page, callback, 'on', 'dialog', fn);
    callback(null, emptyWithLog('Set event handler for future alerts'));
}
