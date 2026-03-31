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
import { stringResponse } from './response-util';

export async function savePageAsPdf(request: pb.Request_Pdf, state: PlaywrightState): Promise<pb.Response_String> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const req: pb.Request_Pdf = request;
    const pdfPath = req.path;
    const displayheaderfooter = req.displayHeaderFooter;
    const footertemplate = req.footerTemplate;
    const format = req.format;
    const headerTemplate = req.headerTemplate;
    const height = req.height;
    const landscape = req.landscape;
    const marginString = req.margin;
    const marging = JSON.parse(marginString);
    const outline = req.outline;
    const pageRanges = req.pageRanges;
    const preferCSSPageSize = req.preferCSSPageSize;
    const printBackground = req.printBackground;
    const scale = req.scale;
    const tagged = req.tagged;
    const width = req.width;
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
    return stringResponse(pdfPath, `Pdf is saved to ${pdfPath}`) as unknown as pb.Response_String;
}

export async function emulateMedia(
    request: pb.Request_EmulateMedia,
    state: PlaywrightState,
): Promise<pb.Response_String> {
    const activePage = state.getActivePage();
    exists(activePage, 'Could not find active page');
    const options: { [key: string]: string | null } = {};
    const req: pb.Request_EmulateMedia = request;
    const colorScheme = req.colorScheme;
    if (colorScheme === 'not_set') {
        logger.info(`Emulating colorScheme not set`);
    } else if (colorScheme === 'null') {
        logger.info(`Emulating colorScheme null`);
        options.colorScheme = null;
    } else {
        logger.info(`Emulating colorScheme ${colorScheme}`);
        options.colorScheme = colorScheme;
    }
    const forcedColors = req.forcedColors;
    if (forcedColors === 'not_set') {
        logger.info(`Emulating forcedColors not set`);
    } else if (forcedColors === 'null') {
        logger.info(`Emulating forcedColors null`);
        options.forcedColors = null;
    } else {
        logger.info(`Emulating forcedColors ${forcedColors}`);
        options.forcedColors = forcedColors;
    }
    const media = req.media;
    if (media === 'not_set') {
        logger.info(`Emulating media not set`);
    } else if (media === 'null') {
        logger.info(`Emulating media null`);
        options.media = null;
    } else {
        logger.info(`Emulating media ${media}`);
        options.media = media;
    }
    const reducedMotion = req.reducedMotion;
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
