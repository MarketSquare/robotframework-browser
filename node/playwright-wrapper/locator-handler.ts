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
import { errorType, logger } from './browser_logger';
import * as pb from './generated/playwright';
import { exists } from './playwright-invoke';
import { findLocator } from './playwright-invoke';
import { locatorCache, PlaywrightState } from './playwright-state';
import { emptyWithLog } from './response-util';

export async function addLocatorHandlerCustom(
    request: pb.Request_LocatorHandlerAddCustom,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const overlaySelector = request.selector;
    const timesString = request.times;
    let times;
    if (timesString === 'None') {
        times = undefined;
    } else {
        times = parseInt(timesString);
    }
    logger.info(`Adding locator handler for ${overlaySelector} as times: ${times}`);
    const noWaitAfter = request.noWaitAfter;
    const handlerSpecs = request.handlerSpecs;
    const overlayLocator = await findLocator(state, overlaySelector, false, undefined, true);
    locatorCache.add(`${state.getActivePageId()}-${overlaySelector}`, overlayLocator);
    await activePage.addLocatorHandler(
        overlayLocator,
        async () => {
            logger.info(`Overlay locator ${overlaySelector} is found`);
            for (const handlerSpec of handlerSpecs) {
                const action = handlerSpec.action;
                const actionSelector = handlerSpec.selector;
                const actionLocator = await findLocator(state, actionSelector, false, undefined, true);
                const options = JSON.parse(handlerSpec.optionsAsJson);
                try {
                    if (action === 'click') {
                        logger.info(
                            `Overlay click on element ${actionSelector} with options: ${JSON.stringify(options)}`,
                        );
                        await actionLocator.click({ ...options });
                    } else if (action === 'fill') {
                        const value = handlerSpec.value;
                        logger.info(
                            `Overlay fill on element ${actionSelector} with value ${value} with options: ${JSON.stringify(options)}`,
                        );
                        await actionLocator.fill(value, { ...options });
                    } else if (action === 'check') {
                        logger.info(
                            `Overlay check on element ${actionSelector} with options: ${JSON.stringify(options)}`,
                        );
                        await actionLocator.check({ ...options });
                    } else if (action === 'uncheck') {
                        logger.info(
                            `Overlay uncheck on element ${actionSelector} with options: ${JSON.stringify(options)}`,
                        );
                        await actionLocator.uncheck({ ...options });
                    }
                } catch (error) {
                    logger.error(
                        { event_kind: 'internal_error', status: 'failed', error_type: errorType(error) },
                        `Error in custom locator handler: ${String(error)}`,
                    );
                }
            }
        },
        { times: times, noWaitAfter: noWaitAfter },
    );
    return emptyWithLog(`Custom locator handler added for element ${overlaySelector}`);
}

export async function removeLocatorHandler(
    request: pb.Request_LocatorHandlerRemove,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    logger.info(`Removing locator handler for ${request.selector}`);
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const activePageId = state.getActivePageId();
    const overlaySelector = request.selector;
    const locator = locatorCache.get(`${activePageId}-${overlaySelector}`);
    locatorCache.delete(`${activePageId}-${overlaySelector}`);
    if (locator === undefined) {
        return emptyWithLog(`No locator handler found for ${overlaySelector}`);
    }
    await activePage.removeLocatorHandler(locator);
    return emptyWithLog(`Removed locator handler ${overlaySelector}`);
}
