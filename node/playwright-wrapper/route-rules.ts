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

import { randomUUID } from 'crypto';
import { APIResponse, BrowserContext, Disposable, Page, Request, Route } from 'playwright';

import { logger } from './browser_logger';
import { isTargetClosed } from './context-tracer';
import * as pb from './generated/playwright';
import { exists } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, parseRegExpOrKeepStringOrThrow } from './response-util';

type RouteAction = (route: Route) => Promise<void>;

type RouteRule = {
    id: string;
    page: Page | undefined;
    disposable: Disposable | undefined;
    inFlight: Set<Promise<void>>;
    runs: number;
};

export class RouteRules {
    private rules = new Map<string, RouteRule>();

    add(rule: RouteRule): void {
        this.rules.set(rule.id, rule);
    }

    take(id: string): RouteRule | undefined {
        const rule = this.rules.get(id);
        this.rules.delete(id);
        return rule;
    }

    takeAll(): RouteRule[] {
        const rules = [...this.rules.values()];
        this.rules.clear();
        return rules;
    }

    dropPage(page: Page): void {
        for (const rule of this.rules.values()) {
            if (rule.page === page) this.rules.delete(rule.id);
        }
    }

    clear(): void {
        this.rules.clear();
    }
}

type JsonObject = { [key: string]: unknown };
type FetchOptions = NonNullable<Parameters<Route['fetch']>[0]>;
type Headers = Record<string, string>;

