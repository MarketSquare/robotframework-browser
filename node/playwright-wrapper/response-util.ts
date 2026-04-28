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

import { status } from '@grpc/grpc-js';
import { errors } from 'playwright';

import { errorType, logger } from './browser_logger';
import {
    Response_Bool,
    Response_Empty,
    Response_Int,
    Response_JavascriptExecutionResult,
    Response_Json,
    Response_Keywords,
    Response_PageReportResponse,
    Response_String,
} from './generated/playwright';
import { IndexedPage } from './playwright-state';

export function emptyWithLog(text: string): Response_Empty {
    return { log: text };
}

export function pageReportResponse(log: string, page: IndexedPage): Response_PageReportResponse {
    return {
        log,
        console: JSON.stringify(
            page.consoleMessages.map((m) => ({
                time: m.time,
                type: m.type,
                text: m.text,
                location: m.location,
            })),
        ),
        errors: JSON.stringify(
            page.pageErrors.map((e) => (e ? `${e.name}: ${e.message}\n${e.stack}` : 'unknown error')),
        ),
        pageId: page.id,
    };
}

export function getConsoleLogResponse(page: IndexedPage, fullLog: boolean, message: string): Response_Json {
    const consoleMessages = page.consoleMessages;
    const responseMessages = fullLog ? consoleMessages : consoleMessages.slice(page.consoleIndex);
    page.consoleIndex = consoleMessages.length;
    return { log: message, json: JSON.stringify(responseMessages), bodyPart: '' };
}

export function getErrorMessagesResponse(page: IndexedPage, fullLog: boolean, message: string): Response_Json {
    const pageErrors = page.pageErrors;
    const responseErrors = fullLog ? pageErrors : pageErrors.slice(page.errorIndex);
    page.errorIndex = pageErrors.length;
    return { log: message, json: JSON.stringify(responseErrors), bodyPart: '' };
}

export function stringResponse(body: string, logMessage: string): Response_String {
    return { body, log: logMessage };
}

export function jsonResponse(body: string, logMessage: string, bodyPart: string = ''): Response_Json {
    return { json: body, log: logMessage, bodyPart };
}

export function intResponse(body: number, logMessage: string): Response_Int {
    return { body, log: logMessage };
}

export function boolResponse(value: boolean, logMessage: string): Response_Bool {
    return { body: value, log: logMessage };
}

export function jsResponse(result: string, logMessage: string): Response_JavascriptExecutionResult {
    return { result: JSON.stringify(result), log: logMessage };
}

export function errorResponse(e: unknown) {
    logger.error(
        { event_kind: 'grpc_error', status: 'failed', error_type: errorType(e) },
        e instanceof Error ? (e.stack ?? e.message) : String(e),
    );
    if (!(e instanceof Error)) return null;
    const errorMessage: string = e.toString().substring(0, 5000);
    let errorCode = status.RESOURCE_EXHAUSTED;
    if (e instanceof errors.TimeoutError) {
        errorCode = status.DEADLINE_EXCEEDED;
    }
    return { code: errorCode, message: errorMessage };
}

export function keywordsResponse(
    keywords: string[],
    keywordArguments: string[],
    keywordDocs: string[],
    logMessage: string,
) {
    return {
        keywords,
        keywordDocumentations: keywordDocs,
        keywordArguments,
        log: logMessage,
    } satisfies Response_Keywords;
}

export function parseRegExpOrKeepString(str: string): RegExp | string {
    const regex = /^\/(?<matcher>.*)\/(?<flags>[gimsuy]+)?$/;
    try {
        const match = str.match(regex);
        if (match) {
            const { matcher, flags } = match.groups!;
            return new RegExp(matcher, flags);
        }
        return str;
    } catch {
        return str;
    }
}
