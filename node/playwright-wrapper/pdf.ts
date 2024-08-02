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
import { stringResponse, emptyWithLog } from './response-util';

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
    const media = request.getMedia();
    logger.info(`Emulating media ${media}`);
    await activePage.emulateMedia({ media: media });
    return emptyWithLog(`Emulating media ${media}`);
}
