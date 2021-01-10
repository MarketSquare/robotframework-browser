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

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { determineElement, exists, invokeOnPage } from './playwirght-invoke';
import { emptyWithLog, stringResponse } from './response-util';

export async function goTo(request: Request.Url, page: Page): Promise<Response.Empty> {
    const url = request.getUrl();
    const timeout = request.getDefaulttimeout();
    await page.goto(url, { timeout });
    return emptyWithLog(`Succesfully opened URL ${url}`);
}

export async function takeScreenshot(
    request: Request.ScreenshotOptions,
    state: PlaywrightState,
): Promise<Response.String> {
    // Add the file extension here because the image type is defined by playwrights defaults
    const path = request.getPath() + '.png';
    const fullPage = request.getFullpage();
    const selector = request.getSelector();
    if (selector) {
        const elem = await determineElement(state, selector);
        exists(elem, `Tried to capture element screenshot, element '${selector}' wasn't found.`);
        await elem.screenshot({ path: path });
    } else {
        const page = state.getActivePage();
        exists(page, 'Tried to take screenshot, but no page was open.');
        await invokeOnPage(page, 'screenshot', { path: path, fullPage });
    }
    const message = 'Screenshot succesfully captured to: ' + path;
    return stringResponse(path, message);
}

export async function setTimeout(request: Request.Timeout, context?: BrowserContext): Promise<Response.Empty> {
    exists(context, 'Tried to set timeout, no open context');
    const timeout = request.getTimeout();
    context.setDefaultTimeout(timeout);
    return emptyWithLog(`Set timeout to: ${timeout}`);
}

export async function setViewportSize(request: Request.Viewport, page?: Page): Promise<Response.Empty> {
    const size = { width: request.getWidth(), height: request.getHeight() };
    await invokeOnPage(page, 'setViewportSize', size);
    return emptyWithLog(`Set viewport size to: ${size}`);
}

export async function setOffline(request: Request.Bool, context?: BrowserContext): Promise<Response.Empty> {
    exists(context, 'Tried to toggle context to offline, no open context');
    const offline = request.getValue();
    await context.setOffline(offline);
    return emptyWithLog(`Set context to ${offline}`);
}

export async function reload(page?: Page): Promise<Response.Empty> {
    await invokeOnPage(page, 'reload');
    return emptyWithLog('Reloaded page');
}

export async function setGeolocation(request: Request.Json, context?: BrowserContext): Promise<Response.Empty> {
    const geolocation = JSON.parse(request.getBody());
    await context?.setGeolocation(geolocation);
    return emptyWithLog('Geolocation set to: ' + JSON.stringify(geolocation));
}
