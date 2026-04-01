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

import { logger } from './browser_logger';
import * as pb from './generated/playwright';
import { exists } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog } from './response-util';

export async function setTime(request: pb.Request_ClockSetTime, state: PlaywrightState): Promise<pb.Response_Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    let time = request.time;
    time = time * 1000;
    const clockType = request.setType;
    const setTime = new Date(time).toISOString();
    if (clockType === 'fixed') {
        logger.info(`Setting time to ${time} ${setTime} as fixed`);
        await activePage.clock.setFixedTime(time);
    } else if (clockType === 'system') {
        logger.info(`Setting time to ${time} ${setTime} as system`);
        await activePage.clock.setSystemTime(time);
    } else if (clockType === 'install') {
        logger.info(`Setting time to ${time} ${setTime} as install`);
        await activePage.clock.install({ time: time });
    } else {
        logger.info(`Invalid clock type ${clockType}`);
        return emptyWithLog('Invalid clock type');
    }
    return emptyWithLog(`Time set to ${setTime} as ${clockType}`);
}

export async function clockResume(request: pb.Request_Empty, state: PlaywrightState): Promise<pb.Response_Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    await activePage.clock.resume();
    return emptyWithLog('Clock resumed');
}

export async function clockPauseAt(
    request: pb.Request_ClockSetTime,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    let time = request.time;
    time = time * 1000;
    const setTime = new Date(time).toISOString();
    logger.info(`Pausing clock at ${time} ${setTime}`);
    await activePage.clock.pauseAt(time);
    return emptyWithLog(`Clock paused at ${setTime}`);
}

export async function advanceClock(
    request: pb.Request_ClockAdvance,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const time = request.time;
    const timeMs = time * 1000;
    const advanceType = request.advanceType;
    logger.info(`Advancing clock by ${timeMs} ${advanceType}`);
    if (advanceType === 'fast_forward') {
        await activePage.clock.fastForward(timeMs);
    } else if (advanceType === 'run_for') {
        await activePage.clock.runFor(timeMs);
    }
    return emptyWithLog(`Clock advanced by ${timeMs} seconds by ${advanceType}`);
}
