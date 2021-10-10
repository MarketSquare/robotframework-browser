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
import { emptyWithLog, stringResponse } from './response-util';
import { exists, findLocator } from './playwirght-invoke';

export async function goTo(request: Request.Url, page: Page): Promise<Response.Empty> {
    const url = request.getUrl();
    const timeout = request.getDefaulttimeout();
    await page.goto(url, { timeout });
    return emptyWithLog(`Successfully opened URL ${url}`);
}

export async function takeScreenshot(
    request: Request.ScreenshotOptions,
    state: PlaywrightState,
): Promise<Response.String> {
    const fileType = request.getFiletype();
    const path = request.getPath() + '.' + fileType;
    const fullPage = request.getFullpage();
    const selector = request.getSelector();
    const quality = request.getQuality();
    const timeout = request.getTimeout();
    const options: Record<string, any> = { path: path, type: fileType, timeout: timeout };
    const strictMode = request.getStrict();
    if (quality) {
        options.quality = parseInt(quality);
    }
    if (selector) {
        const locator = await findLocator(state, selector, strictMode, undefined, true);
        await locator.screenshot(options);
    } else {
        const page = state.getActivePage();
        exists(page, 'Tried to take screenshot, but no page was open.');
        options.fullPage = fullPage;
        await page.screenshot(options);
    }
    const message = 'Screenshot succesfully captured to: ' + path;
    return stringResponse(path, message);
}

export async function setTimeout(request: Request.Timeout, context?: BrowserContext): Promise<Response.Empty> {
    if (!context) {
        return emptyWithLog(`No context open.`);
    }
    const timeout = request.getTimeout();
    context.setDefaultTimeout(timeout);
    return emptyWithLog(`Set timeout to: ${timeout}`);
}

export async function setViewportSize(request: Request.Viewport, page: Page): Promise<Response.Empty> {
    const size = { width: request.getWidth(), height: request.getHeight() };
    await page.setViewportSize(size);
    return emptyWithLog(`Set viewport size to: ${size}`);
}

export async function setOffline(request: Request.Bool, context?: BrowserContext): Promise<Response.Empty> {
    exists(context, 'Tried to toggle context to offline, no open context');
    const offline = request.getValue();
    await context.setOffline(offline);
    return emptyWithLog(`Set context to ${offline}`);
}

export async function reload(page: Page): Promise<Response.Empty> {
    await page.reload();
    return emptyWithLog('Reloaded page');
}

export async function setGeolocation(request: Request.Json, context?: BrowserContext): Promise<Response.Empty> {
    const geolocation = JSON.parse(request.getBody());
    await context?.setGeolocation(geolocation);
    return emptyWithLog('Geolocation set to: ' + JSON.stringify(geolocation));
}
