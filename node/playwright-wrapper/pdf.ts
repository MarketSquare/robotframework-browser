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
    logger.info(`Saving pdf to ${pdfPath}`);
    logger.info(`Using options: displayHeaderFooter: ${displayheaderfooter}`, `footerTemplate: ${footertemplate}`);
    await activePage.pdf({ path: pdfPath, displayHeaderFooter: displayheaderfooter, footerTemplate: footertemplate});
return stringResponse(pdfPath, `Pdf is saved to ${pdfPath}`);
}
