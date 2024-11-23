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

import { CoverageReport } from 'monocart-coverage-reports';
import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, stringResponse } from './response-util';
import { exists } from './playwright-invoke';
import { join, normalize } from 'path';
import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function startCoverage(request: Request.CoverateStart, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const coverageType = request.getCoveratetype();
    const coverageDir = request.getCoveragedir();
    const folderPrefix = request.getFolderprefix();
    const configFile = request.getConfigfile();
    const raw = request.getRaw();
    const coverageOptions = {
        type: coverageType,
        directory: coverageDir,
        folderPrefix: folderPrefix,
        configFile: configFile,
        raw: raw,
    };
    state.addCoverageOptions(coverageOptions);
    const resetOnNavigation = request.getResetonnavigation();
    const reportAnonymousScripts = request.getReportanonymousscripts();
    if (coverageType === 'js' || coverageType === 'all') {
        logger.info(
            `Starting JS coverage with resetOnNavigation: ${resetOnNavigation} and reportAnonymousScripts: ${reportAnonymousScripts}`,
        );
        await activePage.coverage.startJSCoverage({ resetOnNavigation, reportAnonymousScripts });
    }
    if (coverageType === 'css' || coverageType === 'all') {
        logger.info(`Starting CSS coverage with resetOnNavigation: ${resetOnNavigation}`);
        await activePage.coverage.startCSSCoverage({ resetOnNavigation });
    }
    return emptyWithLog(`Coverage started for ${coverageType}`);
}

export async function stopCoverage(request: Request.Empty, state: PlaywrightState): Promise<Response.String> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const coverageOptions = state.getCoverageOptions();
    if (coverageOptions === null) {
        return stringResponse('', 'Coverage not started');
    }
    const coverageDir = coverageOptions?.directory ?? '';
    const folderPrefix = coverageOptions?.folderPrefix ?? '';
    const configFile = coverageOptions?.configFile ?? '';
    const coverageType = coverageOptions?.type;
    const raw = coverageOptions?.raw ?? false;
    let allCoverage: any[] = [];
    if (coverageType === 'js' || coverageType === 'all') {
        logger.info('Stopping JS coverage');
        const jsCoverage = await activePage.coverage.stopJSCoverage();
        allCoverage = [...jsCoverage];
    }
    if (coverageType === 'css' || coverageType === 'all') {
        logger.info('Stopping CSS coverage');
        const cssCoverage = await activePage.coverage.stopCSSCoverage();
        allCoverage = [...allCoverage, ...cssCoverage];
    }
    const pageId = state.getActivePageId();
    let outputDir = join(coverageDir, folderPrefix + pageId);
    outputDir = normalize(outputDir);
    let options = {};
    if (raw && configFile === '') {
        logger.info('Raw and v8 coverage enabled');
        options = {
            outputDir: outputDir,
            reports: [['raw'], ['v8']],
        };
    } else {
        logger.info('v8 coverage disabled');
        options = {
            outputDir: outputDir,
        };
    }
    const mcr = new CoverageReport(options);
    if (configFile !== '') {
        logger.info({ 'Config file: ': configFile });
        await mcr.loadConfig(configFile);
    }
    await mcr.add(allCoverage);
    await mcr.generate();
    return stringResponse(outputDir, 'Coverage stopped and report generated');
}
