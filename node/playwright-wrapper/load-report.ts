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

import { errors, Page, Request } from 'playwright';

import { logger } from './browser_logger';

type OpenRequest = {
    startedAt: number;
    order: number;
};

type RequestTracker = {
    outstanding: Map<Request, OpenRequest>;
    requestCount: number;
    document?: Request;
    documentAnsweredAt: number;
    navigation: 'committed' | 'pending' | 'failed';
};

const PROBE_TIMEOUT_MS = 500;
const MAX_REQUESTS = 20;
const MAX_URL_LENGTH = 150;
// Sent as gRPC metadata, base64 encoded, which must stay below the 8 KB metadata limit.
const MAX_REPORT_BYTES = 4096;

const trackers = new WeakMap<Page, RequestTracker>();
const loadReports = new WeakMap<Error, string>();

export function trackRequests(page: Page): void {
    const tracker: RequestTracker = {
        outstanding: new Map(),
        requestCount: 0,
        documentAnsweredAt: 0,
        navigation: 'committed',
    };
    page.on(
        'request',
        guarded((request) => {
            tracker.requestCount += 1;
            tracker.outstanding.set(request, { startedAt: Date.now(), order: tracker.requestCount });
            if (isPageDocument(page, request)) {
                tracker.document = request;
                tracker.navigation = 'pending';
            }
        }),
    );
    page.on(
        'response',
        guarded((response) => {
            if (response.request() === tracker.document) {
                tracker.navigation = 'committed';
                tracker.documentAnsweredAt = tracker.requestCount;
            }
        }),
    );
    page.on(
        'requestfinished',
        guarded((request) => tracker.outstanding.delete(request)),
    );
    page.on(
        'requestfailed',
        guarded((request) => {
            tracker.outstanding.delete(request);
            if (request === tracker.document) {
                tracker.navigation = 'failed';
            }
        }),
    );
    // Chromium drops the requests of the document it leaves without Playwright firing requestfailed.
    page.on(
        'framenavigated',
        guarded((frame) => {
            if (frame !== page.mainFrame() || tracker.navigation !== 'committed') {
                return;
            }
            for (const [request, { order }] of tracker.outstanding) {
                if (order <= tracker.documentAnsweredAt && request !== tracker.document) {
                    tracker.outstanding.delete(request);
                }
            }
        }),
    );
    trackers.set(page, tracker);
}

// Playwright cannot tell the frame of a navigation request issued before its frame exists.
function isPageDocument(page: Page, request: Request): boolean {
    if (!request.isNavigationRequest()) {
        return false;
    }
    try {
        return request.frame() === page.mainFrame();
    } catch {
        return false;
    }
}

// A listener that throws would crash the Node process, and these run on every page.
function guarded<T>(listener: (event: T) => void): (event: T) => void {
    return (event) => {
        try {
            listener(event);
        } catch (e) {
            logger.info(`Load report request tracking failed: ${String(e)}`);
        }
    };
}

export async function withLoadReport<T>(page: Page, wait: () => Promise<T>): Promise<T> {
    try {
        return await wait();
    } catch (e) {
        if (e instanceof errors.TimeoutError) {
            try {
                loadReports.set(e, await buildLoadReport(page));
            } catch (reportError) {
                logger.error(`Building the load report failed: ${String(reportError)}`);
            }
        }
        throw e;
    }
}

export function loadReportOf(error: unknown): string | undefined {
    return error instanceof Error ? loadReports.get(error) : undefined;
}

async function buildLoadReport(page: Page): Promise<string> {
    const tracker = trackers.get(page);
    if (tracker === undefined) {
        throw Error('The page requests are not tracked');
    }
    const now = Date.now();
    const lines = ['Load report of the page when the wait timed out:', `URL: ${page.url()}`];
    if (tracker.navigation === 'pending') {
        lines.push(`Navigation committed: no (waiting for ${cutUrl(tracker.document?.url() ?? '')})`);
    } else if (tracker.navigation === 'failed') {
        lines.push('Navigation committed: no (document request failed)', ...(await documentProgress(page)));
    } else {
        lines.push('Navigation committed: yes', ...(await documentProgress(page)));
    }
    lines.push(`Outstanding requests: ${tracker.outstanding.size}`);
    for (const [request, { startedAt }] of [...tracker.outstanding].slice(0, MAX_REQUESTS)) {
        const url = cutUrl(request.url());
        lines.push(`${request.method()} ${url} [${request.resourceType()}] open for ${now - startedAt} ms`);
    }
    if (tracker.outstanding.size > MAX_REQUESTS) {
        lines.push(`... and ${tracker.outstanding.size - MAX_REQUESTS} more`);
    }
    return withinMaxBytes(lines);
}

function cutUrl(url: string): string {
    return url.length > MAX_URL_LENGTH ? `${url.slice(0, MAX_URL_LENGTH - 1)}…` : url;
}

function withinMaxBytes(lines: string[]): string {
    const report = lines.join('\n');
    if (Buffer.byteLength(report, 'utf8') <= MAX_REPORT_BYTES) {
        return report;
    }
    const marker = '... load report truncated';
    const kept: string[] = [];
    for (const line of lines) {
        if (Buffer.byteLength([...kept, line, marker].join('\n'), 'utf8') > MAX_REPORT_BYTES) {
            break;
        }
        kept.push(line);
    }
    return [...kept, marker].join('\n');
}

async function documentProgress(page: Page): Promise<string[]> {
    const probe = page.evaluate(() => {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
        return {
            readyState: document.readyState,
            domContentLoaded: navigation?.domContentLoadedEventEnd ?? 0,
            load: navigation?.loadEventEnd ?? 0,
        };
    });
    let timer: NodeJS.Timeout | undefined;
    const giveUp = new Promise<never>((_, reject) => {
        timer = setTimeout(() => reject(Error(`no answer in ${PROBE_TIMEOUT_MS} ms`)), PROBE_TIMEOUT_MS);
    });
    let progress;
    try {
        progress = await Promise.race([probe, giveUp]);
    } catch (e) {
        const reason = e instanceof Error ? e.message : String(e);
        logger.info(`Load report could not ask the page: ${reason}`);
        return [`readyState: unknown (probe failed: ${reason})`];
    } finally {
        clearTimeout(timer);
        probe.catch(() => undefined);
    }
    return [
        `readyState: ${progress.readyState}`,
        `DOMContentLoaded: ${eventTime(progress.domContentLoaded)}, load: ${eventTime(progress.load)}`,
    ];
}

function eventTime(milliseconds: number): string {
    return milliseconds > 0 ? `${Math.round(milliseconds)} ms` : 'never fired';
}
