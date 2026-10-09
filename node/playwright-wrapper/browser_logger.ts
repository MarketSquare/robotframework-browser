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
    test_id?: string;
    test_name?: string;
    suite_id?: string;
    suite_name?: string;
}

const currentRFContext: RFKeywordContext = {};
const _kwContextStack: Array<{ kw_name?: string; kw_file?: string; kw_line?: number }> = [];

export function setRFKeywordContext(ctx: RFKeywordContext): void {
    _kwContextStack.push({
        kw_name: currentRFContext.kw_name,
        kw_file: currentRFContext.kw_file,
        kw_line: currentRFContext.kw_line,
    });
    if (ctx.kw_name !== undefined) {
        currentRFContext.kw_name = ctx.kw_name;
    } else {
        delete currentRFContext.kw_name;
    }
    if (ctx.kw_file !== undefined) {
        currentRFContext.kw_file = ctx.kw_file;
    } else {
        delete currentRFContext.kw_file;
    }
    if (ctx.kw_line !== undefined) {
        currentRFContext.kw_line = ctx.kw_line;
    } else {
        delete currentRFContext.kw_line;
    }
}

export function clearRFKeywordContext(): void {
    const prev = _kwContextStack.pop();
    if (prev) {
        if (prev.kw_name !== undefined) {
            currentRFContext.kw_name = prev.kw_name;
        } else {
            delete currentRFContext.kw_name;
        }
        if (prev.kw_file !== undefined) {
            currentRFContext.kw_file = prev.kw_file;
        } else {
            delete currentRFContext.kw_file;
        }
        if (prev.kw_line !== undefined) {
            currentRFContext.kw_line = prev.kw_line;
        } else {
            delete currentRFContext.kw_line;
        }
    } else {
        delete currentRFContext.kw_name;
        delete currentRFContext.kw_file;
        delete currentRFContext.kw_line;
    }
}

export function setRFTestContext(testId: string, testName: string): void {
    if (testId) {
        currentRFContext.test_id = testId;
    } else {
        delete currentRFContext.test_id;
    }
    if (testName) {
        currentRFContext.test_name = testName;
    } else {
        delete currentRFContext.test_name;
    }
}

export function setRFSuiteContext(suiteId: string, suiteName: string): void {
    if (suiteId) {
        currentRFContext.suite_id = suiteId;
    } else {
        delete currentRFContext.suite_id;
    }
    if (suiteName) {
        currentRFContext.suite_name = suiteName;
    } else {
        delete currentRFContext.suite_name;
    }
}

export function getRFKeywordContext(): Readonly<RFKeywordContext> {
    return { ...currentRFContext };
}

export function errorType(e: unknown): string {
    return e instanceof Error ? e.constructor.name : 'UnknownError';
}

export function createLogger(destination?: { write(msg: string): void }) {
    return pino(
        {
            timestamp: stdTimeFunctions.isoTime,
            level: process.env.ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL || 'info',
            base: null,
            formatters: {
                level(label: string) {
                    return { level: label };
                },
            },
            mixin() {
                const { kw_name, kw_file, kw_line, test_id, test_name, suite_id, suite_name } = currentRFContext;
                return {
                    seq: ++_seq,
                    ...(suite_id !== undefined && { suite_id }),
                    ...(suite_name !== undefined && { suite_name }),
                    ...(test_name !== undefined && { test_name }),
                    ...(kw_name !== undefined && { kw_name }),
                    ...(kw_file !== undefined && { kw_file }),
                    ...(kw_line !== undefined && { kw_line }),
                    ...(test_id !== undefined && { test_id }),
                    component: 'browser-library',
                };
            },
        },
        destination ?? process.stdout,
    );
}

export const logger = createLogger();
