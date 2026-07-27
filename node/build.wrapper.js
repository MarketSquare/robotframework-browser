#!/usr/bin/env node
const esbuild = require('esbuild');
const { nodeExternalsPlugin } = require('esbuild-node-externals');

const withCoverage = process.env.ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE === '1';

esbuild
    .build({
        logLevel: 'info',
        entryPoints: ['./node/playwright-wrapper/index.ts'],
        bundle: true,
        platform: 'node',
        outfile: './Browser/wrapper/index.js',
        sourcemap: withCoverage ? 'external' : false,
        plugins: [
            nodeExternalsPlugin({
                // uuid is ESM only, it has no CommonJS entry point at all, and
                // this bundle is CommonJS. Left external it becomes a
                // require() of an ES module, which NodeJS 22.11 and older
                // refuse outright and newer versions only allow with an
                // experimental warning on every start. Bundling converts it at
                // build time instead, so it works on every supported NodeJS.
                allowList: ['uuid'],
            }),
        ],
        external: ['playwright-core/*'],
    })
    .catch(() => process.exit(1));
