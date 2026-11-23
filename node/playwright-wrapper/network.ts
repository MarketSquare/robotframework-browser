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

import * as fs from 'fs';
import * as path from 'path';
import { APIRequestContext, BrowserContext, Page, Request, Response as PlaywrightResponse } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import { logger } from './browser_logger';
import { MAX_RESPONSE_CHUNK_BYTES, splitBytes } from './chunking';
import * as pb from './generated/playwright';
import { withLoadReport } from './load-report';
import { LifecycleState, navigationOptions } from './navigation-options';
import { exists } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import {
    deserializeUrlOrPredicate,
    emptyWithLog,
    hideCallLog,
    jsonResponse,
    parseRegExpOrKeepStringOrThrow,
} from './response-util';

type PageMultipartField =
    { name: string; value: string } | { name: string; fileName?: string; mimeType?: string; buffer: Uint8Array };

interface PageFetchArguments {
    url: string;
    init: Record<string, unknown>;
    text?: string;
    bytes?: Uint8Array;
    form?: [string, string][];
    multipart?: PageMultipartField[];
    timeout: number;
}

interface PageFetchResult {
    timedOut: boolean;
    status: number;
    statusText: string;
    url: string;
    ok: boolean;
    redirected: boolean;
    type: string;
    headers: Record<string, string>;
    body: Uint8Array;
}

async function multipartFileContent(field: pb.Request_MultipartField): Promise<Uint8Array | undefined> {
    return field.path !== undefined ? await fs.promises.readFile(field.path) : field.buffer;
}

async function pageMultipartField(field: pb.Request_MultipartField): Promise<PageMultipartField> {
    const content = await multipartFileContent(field);
    if (content === undefined) {
        return { name: field.name, value: field.value ?? '' };
    }
    return { name: field.name, fileName: field.fileName, mimeType: field.mimeType, buffer: new Uint8Array(content) };
}

function requestInit(request: pb.Request_HttpRequest): Record<string, unknown> {
    const init: Record<string, unknown> = { method: request.method, headers: JSON.parse(request.headers) };
    const options = {
        credentials: request.credentials,
        redirect: request.redirect,
        mode: request.mode,
        cache: request.cache,
        referrer: request.referrer,
        referrerPolicy: request.referrerPolicy,
        integrity: request.integrity,
        keepalive: request.keepalive,
        priority: request.priority,
    };
    for (const [name, value] of Object.entries(options)) {
        if (value !== undefined) init[name] = value;
    }
    return init;
}

/**
 * Runs in the page through `page.evaluate`, so it uses only the browser's fetch API and
 * nothing from this module's scope.
 */
export async function pageFetch({
    url,
    init,
    text,
    bytes,
    form,
    multipart,
    timeout,
}: PageFetchArguments): Promise<PageFetchResult> {
    const options: Record<string, unknown> = { ...init };
    if (text !== undefined) {
        options.body = text;
    } else if (bytes !== undefined) {
        options.body = bytes;
    } else if (form !== undefined) {
        options.body = new URLSearchParams(form);
    } else if (multipart !== undefined) {
        const formData = new FormData();
        for (const field of multipart) {
            if ('buffer' in field) {
                formData.append(
                    field.name,
                    new Blob([new Uint8Array(field.buffer)], { type: field.mimeType }),
                    field.fileName,
                );
            } else {
                formData.append(field.name, field.value);
            }
        }
        options.body = formData;
    }
    if (timeout > 0) {
        options.signal = AbortSignal.timeout(timeout);
    }
    try {
        const response = await fetch(url, options);
        const body = new Uint8Array(await response.arrayBuffer());
        const headers: Record<string, string> = {};
        response.headers.forEach((value, name) => (headers[name] = value));
        return {
            timedOut: false,
            status: response.status,
            statusText: response.statusText,
            url: response.url,
            ok: response.ok,
            redirected: response.redirected,
            type: response.type,
            headers,
            body,
        };
    } catch (error) {
        if (error instanceof DOMException && error.name === 'TimeoutError') {
            return { timedOut: true } as PageFetchResult;
        }
        throw error;
    }
}

export async function httpRequest(request: pb.Request_HttpRequest, page: Page): Promise<pb.Response_Json[]> {
    const form = request.form?.fields.map((field): [string, string] => [field.name, field.value]);
    const multipart = request.multipart && (await Promise.all(request.multipart.fields.map(pageMultipartField)));
    const result = await page.evaluate(pageFetch, {
        url: request.url,
        init: requestInit(request),
        text: request.body,
        bytes: request.bodyBytes !== undefined ? new Uint8Array(request.bodyBytes) : undefined,
        form,
        multipart,
        timeout: request.timeout,
    });
    if (result.timedOut) {
        throw new Error(`Timeout ${request.timeout}ms exceeded while waiting for the response of ${request.url}.`);
    }
    const meta = {
        status: result.status,
        statusText: result.statusText,
        ok: result.ok,
        url: result.url,
        headers: JSON.stringify(result.headers),
        redirected: result.redirected,
        type: result.type,
    };
    return capturedMessages({
        meta,
        log: 'Request performed successfully.',
        postData: null,
        body: Buffer.from(result.body),
    });
}

