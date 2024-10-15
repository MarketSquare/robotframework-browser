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
import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog } from './response-util';
import { exists } from './playwright-invoke';
import { findLocator } from './playwright-invoke';

import pino from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function addLocatorHandler(
    request: Request.LocatorHandlerAdd,
    state: PlaywrightState,
): Promise<Response.Empty> {
    logger.info(`Adding locator handler for ${request.getSelector()}`);
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const selector = request.getSelector();
    const clickSelector = request.getClickselector();
    await activePage.addLocatorHandler(activePage.locator(selector), async () => {
        logger.info(`Clicking element ${clickSelector} when locator ${selector} is found`);
        try {
            const clickLocator = await findLocator(state, clickSelector, false, undefined, true);
            await clickLocator.click();
        } catch (error) {
            logger.error(`Error clicking element ${clickSelector} when locator ${selector} is found: ${error}`);
            return emptyWithLog(`Got error: ${error}`);
        }

    });
    return emptyWithLog(`Deselected options in element ${request.getSelector()}`);
}

export async function removeLocatorHandler(
    request: Request.LocatorHandlerRemove,
    state: PlaywrightState,
): Promise<Response.Empty> {
    logger.info(`Removing locator handler for ${request.getSelector()}`);
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const locator = await findLocator(state, request.getSelector(), false, undefined, true);
    await activePage.removeLocatorHandler(locator);
    return emptyWithLog(`Removed locator handler ${request.getSelector()}`);
}
