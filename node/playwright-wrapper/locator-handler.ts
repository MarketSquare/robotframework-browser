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

export async function addLocatorHandlerClick(
    request: Request.LocatorHandlerAddClick,
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
    return emptyWithLog(`Added click locator handler for element ${request.getSelector()}`);
}

export async function addLocatorHandlerCustom(
    request: Request.LocatorHandlerAddCustom,
    state: PlaywrightState,
): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const overlaySelector = request.getSelector();
    const timesString = request.getTimes();
    let times;
    if (timesString === 'None') {
        times = undefined;
    } else {
        times = parseInt(timesString);
    }
    logger.info(`Adding locator handler for ${overlaySelector} as times: ${times}`);
    const noWaitAfter = request.getNowaitafter();
    const hadlerSpecs = request.getHandlerspecsList();
    const overlayLocator = await findLocator(state, overlaySelector, false, undefined, true);
    locatorCache.add(`${state.getActivePageId()}-${overlaySelector}`, overlayLocator);
    const allActions: string[] = [];
    await activePage.addLocatorHandler(
        overlayLocator,
        async () => {
            logger.info(`Overlay locator ${overlaySelector} is found`);
            for (const handlerSpec of hadlerSpecs) {
                const action = handlerSpec.getAction();
                const actionSelector = handlerSpec.getSelector();
                const actionLocator = await findLocator(state, actionSelector, false, undefined, true);
                const options = JSON.parse(handlerSpec.getOptionsasjson());
                allActions.push(action);
                if (action === 'click') {
                    logger.info(`Overlay click on element ${actionSelector} with options: ${JSON.stringify(options)}`);
                    await actionLocator.click({ ...options });
                }
            }
        },
        { times: times, noWaitAfter: noWaitAfter },
    );
    return emptyWithLog(`Custom locator handler added for element ${overlaySelector}`);
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
