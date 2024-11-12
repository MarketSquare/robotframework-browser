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
    state.addCoverageType(coverageType);
    if (coverageType === 'js' || coverageType === 'all') {
        logger.info('Starting JS coverage');
        await activePage.coverage.startJSCoverage();
    }
    if (coverageType === 'css' || coverageType === 'all') {
        logger.info('Starting CSS coverage');
        await activePage.coverage.startCSSCoverage();
    }
    return emptyWithLog(`Coverage started for ${coverageType}`);
}

export async function stopCoverage(request: Request.CoverageStop, state: PlaywrightState): Promise<Response.String> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const coverageType = state.getCoverageType();
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
    const coverageDir = request.getCoveragedir();
    const folderPrefix = request.getFolderprefix();
    let outputDir = join(coverageDir, folderPrefix + pageId);
    outputDir = normalize(outputDir);
    const mcr = new CoverageReport({ outputDir: outputDir });
    const configFile = request.getConfigfile();
    if (configFile !== '') {
        logger.info({ 'Config file: ': configFile });
        await mcr.loadConfig(configFile);
    }
    await mcr.add(allCoverage);
    await mcr.generate();
    return stringResponse(outputDir, 'Coverage stopped and report generated');
}
