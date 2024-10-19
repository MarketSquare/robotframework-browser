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
import { PlaywrightState, locatorCache } from './playwright-state';
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
    const activePageId = state.getActivePageId();
    const overlaySelector = request.getSelector();
    const clickSelector = request.getClickselector();
    const overlayLocator = await findLocator(state, overlaySelector, false, undefined, true);
    locatorCache.add(`${activePageId}-${overlaySelector}`, overlayLocator);
    const noWaitAfter = request.getNowaitafter();
    const timesString = request.getTimes();
    let times;
    if (timesString === 'None') {
        times = undefined;
    } else {
        times = parseInt(timesString);
    }
    const clickClickCount = request.getClickclickcount();
    const clickDelay = request.getClickdelay();
    const clickForce = request.getClickforce();
    await activePage.addLocatorHandler(
        overlayLocator,
        async () => {
            logger.info(`Clicking element ${clickSelector} when locator ${overlaySelector} is found`);
            logger.info(`Click options: clickCount=${clickClickCount}, delay=${clickDelay}, force=${clickForce}`);
            try {
                const clickLocator = await findLocator(state, clickSelector, false, undefined, true);
                await clickLocator.click({ clickCount: clickClickCount, delay: clickDelay, force: clickForce });
            } catch (error) {
                logger.error(
                    `Error clicking element ${clickSelector} when locator ${overlaySelector} is found: ${error}`,
                );
                return emptyWithLog(`Got error: ${error}`);
            }
        },
        { times: times, noWaitAfter: noWaitAfter },
    );
    return emptyWithLog(`Deselected options in element ${request.getSelector()}`);
}

export async function removeLocatorHandler(
    request: Request.LocatorHandlerRemove,
    state: PlaywrightState,
): Promise<Response.Empty> {
    logger.info(`Removing locator handler for ${request.getSelector()}`);
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const activePageId = state.getActivePageId();
    const overlaySelector = request.getSelector();
    const locator = locatorCache.get(`${activePageId}-${overlaySelector}`);
    locatorCache.delete(`${activePageId}-${overlaySelector}`);
    if (locator === undefined) {
        return emptyWithLog(`No locator handler found for ${overlaySelector}`);
    }
    await activePage.removeLocatorHandler(locator);
    return emptyWithLog(`Removed locator handler ${overlaySelector}`);
}
