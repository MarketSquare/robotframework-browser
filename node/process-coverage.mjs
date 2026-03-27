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

// Post-processes V8 coverage data collected by NODE_V8_COVERAGE into
// HTML + LCOV reports. Run after `inv atest-coverage-node` or after
// an acceptance test run with ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE=1.

import { createRequire } from 'module';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { CoverageReport } = require('monocart-coverage-reports');

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const v8CoverageDir = process.env.NODE_V8_COVERAGE;
if (!v8CoverageDir) {
    console.error('ERROR: NODE_V8_COVERAGE environment variable is not set.');
    console.error('Run with: ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE=1 inv atest-coverage-node');
    process.exit(1);
}

const outputDir = path.resolve(__dirname, '../atest/output/node-coverage-report');

console.log(`Reading V8 coverage data from: ${v8CoverageDir}`);
console.log(`Writing coverage report to: ${outputDir}`);

const mcr = new CoverageReport({
    name: 'Node.js Wrapper Coverage',
    outputDir,
    entryFilter: (entry) => {
        const url = entry.url || '';
        // Exclude node_modules and node internals — keep only the bundled wrapper
        if (url.includes('/node_modules/')) return false;
        if (url.startsWith('node:')) return false;
        return url.includes('Browser/wrapper/index.js') || url.includes('Browser\\wrapper\\index.js');
    },
    reports: [
        ['v8', { outputFile: 'coverage.html' }],
        ['lcov', { outputFile: 'lcov.info' }],
        ['console-summary'],
    ],
});

await mcr.addFromDir(v8CoverageDir);
const coverageResults = await mcr.generate();

console.log(`\nCoverage report generated: ${outputDir}/coverage.html`);
if (coverageResults?.summary) {
    console.log(coverageResults.summary);
}
