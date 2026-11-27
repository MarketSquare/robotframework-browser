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

import { AsyncLocalStorage } from 'node:async_hooks';

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

type KeywordFields = Pick<RFKeywordContext, 'kw_name' | 'kw_file' | 'kw_line'>;

export class RFContext {
    private suiteAndTest: Omit<RFKeywordContext, keyof KeywordFields> = {};
    private keywords: KeywordFields[] = [];

    setTest(testId: string, testName: string): void {
        this.suiteAndTest.test_id = testId || undefined;
        this.suiteAndTest.test_name = testName || undefined;
    }

    setSuite(suiteId: string, suiteName: string): void {
        this.suiteAndTest.suite_id = suiteId || undefined;
        this.suiteAndTest.suite_name = suiteName || undefined;
    }

    openKeyword(keyword: KeywordFields, depth: number): void {
        this.closeKeywordsTo(depth);
        this.keywords.push({ ...keyword });
    }

    closeKeywordsTo(depth: number): void {
        this.keywords.length = Math.min(this.keywords.length, depth);
    }

    get fields(): Readonly<RFKeywordContext> {
        return { ...this.suiteAndTest, ...this.keywords[this.keywords.length - 1] };
    }
}

const servedRFContext = new AsyncLocalStorage<RFContext>();

export function runInRFContext<T>(context: RFContext, fn: () => T): T {
    return servedRFContext.run(context, fn);
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
                const { kw_name, kw_file, kw_line, test_id, test_name, suite_id, suite_name } =
                    servedRFContext.getStore()?.fields ?? {};
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
