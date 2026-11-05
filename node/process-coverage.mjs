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

// LCOV `SF:` paths are relative to the repository root, the same as Jest's, so
// both tracefiles can be merged.

import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { CoverageReport } = require('monocart-coverage-reports');

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const inputDirs = process.argv.slice(2);
if (inputDirs.length === 0) {
    console.error('Usage: node node/process-coverage.mjs <v8-coverage-dir> [<v8-coverage-dir> ...]');
    process.exit(1);
}
const withData = inputDirs.filter((dir) => fs.existsSync(dir) && fs.readdirSync(dir).some((f) => f.endsWith('.json')));
if (withData.length === 0) {
    console.error(`ERROR: no V8 coverage data in ${inputDirs.join(', ')}`);
    process.exit(1);
}

const outputDir = path.resolve(__dirname, '../atest/output/node-coverage-report');

console.log(`Reading V8 coverage data from: ${withData.join(', ')}`);
console.log(`Writing coverage report to: ${outputDir}`);

const mcr = new CoverageReport({
    name: 'Node.js Wrapper Coverage',
    outputDir,
    entryFilter: (entry) => {
        const url = entry.url || '';
        if (url.includes('/node_modules/')) return false;
        if (url.startsWith('node:')) return false;
        return url.includes('Browser/wrapper/index.js') || url.includes('Browser\\wrapper\\index.js');
    },
    sourceFilter: (sourcePath) =>
        sourcePath.includes('node/playwright-wrapper/') && !sourcePath.includes('/generated/'),
    sourcePath: (sourcePath) => sourcePath.replace(/^.*?\/node\/playwright-wrapper\//, 'node/playwright-wrapper/'),
    reports: [['v8', { outputFile: 'coverage.html' }], ['lcov', { outputFile: 'lcov.info' }], ['console-summary']],
});

for (const dir of withData) {
    await mcr.addFromDir(dir);
}
await mcr.generate();

console.log(`\nCoverage report generated: ${outputDir}/coverage.html`);
console.log(`LCOV: ${outputDir}/lcov.info`);
