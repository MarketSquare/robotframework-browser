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

import * as path from 'path';
import * as pb from './generated/playwright_pb';
import { Page } from 'playwright';
import { PlaywrightState } from './playwright-state';
import { v4 as uuidv4 } from 'uuid';

import { emptyWithLog, jsonResponse, parseRegExpOrKeepString, stringResponse } from './response-util';

import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function httpRequest(request: pb.Request.HttpRequest, page: Page): Promise<pb.Response.Json> {
    const opts: { [k: string]: any } = {
        method: request.getMethod(),
        url: request.getUrl(),
        headers: JSON.parse(request.getHeaders()),
    };
    if (opts.method != 'GET') {
        opts.body = request.getBody();
    }
    const response = await page.evaluate(({ url, method, body, headers }) => {
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
    return jsonResponse(JSON.stringify(response), 'Request performed successfully.');
}

export function deserializeUrlOrPredicate(
    urlOrPredicate: string,
): RegExp | string | ((request: unknown) => boolean | Promise<boolean>) {
    // if the matcher is a function or arrow function, wrap it in parens and evaluate.
    if (
        /^function.*{.*}$/.test(urlOrPredicate) ||
        /([a-zA-Z]\w*|\([a-zA-Z]\w*(,\s*[a-zA-Z]\w*)*\)) =>/.test(urlOrPredicate)
    ) {
        const fn = new Function(`return (${urlOrPredicate})`)();
        if (typeof fn === 'function' || Object.prototype.toString.call(fn) === '[object Function]') {
            return fn;
        }
    }

    return parseRegExpOrKeepString(urlOrPredicate);
}

export async function waitForResponse(request: pb.Request.HttpCapture, page: Page): Promise<pb.Response.Json[]> {
    const urlOrPredicate = deserializeUrlOrPredicate(request.getUrlorpredicate());
    const timeout = request.getTimeout();
    const data = await page.waitForResponse(urlOrPredicate, { timeout });
    let body = null;
    try {
        body = await data.text();
    } catch (e) {
        logger.info(`Error reading response ${e}`);
    }
    const jsonData = JSON.stringify({
        status: data.status(),
        headers: JSON.stringify(data.headers()),
        statusText: data.statusText(),
        url: data.url(),
        ok: data.ok(),
        request: {
            headers: JSON.stringify(data.request().headers()),
            method: data.request().method(),
            postData: data.request().postData(),
        },
    });
    const chunkSize = 3500000;
    const responseChunks = [];
    if (body && body.length > chunkSize) {
        logger.info(`body.length: ${body.length}`);
        for (let i = 0; i < body.length; i += chunkSize) {
            const chunk = body.substring(i, i + chunkSize);
            const response = jsonResponse(jsonData, `Response received, chunk ${i}`, chunk);
            logger.info(`chunked response: ${i}`);
            responseChunks.push(response);
        }
    } else {
        if (body !== null) {
            const response = jsonResponse(jsonData, 'Response received', body);
            responseChunks.push(response);
        } else {
            const jsonDataMap = JSON.parse(jsonData);
            jsonDataMap.body = null;
            const response = jsonResponse(JSON.stringify(jsonDataMap), 'Response received with empty body', '');
            responseChunks.push(response);
        }
    }
    logger.info(`responseChunks.length: ${responseChunks.length}`);
    return responseChunks;
}
export async function waitForRequest(request: pb.Request.HttpCapture, page: Page): Promise<pb.Response.String> {
    const urlOrPredicate = deserializeUrlOrPredicate(request.getUrlorpredicate());
    const timeout = request.getTimeout();
    const result = await page.waitForRequest(urlOrPredicate, { timeout });
    return stringResponse(result.url(), 'Request completed within timeout.');
}

export async function waitForNavigation(request: pb.Request.UrlOptions, page: Page): Promise<pb.Response.Empty> {
    const url = parseRegExpOrKeepString(<string>request.getUrl()?.getUrl());
    const timeout = request.getUrl()?.getDefaulttimeout();
    const waitUntil = <'load' | 'domcontentloaded' | 'networkidle' | 'commit' | undefined>request.getWaituntil();
    await page.waitForNavigation({ timeout: timeout, url: url, waitUntil: waitUntil });
    return emptyWithLog(`Navigated to: ${url}, location is: ${page.url()}`);
}

export async function WaitForPageLoadState(request: pb.Request.PageLoadState, page: Page): Promise<pb.Response.Empty> {
    const state = <'load' | 'domcontentloaded' | 'networkidle' | undefined>request.getState();
    const timeout = request.getTimeout();
    logger.info(`timeout: ${timeout} state: ${state}`);
    await page.waitForLoadState(state, { timeout });
    return emptyWithLog(`Load state ${state} got in ${timeout}`);
}

export async function waitForDownload(
    request: pb.Request.DownloadOptions,
    state: PlaywrightState,
    page: Page,
): Promise<pb.Response.Json> {
    const saveAs = request.getPath();
    const waitForFinish = request.getWaitforfinish();
    const downloadTimeout = request.getDownloadtimeout();
    return await _waitForDownload(page, state, saveAs, downloadTimeout, waitForFinish);
}

export async function _waitForDownload(
    page: Page,
    state: PlaywrightState,
    saveAs: string,
    downloadTimeout: number,
    waitForFinished: boolean,
): Promise<pb.Response.Json> {
    const downloadObject = await page.waitForEvent('download');
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    const downloadsPath = state.activeBrowser.browser?._options?.downloadsPath;
    if (downloadsPath && saveAs) {
        logger.info('saveAs: ' + path.resolve(downloadsPath, saveAs));
        if (!path.isAbsolute(saveAs)) {
            saveAs = path.resolve(downloadsPath, saveAs);
        }
    }
    const fileName = downloadObject.suggestedFilename();
    if (!waitForFinished) {
        const downloadID = uuidv4();
        const activeIndexedPage = state.activeBrowser?.page;
        if (activeIndexedPage) {
            activeIndexedPage.activeDownloads.set(downloadID, {
                downloadObject: downloadObject,
                suggestedFilename: fileName,
                saveAs: saveAs,
            });
            return jsonResponse(
                JSON.stringify({
                    saveAs: '',
                    suggestedFilename: fileName,
                    state: 'in_progress',
                    downloadID: downloadID,
                }),
                'Download started successfully.',
            );
        } else {
            throw new Error('No active page found');
        }
    }
    if (downloadTimeout > 0) {
        const readStream = await Promise.race([
            downloadObject.createReadStream(),
            new Promise((resolve) => setTimeout(resolve, downloadTimeout)),
        ]);
        if (!readStream) {
            downloadObject.cancel();
            throw new Error('Download failed, Timeout exceeded.');
        }
    }
    let filePath;
    if (saveAs) {
        await downloadObject.saveAs(saveAs);
        filePath = path.resolve(saveAs);
    } else {
        filePath = await downloadObject.path();
    }
    logger.info('suggestedFilename: ' + fileName + ' saveAs path: ' + filePath);
    return jsonResponse(
        JSON.stringify({ saveAs: filePath, suggestedFilename: fileName, state: 'finished', downloadID: null }),
        'Download done successfully to: ' + filePath,
    );
}

export async function getDownloadState(
    request: pb.Request.DownloadID,
    state: PlaywrightState,
): Promise<pb.Response.Json> {
    const downloadID = request.getId();
    const activeIndexedPage = state.activeBrowser?.page;
    if (!activeIndexedPage) {
        throw new Error('No active page found');
    }
    const downloadInfo = activeIndexedPage.activeDownloads.get(downloadID);
    if (!downloadInfo) {
        throw new Error('No download object found for id: ' + downloadID);
    }
    const downloadObject = downloadInfo.downloadObject;
    const suggestedFilename = downloadInfo.suggestedFilename;
    const failure = await Promise.race([downloadObject.failure(), new Promise((resolve) => setTimeout(resolve, 50))]);
    if (failure === null) {
        const saveAs = downloadInfo.saveAs;
        let filePath;
        if (saveAs) {
            await downloadObject.saveAs(saveAs);
            filePath = path.resolve(saveAs);
        } else {
            filePath = await downloadObject.path();
        }
        return jsonResponse(
            JSON.stringify({
                saveAs: filePath,
                suggestedFilename: suggestedFilename,
                state: 'finished',
                downloadID: downloadID,
            }),
            'Download state received',
        );
    } else if (failure) {
        return jsonResponse(
            JSON.stringify({
                saveAs: '',
                suggestedFilename: suggestedFilename,
                state: failure,
                downloadID: downloadID,
            }),
            'Download state received',
        );
    } else {
        return jsonResponse(
            JSON.stringify({
                saveAs: '',
                suggestedFilename: suggestedFilename,
                state: 'in_progress',
                downloadID: downloadID,
            }),
            'Download state received',
        );
    }
}

export async function cancelDownload(
    request: pb.Request.DownloadID,
    state: PlaywrightState,
): Promise<pb.Response.Empty> {
    const downloadID = request.getId();
    const activeIndexedPage = state.activeBrowser?.page;
    if (!activeIndexedPage) {
        throw new Error('No active page found');
    }
    const downloadInfo = activeIndexedPage.activeDownloads.get(downloadID);
    if (!downloadInfo) {
        throw new Error('No download object found for id: ' + downloadID);
    }
    const downloadObject = downloadInfo.downloadObject;
    downloadObject.cancel();
    const failure = await downloadObject.failure();
    if (failure == 'canceled') {
        return emptyWithLog('Download canceled successfully.');
    } else if (failure === null) {
        return emptyWithLog('Canceling download not possible anymore, download finished.');
    } else {
        return emptyWithLog(`Canceling download not possible anymore, download ${failure}.`);
    }
}
