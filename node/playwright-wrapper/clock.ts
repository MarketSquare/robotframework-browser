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
    const setTime = new Date(time).toISOString();
    if (clockType === 'fixed') {
        logger.info(`Setting time to ${time} ${setTime} as fixed`);
        activePage.clock.setFixedTime(time);
    } else if (clockType === 'system') {
        logger.info(`Setting time to ${time} ${setTime} as system`);
        activePage.clock.setSystemTime(time);
    } else if (clockType === 'install') {
        logger.info(`Setting time to ${time} ${setTime} as install`);
        activePage.clock.install({ time: time });
    } else {
        logger.info(`Invalid clock type ${clockType}`);
        return emptyWithLog('Invalid clock type');
    }
    return emptyWithLog(`Time set to ${setTime} as ${clockType}`);
}

export async function clockResume(request: Request.Empty, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    activePage.clock.resume();
    return emptyWithLog('Clock resumed');
}

export async function clockPauseAt(request: Request.ClockSetTime, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    let time = request.getTime();
    time = time * 1000;
    const setTime = new Date(time).toISOString();
    logger.info(`Pausing clock at ${time} ${setTime}`);
    await activePage.clock.pauseAt(time);
    return emptyWithLog(`Clock paused at ${setTime}`);
}

export async function advanceClock(request: Request.ClockAdvance, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const time = request.getTime();
    const timeMs = time * 1000;
    const advanceType = request.getAdvancetype();
    logger.info(`Advancing clock by ${timeMs} ${advanceType}`);
    if (advanceType === 'fast_forward') {
        await activePage.clock.fastForward(timeMs);
    } else if (advanceType === 'run_for') {
        await activePage.clock.runFor(timeMs);
    }
    return emptyWithLog(`Clock advanced by ${timeMs} seconds by ${advanceType}`);
}
