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
import { exists } from './playwright-invoke';
import { stringResponse } from './response-util';

import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

export async function savePageAsPdf(request: Request.Pdf, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const pdfPath = request.getPath();
    const displayheaderfooter = request.getDisplayheaderfooter();
    const footertemplate = request.getFootertemplate();
    const format = request.getFormat();
    const headerTemplate = request.getHeadertemplate();
    const height = request.getHeight();
    const landscape = request.getLandscape();
    const marginString = request.getMargin();
    const marging = JSON.parse(marginString);
    const outline = request.getOutline();
    const pageRanges = request.getPageranges();
    const preferCSSPageSize = request.getPrefercsspagesize();
    const printBackground = request.getPrintbackground();
    const scale = request.getScale();
    const tagged = request.getTagged();
    const width = request.getWidth();
    logger.info(`Saving pdf to ${pdfPath}`);
    const message =
        `Using options: displayHeaderFooter: ${displayheaderfooter}, ` +
        `footerTemplate: ${footertemplate}, ` +
        `format: ${format}, ` +
        `headerTemplate: ${headerTemplate}, ` +
        `height: ${height}, ` +
        `landscape: ${landscape}, ` +
        `margin (as string): ${marginString}, ` +
        `outline: ${outline}, ` +
        `pageRanges: ${pageRanges}, ` +
        `preferCSSPageSize: ${preferCSSPageSize}, ` +
        `printBackground: ${printBackground}, ` +
        `scale: ${scale}, ` +
        `tagged: ${tagged}  and ` +
        `width: ${width}`;
    logger.info(message);
    await activePage.pdf({
        path: pdfPath,
        displayHeaderFooter: displayheaderfooter,
        footerTemplate: footertemplate,
        format: format,
        headerTemplate: headerTemplate,
        height: height,
        landscape: landscape,
        margin: marging,
        outline: outline,
        pageRanges: pageRanges,
        preferCSSPageSize: preferCSSPageSize,
        printBackground: printBackground,
        scale: scale,
        tagged: tagged,
        width: width,
    });
    return stringResponse(pdfPath, `Pdf is saved to ${pdfPath}`);
}

export async function emulateMedia(request: Request.EmulateMedia, state: PlaywrightState): Promise<Response.Empty> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const options: { [key: string]: string | null } = {};
    const colorScheme = request.getColorscheme();
    if (colorScheme === 'not_set') {
        logger.info(`Emulating colorScheme not set`);
    } else if (colorScheme === 'null') {
        logger.info(`Emulating colorScheme null`);
        options.colorScheme = null;
    } else {
        logger.info(`Emulating colorScheme ${colorScheme}`);
        options.colorScheme = colorScheme;
    }
    const forcedColors = request.getForcedcolors();
    if (forcedColors === 'not_set') {
        logger.info(`Emulating forcedColors not set`);
    } else if (forcedColors === 'null') {
        logger.info(`Emulating forcedColors null`);
        options.forcedColors = null;
    } else {
        logger.info(`Emulating forcedColors ${forcedColors}`);
        options.forcedColors = forcedColors;
    }
    const media = request.getMedia();
    if (media === 'not_set') {
        logger.info(`Emulating media not set`);
    } else if (media === 'null') {
        logger.info(`Emulating media null`);
        options.media = null;
    } else {
        logger.info(`Emulating media ${media}`);
        options.media = media;
    }
    const reducedMotion = request.getReducedmotion();
    if (reducedMotion === 'not_set') {
        logger.info(`Emulating reducedMotion not set`);
    } else if (reducedMotion === 'null') {
        logger.info(`Emulating reducedMotion null`);
        options.reducedMotion = null;
    } else {
        logger.info(`Emulating reducedMotion ${reducedMotion}`);
        options.reducedMotion = reducedMotion;
    }
    await activePage.emulateMedia(options);
    return stringResponse(JSON.stringify(options), `Emulating media ${JSON.stringify(options)}`);
}
