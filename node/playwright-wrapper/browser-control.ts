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

import { logger } from './browser_logger';
import * as pb from './generated/playwright';
import { exists, findLocator } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, stringResponse } from './response-util';

const { program: pwProgram } = require('playwright-core/lib/cli/program') as { program: import('commander').Command }; // eslint-disable-line

export async function executePlaywright(request: pb.Request_Json): Promise<pb.Response_Empty> {
    const args = JSON.parse(request.body);
    pwProgram.exitOverride();
    await pwProgram.parseAsync(args, { from: 'user' });
    return emptyWithLog('Executed Playwright command: ' + args.join(' '));
}

export async function grantPermissions(
    request: pb.Request_Permissions,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const browserContext = state.getActiveContext();
    if (!browserContext) {
        return emptyWithLog(`No browser context is active. Use 'Open Browser' to open a new one.`);
    }
    await browserContext.grantPermissions(request.permissions, {
        ...(request.origin.length > 0 && { origin: request.origin }),
    });
    return emptyWithLog(
        `Granted permissions "${request.permissions.join(', ')}"` +
            (request.origin.length > 0 ? ` for origin "${request.origin}"` : ''),
    );
}

export async function clearPermissions(request: pb.Request_Empty, state: PlaywrightState): Promise<pb.Response_Empty> {
    const browserContext = state.getActiveContext();
    if (!browserContext) {
        return emptyWithLog(`No browser context is active. Use 'Open Browser' to open a new one.`);
    }
    await browserContext.clearPermissions();
    return emptyWithLog('Cleared all permissions');
}

export async function goTo(request: pb.Request_UrlOptions, page: Page): Promise<pb.Response_String> {
    const url = request.url?.url || 'about:blank';
    const timeout = request.url?.defaultTimeout;
    const goToOptions: {
        timeout?: number;
        waitUntil?: 'load' | 'domcontentloaded' | 'networkidle' | 'commit';
    } = { timeout: timeout };
    const waitUntil = <'load' | 'domcontentloaded' | 'networkidle' | 'commit'>request.waitUntil;
    if (waitUntil) {
        goToOptions.waitUntil = waitUntil;
    }
    const response = await page.goto(url, goToOptions);
    return stringResponse(response?.status().toString() || '', `Successfully opened URL ${url}`);
}

export async function takeScreenshot(
    request: pb.Request_ScreenshotOptions,
    state: PlaywrightState,
): Promise<pb.Response_String> {
    const selector = request.selector;
    const options = JSON.parse(request.options);
    const mask = JSON.parse(request.mask);
    const strictMode = request.strict;
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

export async function setTimeout(request: pb.Request_Timeout, context?: BrowserContext): Promise<pb.Response_Empty> {
    if (!context) {
        return emptyWithLog(`No context open.`);
    }
    const timeout = request.timeout;
    context.setDefaultTimeout(timeout);
    return emptyWithLog(`Set timeout to: ${timeout}`);
}

export async function setViewportSize(request: pb.Request_Viewport, page: Page): Promise<pb.Response_Empty> {
    const size = { width: request.width, height: request.height };
    await page.setViewportSize(size);
    return emptyWithLog(`Set viewport size to: ${JSON.stringify(size)}`);
}

export async function setOffline(request: pb.Request_Bool, context?: BrowserContext): Promise<pb.Response_Empty> {
    exists(context, 'Tried to toggle context to offline, no open context');
    const offline = request.value;
    await context.setOffline(offline);
    return emptyWithLog(`Set context to ${offline}`);
}

export async function reload(page: Page, body: string): Promise<pb.Response_Empty> {
    const options = JSON.parse(body);
    logger.info(`Reload page with options: ${body}`);
    await page.reload(options);
    return emptyWithLog(`Reloaded page with options: ${body}`);
}

export async function setGeolocation(request: pb.Request_Json, context?: BrowserContext): Promise<pb.Response_Empty> {
    const geolocation = JSON.parse(request.body);
    await context?.setGeolocation(geolocation);
    return emptyWithLog('Geolocation set to: ' + JSON.stringify(geolocation));
}
