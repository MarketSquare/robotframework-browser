import * as pb from './generated/playwright_pb';
import { Page } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { emptyWithLog, jsonResponse, stringResponse } from './response-util';
import { invokeOnPage } from './playwirght-invoke';
export async function httpRequest(
    call: ServerUnaryCall<pb.Request.HttpRequest>,
    callback: sendUnaryData<pb.Response.Json>,
    page?: Page,
) {
    const opts: { [k: string]: any } = {
        method: call.request.getMethod(),
        url: call.request.getUrl(),
        headers: JSON.parse(call.request.getHeaders()),
    };
    if (opts.method != 'GET') {
        opts.body = call.request.getBody();
    }
    try {
        const response = await page?.evaluate(({ url, method, body, headers }) => {
            return fetch(url, { method, body, headers }).then((data: Response) => {
                return data.text().then((body) => {
                    const headers: { [k: string]: any } = {};
                    data.headers.forEach((value, name) => (headers[name] = value));
                    return {
                        status: data.status,
                        body: body,
                        headers: JSON.stringify(headers),
                        type: data.type,
                        statusText: data.statusText,
                        url: data.url,
                        ok: data.ok,
                        redirected: data.redirected,
                    };
                });
            });
        }, opts);
        callback(null, jsonResponse(JSON.stringify(response), 'Request performed succesfully.'));
    } catch (e) {
        callback(e, null);
    }
}

export async function waitForResponse(
    call: ServerUnaryCall<pb.Request.HttpCapture>,
    callback: sendUnaryData<pb.Response.Json>,
    page?: Page,
) {
    const urlOrPredicate = call.request.getUrlorpredicate();
    const timeout = call.request.getTimeout();
    const result = await invokeOnPage(page, callback, 'waitForResponse', urlOrPredicate, { timeout: timeout });
    const body = await result.json();
    callback(null, jsonResponse(body, ''));
}
export async function waitForRequest(
    call: ServerUnaryCall<pb.Request.HttpCapture>,
    callback: sendUnaryData<pb.Response.String>,
    page?: Page,
) {
    const urlOrPredicate = call.request.getUrlorpredicate();
    const timeout = call.request.getTimeout();
    const result = await invokeOnPage(page, callback, 'waitForRequest', urlOrPredicate, { timeout: timeout });
    callback(null, stringResponse(result.url(), 'Requested compeleted withing timeout.'));
}

export async function waitUntilNetworkIsIdle(
    call: ServerUnaryCall<pb.Request.Timeout>,
    callback: sendUnaryData<pb.Response.Empty>,
    page?: Page,
) {
    const timeout = call.request.getTimeout();
    await invokeOnPage(page, callback, 'waitForLoadState', 'networkidle', { timeout: timeout });
    callback(null, emptyWithLog('Network is idle'));
}

export async function waitForDownload(
    call: ServerUnaryCall<pb.Request.FilePath>,
    callback: sendUnaryData<pb.Response.String>,
    page?: Page,
) {
    const saveAs = call.request.getPath();
    const downloadObject = await invokeOnPage(page, callback, 'waitForEvent', 'download');

    if (saveAs) {
        await downloadObject.saveAs(saveAs);
    }
    const path = await downloadObject.path();
    callback(null, stringResponse(JSON.stringify(path), 'Download done successfully to.'));
}
