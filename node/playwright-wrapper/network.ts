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

import * as pb from './generated/playwright_pb';
import { Page } from 'playwright';

import { emptyWithLog, jsonResponse, stringResponse } from './response-util';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

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
    return jsonResponse(JSON.stringify(response), 'Request performed succesfully.');
}

export async function waitForResponse(request: pb.Request.HttpCapture, page: Page): Promise<pb.Response.Json> {
    const urlOrPredicate = new RegExp(`.*${request.getUrlorpredicate()}`);
    const timeout = request.getTimeout();
    const data = await page.waitForResponse(urlOrPredicate, { timeout });
    return jsonResponse(
        JSON.stringify({
            status: data.status(),
            body: await data.text(),
            headers: JSON.stringify(data.headers()),
            statusText: data.statusText(),
            url: data.url(),
            ok: data.ok(),
            request: {
                headers: JSON.stringify(data.request().headers()),
                method: data.request().method(),
                postData: data.request().postData(),
            },
        }),
        '',
    );
}
export async function waitForRequest(request: pb.Request.HttpCapture, page: Page): Promise<pb.Response.String> {
    const urlOrPredicate = request.getUrlorpredicate();
    const timeout = request.getTimeout();
    const result = await page.waitForRequest(urlOrPredicate, { timeout });
    return stringResponse(result.url(), 'Requested compeleted withing timeout.');
}

export async function waitUntilNetworkIsIdle(request: pb.Request.Timeout, page: Page): Promise<pb.Response.Empty> {
    const timeout = request.getTimeout();
    await page.waitForLoadState('networkidle', { timeout });
    return emptyWithLog('Network is idle');
}

export async function waitForNavigation(request: pb.Request.Url, page: Page): Promise<pb.Response.Empty> {
    const url = request.getUrl();
    const timeout = request.getDefaulttimeout();
    await page.waitForNavigation({timeout, url})
    return emptyWithLog(`Navigated to ${url}`);
}

export async function waitForDownload(request: pb.Request.FilePath, page: Page): Promise<pb.Response.Json> {
    const saveAs = request.getPath();
    const downloadObject = await page.waitForEvent('download');

    if (saveAs) {
        await downloadObject.saveAs(saveAs);
    }
    const path = await downloadObject.path();
    const fileName = downloadObject.suggestedFilename();
    logger.info('suggestedFilename: ' + fileName + ' saveAs path: ' + path);
    return jsonResponse(
        JSON.stringify({ saveAs: path, suggestedFilename: fileName }),
        'Download done successfully to: ' + path,
    );
}
