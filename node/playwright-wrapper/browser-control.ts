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
import { exists, findLocator } from './playwright-invoke';
import { logger } from './browser_logger';

const { program: pwProgram } = require('playwright-core/lib/cli/program') as { program: import('commander').Command }; // eslint-disable-line

export async function executePlaywright(request: Request.Json): Promise<Response.Empty> {
    const args = JSON.parse(request.getBody());
    pwProgram.exitOverride();
    await pwProgram.parseAsync(args, { from: 'user' });
    return emptyWithLog('Installed browsers');
}

export async function grantPermissions(request: Request.Permissions, state: PlaywrightState): Promise<Response.Empty> {
    const browserContext = state.getActiveContext();
    if (!browserContext) {
        return emptyWithLog(`No browser context is active. Use 'Open Browser' to open a new one.`);
    }
    await browserContext.grantPermissions(request.getPermissionsList(), {
        ...(request.getOrigin().length > 0 && { origin: request.getOrigin() }),
    });
    return emptyWithLog(
        `Granted permissions "${request.getPermissionsList().join(', ')}"` +
            (request.getOrigin().length > 0 ? ` for origin "${request.getOrigin()}"` : ''),
    );
}

export async function clearPermissions(request: Request.Empty, state: PlaywrightState): Promise<Response.Empty> {
    const browserContext = state.getActiveContext();
    if (!browserContext) {
        return emptyWithLog(`No browser context is active. Use 'Open Browser' to open a new one.`);
    }
    await browserContext.clearPermissions();
    return emptyWithLog('Cleared all permissions');
}

export async function goTo(request: Request.UrlOptions, page: Page): Promise<Response.Empty> {
    const url = request.getUrl()?.getUrl() || 'about:blank';
    const timeout = request.getUrl()?.getDefaulttimeout();
    const goToOptions: {
        timeout?: number;
        waitUntil?: 'load' | 'domcontentloaded' | 'networkidle' | 'commit';
    } = { timeout: timeout };
    const waitUntil = <'load' | 'domcontentloaded' | 'networkidle' | 'commit'>request.getWaituntil();
    if (waitUntil) {
        goToOptions.waitUntil = waitUntil;
    }
    const response = await page.goto(url, goToOptions);
    return stringResponse(response?.status().toString() || '', `Successfully opened URL ${url}`);
}

export async function takeScreenshot(
    request: Request.ScreenshotOptions,
    state: PlaywrightState,
): Promise<Response.String> {
    const selector = request.getSelector();
    const options = JSON.parse(request.getOptions());
    const mask = JSON.parse(request.getMask());
    const strictMode = request.getStrict();
    const page = state.getActivePage();
    exists(page, 'Tried to take screenshot, but no page was open.');
    if (mask) {
        const mask_locators = [];
        for (const sel of mask) {
            mask_locators.push(await findLocator(state, sel, false, undefined, false));
        }
        options.mask = mask_locators;
    }
    logger.info({ 'Take screenshot with options: ': options });
    if (selector) {
        logger.info({ 'Using selecotr: ': selector });
        const locator = await findLocator(state, selector, strictMode, undefined, true);
        await locator.screenshot(options);
    } else {
        await page.screenshot(options);
    }
    const message = 'Screenshot successfully captured to: ' + options.path;
    return stringResponse(options.path, message);
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

export async function reload(page: Page, body: string): Promise<Response.Empty> {
    const options = JSON.parse(body);
    logger.info(`Reload page with options: ${body}`);
    await page.reload(options);
    return emptyWithLog(`Reloaded page with options: ${body}`);
}

export async function setGeolocation(request: Request.Json, context?: BrowserContext): Promise<Response.Empty> {
    const geolocation = JSON.parse(request.getBody());
    await context?.setGeolocation(geolocation);
    return emptyWithLog('Geolocation set to: ' + JSON.stringify(geolocation));
}
