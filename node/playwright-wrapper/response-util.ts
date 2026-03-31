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

// Responses are plain ts-proto messages; no compatibility getters required.

export function emptyWithLog(text: string): Response_Empty {
    return Response_Empty.create({ log: text });
}

// use addGetters from proto-compat

export function pageReportResponse(log: string, page: IndexedPage): Response_PageReportResponse {
    return Response_PageReportResponse.create({
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
    });
}

export function getConsoleLogResponse(page: IndexedPage, fullLog: boolean, message: string): Response_Json {
    const consoleMessages = page.consoleMessages;
    const reponseMessages = fullLog ? consoleMessages : consoleMessages.slice(page.consoleIndex);
    page.consoleIndex = consoleMessages.length;
    return Response_Json.create({ log: message, json: JSON.stringify(reponseMessages) });
}

export function getErrorMessagesResponse(page: IndexedPage, fullLog: boolean, message: string): Response_Json {
    const pageErrors = page.pageErrors;
    const reponseErrors = fullLog ? pageErrors : pageErrors.slice(page.errorIndex);
    page.errorIndex = pageErrors.length;
    return Response_Json.create({ log: message, json: JSON.stringify(reponseErrors) });
}

export function stringResponse(body: string, logMessage: string): Response_String {
    return Response_String.create({ body, log: logMessage });
}

export function jsonResponse(body: string, logMessage: string, bodyPart: string = ''): Response_Json {
    return Response_Json.create({ json: body, log: logMessage, bodyPart });
}

export function intResponse(body: number, logMessage: string): Response_Int {
    return Response_Int.create({ body, log: logMessage });
}

export function boolResponse(value: boolean, logMessage: string): Response_Bool {
    return Response_Bool.create({ body: value, log: logMessage });
}

export function jsResponse(result: string, logMessage: string): Response_JavascriptExecutionResult {
    return Response_JavascriptExecutionResult.create({ result: JSON.stringify(result), log: logMessage });
}

export function errorResponse(e: unknown) {
    console.log('================= Original suppressed error =================');
    console.log(e);
    console.log('=============================================================');
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
): Response_Keywords {
    return Response_Keywords.create({
        keywords,
        keywordDocumentations: keywordDocs,
        keywordArguments,
        log: logMessage,
    });
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
