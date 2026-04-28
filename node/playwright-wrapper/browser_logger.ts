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

/**
 * Centralized logger configuration for the robotframework-playwright wrapper.
 *
 * Usage:
 * ```typescript
 * import { logger } from './browser_logger';
 *
 * logger.info('Information message');
 * logger.error('Error message');
 * logger.warn('Warning message');
 * logger.debug('Debug message');
 * ```
 */

import { pino, stdTimeFunctions } from 'pino';

let _seq = 0;

export interface RFKeywordContext {
    kw_name?: string;
    kw_file?: string;
    kw_line?: number;
}

const currentRFContext: RFKeywordContext = {};

export function setRFKeywordContext(ctx: RFKeywordContext): void {
    if (ctx.kw_name !== undefined) currentRFContext.kw_name = ctx.kw_name;
    if (ctx.kw_file !== undefined) currentRFContext.kw_file = ctx.kw_file;
    if (ctx.kw_line !== undefined) currentRFContext.kw_line = ctx.kw_line;
}

export function clearRFKeywordContext(): void {
    delete currentRFContext.kw_name;
    delete currentRFContext.kw_file;
    delete currentRFContext.kw_line;
}

export function getRFKeywordContext(): Readonly<RFKeywordContext> {
    return { ...currentRFContext };
}

export const logger = pino({
    timestamp: stdTimeFunctions.isoTime,
    level: process.env.ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL || 'info',
    base: null,
    formatters: {
        level(label: string) {
            return { level: label };
        },
    },
    mixin() {
        return {
            seq: ++_seq,
            component: 'browser-library',
            ...currentRFContext,
        };
    },
});
