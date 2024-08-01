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

import { IndexedPage } from './playwright-state';
import { Response } from './generated/playwright_pb';
import { errors } from 'playwright';
import { status } from '@grpc/grpc-js';

export function emptyWithLog(text: string): Response.Empty {
    const response = new Response.Empty();
    response.setLog(text);
    return response;
}

export function pageReportResponse(log: string, page: IndexedPage): Response.PageReportResponse {
    const response = new Response.PageReportResponse();
    response.setLog(log);
    response.setConsole(
        JSON.stringify(
            page.consoleMessages.map((m) => ({
                time: m.time,
                type: m.type,
                text: m.text,
                location: m.location,
            })),
        ),
    );
    response.setErrors(
        JSON.stringify(page.pageErrors.map((e) => (e ? `${e.name}: ${e.message}\n${e.stack}` : 'unknown error'))),
    );
    response.setPageid(page.id);
    return response;
}

export function getConsoleLogResponse(page: IndexedPage, fullLog: boolean, message: string): Response.Json {
    const response = new Response.Json();
    const consoleMessages = page.consoleMessages;
    const reponseMessages = fullLog ? consoleMessages : consoleMessages.slice(page.consoleIndex);
    page.consoleIndex = consoleMessages.length;
    response.setLog(message);
    response.setJson(JSON.stringify(reponseMessages));
    return response;
}

export function getErrorMessagesResponse(page: IndexedPage, fullLog: boolean, message: string): Response.Json {
    const response = new Response.Json();
    const pageErrors = page.pageErrors;
    const reponseErrors = fullLog ? pageErrors : pageErrors.slice(page.errorIndex);
    page.errorIndex = pageErrors.length;
    response.setLog(message);
    response.setJson(JSON.stringify(reponseErrors));
    return response;
}

export function stringResponse(body: string, logMessage: string): Response.String {
    const response = new Response.String();
    response.setBody(body);
    response.setLog(logMessage);
    return response;
}

export function jsonResponse(body: string, logMessage: string) {
    const response = new Response.Json();
    response.setJson(body);
    response.setLog(logMessage);
    return response;
}

export function intResponse(body: number, logMessage: string) {
    const response = new Response.Int();
    response.setBody(body);
    response.setLog(logMessage);
    return response;
}

export function boolResponse(value: boolean, logMessage: string) {
    const response = new Response.Bool();
    response.setBody(value);
    response.setLog(logMessage);
    return response;
}

export function jsResponse(result: string, logMessage: string) {
    const response = new Response.JavascriptExecutionResult();
    response.setResult(JSON.stringify(result));
    response.setLog(logMessage);
    return response;
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
) {
    const response = new Response.Keywords();
    response.setKeywordsList(keywords);
    response.setKeyworddocumentationsList(keywordDocs);
    response.setKeywordargumentsList(keywordArguments);
    response.setLog(logMessage);
    return response;
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
    } catch (e) { // eslint-disable-line
        return str;
    }
}
