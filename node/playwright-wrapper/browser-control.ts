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

import { BrowserContext, Page } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { determineElement, exists, invokeOnPage } from './playwirght-invoke';
import { emptyWithLog, stringResponse } from './response-util';

export async function goTo(
    call: ServerUnaryCall<Request.Url>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
): Promise<void> {
    const url = call.request.getUrl();
    const timeout = call.request.getDefaulttimeout();
    await invokeOnPage(page, 'goto', url, { timeout: timeout });
    callback(null, emptyWithLog(`Succesfully opened URL ${url}`));
}

export async function goBack(callback: sendUnaryData<Response.Empty>, page?: Page): Promise<void> {
    await invokeOnPage(page, 'goBack');
    callback(null, emptyWithLog('Did Go Back'));
}

export async function goForward(callback: sendUnaryData<Response.Empty>, page?: Page): Promise<void> {
    await invokeOnPage(page, 'goForward');
    callback(null, emptyWithLog('Did Go Forward'));
}

export async function takeScreenshot(
    call: ServerUnaryCall<Request.ScreenshotOptions>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
) {
    // Add the file extension here because the image type is defined by playwrights defaults
    const path = call.request.getPath() + '.png';
    const fullPage = call.request.getFullpage();
    const selector = call.request.getSelector();
    if (selector) {
        const elem = await determineElement(state, selector, callback);
        exists(elem, `Tried to capture element screenshot, element '${selector}' wasn't found.`);
        await elem.screenshot({ path: path });
    } else {
        const page = state.getActivePage();
        exists(page, 'Tried to take screenshot, but no page was open.');
        await invokeOnPage(page, 'screenshot', { path: path, fullPage });
    }
    const message = 'Screenshot succesfully captured to: ' + path;
    callback(null, stringResponse(path, message));
}

export function setTimeout(
    call: ServerUnaryCall<Request.Timeout>,
    callback: sendUnaryData<Response.Empty>,
    context?: BrowserContext,
) {
    exists(context, 'Tried to set timeout, no open context');
    const timeout = call.request.getTimeout();
    context.setDefaultTimeout(timeout);
    callback(null, emptyWithLog(`Set timeout to: ${timeout}`));
}

export async function setViewportSize(
    call: ServerUnaryCall<Request.Viewport>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const size = { width: call.request.getWidth(), height: call.request.getHeight() };
    await invokeOnPage(page, 'setViewportSize', size);
    callback(null, emptyWithLog(`Set viewport size to: ${size}`));
}

export async function setOffline(
    call: ServerUnaryCall<Request.Bool>,
    callback: sendUnaryData<Response.Empty>,
    context?: BrowserContext,
) {
    exists(context, 'Tried to toggle context to offline, no open context');
    const offline = call.request.getValue();
    await context.setOffline(offline);
    callback(null, emptyWithLog(`Set context to ${offline}`));
}

export async function reload(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    await invokeOnPage(page, 'reload');
    callback(null, emptyWithLog('Reloaded page'));
}

export async function setGeolocation(
    call: ServerUnaryCall<Request.Json>,
    callback: sendUnaryData<Response.Empty>,
    context?: BrowserContext,
) {
    try {
        const geolocation = JSON.parse(call.request.getBody());
        await context?.setGeolocation(geolocation);
        callback(null, emptyWithLog('Geolocation set to: ' + JSON.stringify(geolocation)));
    } catch (error) {
        callback(error, null);
    }
}