type ApiFetchOptions = NonNullable<Parameters<APIRequestContext['fetch']>[1]>;

function searchParams(fields: pb.Request_FormField[]): URLSearchParams {
    return new URLSearchParams(fields.map((field): [string, string] => [field.name, field.value]));
}

function formData(fields: pb.Request_FormField[]): FormData {
    const form = new FormData();
    for (const field of fields) form.append(field.name, field.value);
    return form;
}

async function multipartFormData(fields: pb.Request_MultipartField[]): Promise<FormData> {
    const form = new FormData();
    for (const field of fields) {
        const content = await multipartFileContent(field);
        if (content === undefined) {
            form.append(field.name, field.value ?? '');
        } else {
            const type = field.mimeType ?? 'application/octet-stream';
            form.append(field.name, new Blob([new Uint8Array(content)], { type }), field.fileName ?? field.name);
        }
    }
    return form;
}

function hasHeader(headers: Record<string, string>, name: string): boolean {
    return Object.keys(headers).some((key) => key.toLowerCase() === name);
}

function setApiRequestData(options: ApiFetchOptions, request: pb.Request_ApiRequest): void {
    if (request.dataText !== undefined) {
        options.data = request.dataText;
    } else if (request.dataBytes !== undefined) {
        options.data = Buffer.from(request.dataBytes);
    } else if (request.dataJson !== undefined) {
        // Playwright sends a JSON string as written when the content type is JSON, so the
        // JSON that Python wrote reaches the server unchanged, large integers included.
        const headers = (options.headers ?? {}) as Record<string, string>;
        if (!hasHeader(headers, 'content-type')) headers['content-type'] = 'application/json';
        options.headers = headers;
        options.data = request.dataJson;
    }
}

async function apiFetchOptions(request: pb.Request_ApiRequest): Promise<ApiFetchOptions> {
    const options: ApiFetchOptions = { method: request.method, timeout: request.timeout };
    if (request.headers !== undefined) options.headers = JSON.parse(request.headers);
    if (request.encodedParams !== undefined) {
        options.params = request.encodedParams;
    } else if (request.params !== undefined) {
        options.params = searchParams(request.params.fields);
    }
    setApiRequestData(options, request);
    if (request.form !== undefined) options.form = formData(request.form.fields);
    if (request.multipart !== undefined) options.multipart = await multipartFormData(request.multipart.fields);
    if (request.failOnStatusCode !== undefined) options.failOnStatusCode = request.failOnStatusCode;
    if (request.maxRedirects !== undefined) options.maxRedirects = request.maxRedirects;
    if (request.maxRetries !== undefined) options.maxRetries = request.maxRetries;
    if (request.ignoreHTTPSErrors !== undefined) options.ignoreHTTPSErrors = request.ignoreHTTPSErrors;
    return options;
}

