import { BrowserContext, Cookie } from 'playwright';

import { Request, Response } from './generated/playwright_pb';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';
import { exists, findLocator } from './playwright-invoke';

import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function startCoverage(request: Request.StartCoverage, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    await activePage?.coverage.startJSCoverage();
    return emptyWithLog("Coverage started.");
}

export async function stopCoverage(request: Request.Empty, state: PlaywrightState): Promise<Response.Json> {
    const activePage = state.getActivePage();
    const coverage = await activePage?.coverage.stopJSCoverage();
    exists(coverage, "Coverage report is empry");
    for (const entry of coverage) {
        logger.info(`Entry ${JSON.stringify(entry)}`);
        logger.info(`=======================`)

    }
    return jsonResponse(JSON.parse('{"key": "value"}'), "Coverage stopped.");
}
