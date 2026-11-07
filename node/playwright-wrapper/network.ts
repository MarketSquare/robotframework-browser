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
import { Page, Request, Response as PlaywrightResponse } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import { logger } from './browser_logger';
import { MAX_RESPONSE_CHUNK_BYTES, splitBytes } from './chunking';
import * as pb from './generated/playwright';
import { withLoadReport } from './load-report';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse, parseRegExpOrKeepString } from './response-util';

export async function httpRequest(request: pb.Request_HttpRequest, page: Page): Promise<pb.Response_Json> {
    const opts: { [k: string]: any } = {
        method: request.method,
        url: request.url,
        headers: JSON.parse(request.headers),
    };
    if (opts.method != 'GET') {
        opts.body = request.body;
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
        // eslint-disable-next-line @typescript-eslint/no-implied-eval
        const fn = new Function(`return (${urlOrPredicate})`)();
        if (typeof fn === 'function' || Object.prototype.toString.call(fn) === '[object Function]') {
            return fn;
        }
    }

    return parseRegExpOrKeepString(urlOrPredicate);
}

interface CapturedBytes {
    meta: Record<string, unknown>;
    log: string;
    postData: Buffer | null;
    body: Buffer | null;
}

async function orFallback<T>(read: () => Promise<T>, fallback: T, what: string): Promise<T> {
    try {
        return await read();
    } catch (e) {
        logger.info(`Could not read ${what}: ${String(e)}`);
        return fallback;
    }
}

async function headersOf(message: Request | PlaywrightResponse, what: string): Promise<Record<string, unknown>> {
    const headers = message.headers();
    return {
        allHeaders: await orFallback(() => message.allHeaders(), headers, `${what} headers`),
        headersArray: await orFallback(
            () => message.headersArray(),
            Object.entries(headers).map(([name, value]) => ({ name, value })),
            `${what} headers array`,
        ),
    };
}

function frameOf(request: Request): { url: string; name: string } | null {
    try {
        const frame = request.frame();
        return { url: frame.url(), name: frame.name() };
    } catch {
        return null;
    }
}

async function requestDetails(request: Request): Promise<Record<string, unknown>> {
    const details: Record<string, unknown> = {
        url: request.url(),
        ...(await headersOf(request, 'request')),
        resourceType: request.resourceType(),
        isNavigationRequest: request.isNavigationRequest(),
        redirectedFrom: request.redirectedFrom()?.url() ?? null,
        redirectedTo: request.redirectedTo()?.url() ?? null,
        frame: frameOf(request),
        hasPostData: request.postDataBuffer() !== null,
    };
    return details;
}

function legacyPostData(request: Request): unknown {
    try {
        return JSON.parse(request.postData() || 'null');
    } catch (e) {
        logger.info(`Failed to parse postData as JSON: ${String(e)}, using raw postData`);
        return request.postData();
    }
}

function capturedMessages(captured: CapturedBytes): pb.Response_Json[] {
    const postDataChunks = captured.postData ? splitBytes(captured.postData, MAX_RESPONSE_CHUNK_BYTES) : [];
    const bodyChunks = captured.body ? splitBytes(captured.body, MAX_RESPONSE_CHUNK_BYTES) : [];
    const count = Math.max(postDataChunks.length, bodyChunks.length, 1);
    const messages: pb.Response_Json[] = [];
    for (let i = 0; i < count; i++) {
        messages.push({
            ...jsonResponse(i === 0 ? JSON.stringify(captured.meta) : '', `${captured.log}, chunk ${i + 1}/${count}`),
            postDataBytes: postDataChunks[i] ?? Buffer.alloc(0),
            bodyBytes: bodyChunks[i] ?? Buffer.alloc(0),
        });
    }
    return messages;
}

export async function waitForResponse(request: pb.Request_HttpCapture, page: Page): Promise<pb.Response_Json[]> {
    const urlOrPredicate = deserializeUrlOrPredicate(request.urlOrPredicate);
    const timeout = request.timeout;
    const data = await page.waitForResponse(urlOrPredicate, { timeout });
    const capturedRequest = data.request();
    let body: Buffer | null = null;
    if (!request.excludeBody) {
        body = await orFallback<Buffer | null>(() => data.body(), null, 'response body');
    }
    const meta: Record<string, unknown> = {
        status: data.status(),
        headers: JSON.stringify(data.headers()),
        statusText: data.statusText(),
        url: data.url(),
        ok: data.ok(),
        ...(await headersOf(data, 'response')),
        httpVersion: await orFallback<string | null>(() => data.httpVersion(), null, 'HTTP version'),
        serverAddr: await orFallback(() => data.serverAddr(), null, 'server address'),
        securityDetails: await orFallback(() => data.securityDetails(), null, 'security details'),
        fromServiceWorker: data.fromServiceWorker(),
        hasBody: body !== null,
        request: {
            headers: JSON.stringify(capturedRequest.headers()),
            method: capturedRequest.method(),
            postData: capturedRequest.postData(),
            ...(await requestDetails(capturedRequest)),
        },
    };
    logger.info(`waitForResponse received: ${data.url()} status: ${data.status()}`);
    return capturedMessages({
        meta,
        log: 'Response received',
        postData: capturedRequest.postDataBuffer(),
        body,
    });
}