export async function sendApiRequest(
    request: pb.Request_ApiRequest,
    context: BrowserContext | undefined,
): Promise<pb.Response_Json[]> {
    exists(context, 'Tried to send an API request, but no context was open.');
    const response = await context.request
        .fetch(request.url, await apiFetchOptions(request))
        .catch((error: unknown) => {
            throw hideCallLog(error);
        });
    try {
        const meta = {
            status: response.status(),
            statusText: response.statusText(),
            ok: response.ok(),
            url: response.url(),
            headers: response.headers(),
            headersArray: response.headersArray(),
        };
        return capturedMessages({ meta, log: 'API request sent.', postData: null, body: await response.body() });
    } finally {
        await response.dispose();
    }
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

const UNAVAILABLE_HEADERS = { allHeaders: null, headersArray: null };

async function headersOf(message: Request | PlaywrightResponse): Promise<Record<string, unknown>> {
    const [allHeaders, headersArray] = await Promise.all([message.allHeaders(), message.headersArray()]);
    return { allHeaders, headersArray };
}

async function headersOrNull(message: Request | PlaywrightResponse, what: string): Promise<Record<string, unknown>> {
    return orFallback(() => headersOf(message), UNAVAILABLE_HEADERS, `${what} headers`);
}

function frameOf(request: Request): { url: string; name: string } | null {
    try {
        const frame = request.frame();
        return { url: frame.url(), name: frame.name() };
    } catch {
        return null;
    }
}

async function withinTimeout<T>(read: Promise<T>, remaining: number, timeoutMessage: string): Promise<T> {
    if (remaining <= 0) return read;
    let timer: NodeJS.Timeout | undefined;
    const expired = new Promise<never>((_, reject) => {
        timer = setTimeout(() => reject(new Error(timeoutMessage)), remaining);
    });
    try {
        return await Promise.race([read, expired]);
    } finally {
        clearTimeout(timer);
    }
}

const STATUSES_WITHOUT_BODY = new Set([204, 205, 304]);

function isRedirect(status: number): boolean {
    return status >= 300 && status < 400 && status !== 304;
}

function emptyBodyOrNull(response: PlaywrightResponse): Buffer | null {
    const status = response.status();
    const hasNoBody =
        STATUSES_WITHOUT_BODY.has(status) || (!isRedirect(status) && response.headers()['content-length'] === '0');
    return hasNoBody ? Buffer.alloc(0) : null;
}

function remainingTime(timeout: number, started: number): number {
    return timeout > 0 ? Math.max(timeout - (Date.now() - started), 1) : 0;
}

function requestDetails(request: Request, headers: Record<string, unknown>): Record<string, unknown> {
    return {
        url: request.url(),
        ...headers,
        resourceType: request.resourceType(),
        isNavigationRequest: request.isNavigationRequest(),
        redirectedFrom: request.redirectedFrom()?.url() ?? null,
        redirectedTo: request.redirectedTo()?.url() ?? null,
        frame: frameOf(request),
        hasPostData: request.postDataBuffer() !== null,
    };
}

function capturedMessages(captured: CapturedBytes): pb.Response_Json[] {
    const postDataChunks = captured.postData ? splitBytes(captured.postData, MAX_RESPONSE_CHUNK_BYTES) : [];
    const bodyChunks = captured.body ? splitBytes(captured.body, MAX_RESPONSE_CHUNK_BYTES) : [];
    const count = Math.max(postDataChunks.length, bodyChunks.length, 1);
    const firstLog = count > 1 ? `${captured.log}, sent in ${count} chunks` : captured.log;
    const messages: pb.Response_Json[] = [];
    for (let i = 0; i < count; i++) {
        messages.push({
            ...(i === 0 ? jsonResponse(JSON.stringify(captured.meta), firstLog) : jsonResponse('', '')),
            postDataBytes: postDataChunks[i] ?? Buffer.alloc(0),
            bodyBytes: bodyChunks[i] ?? Buffer.alloc(0),
        });
    }
    return messages;
}

export async function waitForResponse(request: pb.Request_HttpCapture, page: Page): Promise<pb.Response_Json[]> {
    const urlOrPredicate = deserializeUrlOrPredicate(request.urlOrPredicate);
    const timeout = request.timeout;
    const started = Date.now();
    const data = await page.waitForResponse(urlOrPredicate, { timeout });
    const capturedRequest = data.request();
    const withBody = !request.excludeBody;
    const [body, responseHeaders, httpVersion, serverAddr, securityDetails, requestHeaders] = await withinTimeout(
        Promise.all([
            withBody ? orFallback<Buffer | null>(() => data.body(), emptyBodyOrNull(data), 'response body') : null,
            headersOrNull(data, 'response'),
            withBody ? orFallback<string | null>(() => data.httpVersion(), null, 'HTTP version') : null,
            withBody ? orFallback(() => data.serverAddr(), null, 'server address') : null,
            withBody ? orFallback(() => data.securityDetails(), null, 'security details') : null,
            headersOrNull(capturedRequest, 'request'),
        ]),
        remainingTime(timeout, started),
        `Timeout ${timeout}ms exceeded while waiting for all fields of the response.`,
    );
    const meta: Record<string, unknown> = {
        status: data.status(),
        headers: JSON.stringify(data.headers()),
        statusText: data.statusText(),
        url: data.url(),
        ok: data.ok(),
        ...responseHeaders,
        httpVersion,
        serverAddr,
        securityDetails,
        fromServiceWorker: data.fromServiceWorker(),
        hasBody: body !== null,
        request: {
            headers: JSON.stringify(capturedRequest.headers()),
            method: capturedRequest.method(),
            ...requestDetails(capturedRequest, requestHeaders),
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
    const started = Date.now();
    const result = await page.waitForRequest(urlOrPredicate, { timeout });
    const headers = request.waitForAllFields
        ? await withinTimeout(
              headersOf(result),
              remainingTime(timeout, started),
              `Timeout ${timeout}ms exceeded while waiting for all fields of the request.`,
          )
        : UNAVAILABLE_HEADERS;
    const meta = {
        method: result.method(),
        headers: result.headers(),
        ...requestDetails(result, headers),
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
    const url = parseRegExpOrKeepStringOrThrow(<string>request.url?.url);
    const options = { ...navigationOptions(request.url?.defaultTimeout, request.waitUntil), url };
    await withLoadReport(page, () => page.waitForNavigation(options));
    return emptyWithLog(`Navigated to: ${url}, location is: ${page.url()}`);
}

export async function WaitForPageLoadState(request: pb.Request_PageLoadState, page: Page): Promise<pb.Response_Empty> {
    const state = <LifecycleState | undefined>request.state;
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
    const downloadWaitStartedAt = performance.now();
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
        const remainingTimeout = Math.max(downloadTimeout - (performance.now() - downloadWaitStartedAt), 0);
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