function isJsonObject(value: unknown): value is JsonObject {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function setOwnPropertyEvenIfProto(object: JsonObject, key: string, value: unknown): void {
    Object.defineProperty(object, key, { value, enumerable: true, writable: true, configurable: true });
}

export function jsonMergePatch(target: unknown, patch: unknown): unknown {
    if (!isJsonObject(patch)) return patch;
    const merged: JsonObject = isJsonObject(target) ? { ...target } : {};
    for (const [key, value] of Object.entries(patch)) {
        if (value === null) delete merged[key];
        else setOwnPropertyEvenIfProto(merged, key, jsonMergePatch(merged[key], value));
    }
    return merged;
}

function withoutHeaders(headers: Headers, names: Set<string>): Headers {
    return Object.fromEntries(Object.entries(headers).filter(([name]) => !names.has(name.toLowerCase())));
}

function mergeHeaders(real: Headers, changes: Headers): Headers {
    const merged = withoutHeaders(real, new Set(Object.keys(changes).map((name) => name.toLowerCase())));
    for (const [name, value] of Object.entries(changes)) {
        if (value !== '') merged[name] = value;
    }
    return merged;
}

const STALE_BODY_HEADERS = new Set(['content-encoding', 'content-length']);
const ORIGINAL_TARGET_HEADERS = new Set(['host', 'cookie']);
const BODYLESS_METHODS = new Set(['GET', 'HEAD']);

async function modifiedBody(modify: pb.Request_RouteModify, response: APIResponse): Promise<Buffer | undefined> {
    if (modify.jsonPatch === undefined) return modify.body;
    const real: unknown = JSON.parse((await response.body()).toString('utf8'));
    return Buffer.from(JSON.stringify(jsonMergePatch(real, JSON.parse(modify.jsonPatch))));
}

function fetchOptions(modify: pb.Request_RouteModify, request: Request): FetchOptions {
    const options: FetchOptions = { timeout: modify.timeout };
    let headers = request.headers();
    if (modify.url !== undefined) {
        options.url = new URL(modify.url, request.url()).toString();
        headers = withoutHeaders(headers, ORIGINAL_TARGET_HEADERS);
    }
    if (modify.url !== undefined || Object.keys(modify.requestHeaders).length > 0) {
        options.headers = mergeHeaders(headers, modify.requestHeaders);
    }
    if (modify.method !== undefined) options.method = modify.method;
    if (modify.postData !== undefined) options.postData = modify.postData;
    else if (modify.method !== undefined && BODYLESS_METHODS.has(modify.method)) options.postData = Buffer.alloc(0);
    return options;
}

function withoutCallLog(error: unknown): string {
    const message = error instanceof Error ? error.message : String(error);
    return message.split(/\n\s*Call log:/)[0];
}

async function fetchAndFulfill(route: Route, modify: pb.Request_RouteModify): Promise<void> {
    const response = await route.fetch(fetchOptions(modify, route.request()));
    const body = await modifiedBody(modify, response);
    const realHeaders =
        body === undefined ? response.headers() : withoutHeaders(response.headers(), STALE_BODY_HEADERS);
    await route.fulfill({ response, status: modify.status, headers: mergeHeaders(realHeaders, modify.headers), body });
}

function modifyAction(modify: pb.Request_RouteModify): RouteAction {
    return async (route) => {
        try {
            await fetchAndFulfill(route, modify);
        } catch (error) {
            const failure = new Error(`request failed: ${withoutCallLog(error)}`, { cause: error });
            await route.abort('failed').catch((abortError: unknown) => {
                logger.info(`Could not abort ${route.request().url()}: ${withoutCallLog(abortError)}`);
            });
            throw failure;
        }
    };
}

function routeAction(request: pb.Request_RouteRule): RouteAction {
    if (request.abort) {
        const errorCode = request.abort.errorCode;
        return (route) => route.abort(errorCode);
    }
    if (request.fulfill) {
        const { status, headers, body } = request.fulfill;
        return (route) => route.fulfill({ status, headers, body });
    }
    if (request.modify) return modifyAction(request.modify);
    throw new Error('Route rule has no action.');
}

async function addRouteRule(
    target: BrowserContext | Page,
    page: Page | undefined,
    rules: RouteRules,
    request: pb.Request_RouteRule,
): Promise<pb.Response_RouteRuleId> {
    const url = parseRegExpOrKeepStringOrThrow(request.url);
    const action = routeAction(request);
    const rule: RouteRule = { id: randomUUID(), page, disposable: undefined, inFlight: new Set(), runs: 0 };
    let remaining = request.times;
    const handler = (route: Route): Promise<void> => {
        if (remaining !== undefined) remaining -= 1;
        rule.runs += 1;
        logger.info(`Route rule ${rule.id} ran for ${route.request().method()} ${route.request().url()}`);
        const call: Promise<void> = action(route)
            .catch((error: unknown) => logger.info(`Route rule ${rule.id} failed: ${String(error)}`))
            .finally(() => {
                rule.inFlight.delete(call);
                if (remaining === 0 && rule.inFlight.size === 0) rules.take(rule.id);
            });
        rule.inFlight.add(call);
        return call;
    };
    rules.add(rule);
    try {
        rule.disposable = await target.route(url, handler, { times: request.times });
    } catch (error) {
        rules.take(rule.id);
        throw error;
    }
    return { id: rule.id };
}

export async function addContextRoute(
    request: pb.Request_RouteRule,
    state: PlaywrightState,
): Promise<pb.Response_RouteRuleId> {
    const context = state.activeBrowser?.context;
    exists(context, 'Tried to add a route rule, but no context was open.');
    return addRouteRule(context.c, undefined, context.routeRules, request);
}

export async function addPageRoute(
    request: pb.Request_RouteRule,
    state: PlaywrightState,
): Promise<pb.Response_RouteRuleId> {
    const context = state.activeBrowser?.context;
    const page = state.activeBrowser?.page;
    exists(context, 'Tried to add a route rule, but no context was open.');
    exists(page, 'Tried to add a route rule, but no page was open.');
    return addRouteRule(page.p, page.p, context.routeRules, request);
}

function ranTimes(rule: RouteRule): string {
    return rule.runs === 1 ? '1 time' : `${rule.runs} times`;
}

async function endRule(rule: RouteRule): Promise<void> {
    try {
        await rule.disposable?.dispose();
    } catch (error) {
        if (!isTargetClosed(error)) throw error;
    }
    await Promise.allSettled(rule.inFlight);
}

export async function removeRouteRule(
    request: pb.Request_RouteRuleId,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    for (const browser of state.browserStack) {
        for (const context of browser.contextStack) {
            const rule = context.routeRules.take(request.id);
            if (rule) {
                await endRule(rule);
                return emptyWithLog(`Removed route rule ${request.id}. It ran ${ranTimes(rule)}.`);
            }
        }
    }
    return emptyWithLog(`No route rule ${request.id}: it was removed, used up, or its context or page closed.`);
}

export async function removeAllRouteRules(
    _request: pb.Request_Empty,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const context = state.activeBrowser?.context;
    if (context === undefined) return emptyWithLog('No context open, no route rules to remove.');
    const rules = context.routeRules.takeAll();
    const results = await Promise.allSettled(rules.map(endRule));
    const failure = results.find((result) => result.status === 'rejected');
    if (failure) throw failure.reason;
    const pageRules = rules.filter((rule) => rule.page !== undefined).length;
    const summary = `Removed ${rules.length - pageRules} Context and ${pageRules} Page route rules from context ${context.id}.`;
    const ruleLines = rules.map(
        (rule) => `${rule.page === undefined ? 'Context' : 'Page'} route rule ${rule.id} ran ${ranTimes(rule)}.`,
    );
    return emptyWithLog([summary, ...ruleLines].join('\n'));
}