export async function waitForRequest(request: pb.Request_HttpCapture, page: Page): Promise<pb.Response_Json[]> {
    const urlOrPredicate = deserializeUrlOrPredicate(request.urlOrPredicate);
    const timeout = request.timeout;
    const result = await page.waitForRequest(urlOrPredicate, { timeout });
    const meta = {
        method: result.method(),
        headers: result.headers(),
        postData: legacyPostData(result),
        ...(await requestDetails(result)),
    };
    logger.info(`waitForRequest received: ${result.url()} method: ${result.method()}`);
    const matcherStr = typeof urlOrPredicate === 'string' ? urlOrPredicate : urlOrPredicate.toString();
    return capturedMessages({
        meta,
        log: `Request completed within timeout ${timeout}ms by using matcher: ${matcherStr}`,
        postData: result.postDataBuffer(),
        body: null,
    });
}

export async function waitForNavigation(request: pb.Request_UrlOptions, page: Page): Promise<pb.Response_Empty> {
    const url = parseRegExpOrKeepString(<string>request.url?.url);
    const timeout = request.url?.defaultTimeout;
    const waitUntil = <'load' | 'domcontentloaded' | 'networkidle' | 'commit' | undefined>request.waitUntil;
    await withLoadReport(page, () => page.waitForNavigation({ timeout: timeout, url: url, waitUntil: waitUntil }));
    return emptyWithLog(`Navigated to: ${url}, location is: ${page.url()}`);
}

export async function WaitForPageLoadState(request: pb.Request_PageLoadState, page: Page): Promise<pb.Response_Empty> {
    const state = <'load' | 'domcontentloaded' | 'networkidle' | undefined>request.state;
    const timeout = request.timeout;
    logger.info(`timeout: ${timeout} state: ${state}`);
    await withLoadReport(page, () => page.waitForLoadState(state, { timeout }));
    return emptyWithLog(`Load state ${state} got in ${timeout}`);
}

export async function waitForDownload(
    request: pb.Request_DownloadOptions,
    state: PlaywrightState,
    page: Page,
): Promise<pb.Response_Json> {
    const saveAs = request.path;
    const waitForFinish = request.waitForFinish;
    const downloadTimeout = request.downloadTimeout;
    return await _waitForDownload(page, state, saveAs, downloadTimeout, waitForFinish);
}

export async function _waitForDownload(
    page: Page,
    state: PlaywrightState,
    saveAs: string,
    downloadTimeout: number,
    waitForFinished: boolean,
): Promise<pb.Response_Json> {
    const downloadWaitStartedAt = Date.now();
    const downloadObject = await page.waitForEvent('download', { timeout: downloadTimeout || undefined });

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
        const remainingTimeout = Math.max(downloadTimeout - (Date.now() - downloadWaitStartedAt), 0);
        let timer: NodeJS.Timeout | undefined;
        const readStream = await Promise.race([
            downloadObject.createReadStream(),
            new Promise((resolve) => {
                timer = setTimeout(resolve, remainingTimeout);
            }),
        ]).finally(() => clearTimeout(timer));
        if (!readStream) {
            await downloadObject.cancel();
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
    request: pb.Request_DownloadID,
    state: PlaywrightState,
): Promise<pb.Response_Json> {
    const downloadID = request.id;
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
    request: pb.Request_DownloadID,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const downloadID = request.id;
    const activeIndexedPage = state.activeBrowser?.page;
    if (!activeIndexedPage) {
        throw new Error('No active page found');
    }
    const downloadInfo = activeIndexedPage.activeDownloads.get(downloadID);
    if (!downloadInfo) {
        throw new Error('No download object found for id: ' + downloadID);
    }
    const downloadObject = downloadInfo.downloadObject;
    await downloadObject.cancel();
    const failure = await downloadObject.failure();
    if (failure == 'canceled') {
        return emptyWithLog('Download canceled successfully.');
    } else if (failure === null) {
        return emptyWithLog('Canceling download not possible anymore, download finished.');
    } else {
        return emptyWithLog(`Canceling download not possible anymore, download ${failure}.`);
    }
}
