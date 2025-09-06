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

export const logger = pino({
    timestamp: stdTimeFunctions.isoTime,
    level: process.env.ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL || 'info',
});
