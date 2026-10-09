// Reads node/coverage/coverage-summary.json and appends a markdown table
// to the GitHub Actions job summary (GITHUB_STEP_SUMMARY).
// Called from CI after `npm run test:coverage`.
import { appendFileSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const summary = JSON.parse(readFileSync(resolve(dir, 'coverage/coverage-summary.json'), 'utf8'));
const t = summary.total;
const fmt = (m) => `${m.covered}/${m.total} (${m.pct}%)`;
const table = [
    '## Node.js Unit Test Coverage',
    '| Metric | Coverage |',
    '|---|---|',
    `| Statements | ${fmt(t.statements)} |`,
    `| Branches   | ${fmt(t.branches)}   |`,
    `| Functions  | ${fmt(t.functions)}  |`,
    `| Lines      | ${fmt(t.lines)}      |`,
].join('\n') + '\n';

const summaryFile = process.env.GITHUB_STEP_SUMMARY;
if (summaryFile) {
    appendFileSync(summaryFile, table, 'utf8');
} else {
    process.stdout.write(table);
}
