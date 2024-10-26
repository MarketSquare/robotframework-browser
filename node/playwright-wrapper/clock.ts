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

import pino from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function setTime(request: Request.ClockSetTime, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    let time = request.getTime();
    time = time * 1000;
    const clockType = request.getSettype();
    if (clockType === 'fixed') {
        logger.info(`Setting time to ${time} as fixed`);
        activePage.clock.setFixedTime(time);
    } else if (clockType === 'system') {
        logger.info(`Setting time to ${time} as system`);
        activePage.clock.setSystemTime(time);
    } else {
        return emptyWithLog('Invalid clock type');
    }
    return emptyWithLog(`Time set to ${time} as ${clockType}`);
}
