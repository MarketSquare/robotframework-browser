#!/usr/bin/env node
const esbuild = require('esbuild');
const { nodeExternalsPlugin } = require('esbuild-node-externals');

const withCoverage = process.env.ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE === '1';

const shared = {
    logLevel: 'info',
    bundle: true,
    platform: 'node',
    sourcemap: withCoverage ? 'external' : false,
    // Runs before every other module in the bundle, which it must: it has to
    // patch require() before Playwright is loaded. See inspector-shim.ts.
    inject: ['./node/playwright-wrapper/inspector-shim.ts'],
    plugins: [
        nodeExternalsPlugin({
            // Allow UUID to be bundled instead of external
            // Needed when building with pkg
            allowList: ['uuid'],
        }),
    ],
    external: ['playwright-core/*'],
};

Promise.all([
    esbuild.build({
        ...shared,
        entryPoints: ['./node/playwright-wrapper/index.ts'],
        outfile: './Browser/wrapper/index.js',
    }),
    // Entry point for the children Playwright forks. Picked up by pkg through
    // the "Browser/wrapper/*.js" scripts glob in package.json.
    esbuild.build({
        ...shared,
        entryPoints: ['./node/playwright-wrapper/fork-bootstrap.ts'],
        outfile: './Browser/wrapper/fork-bootstrap.js',
    }),
]).catch(() => process.exit(1));
