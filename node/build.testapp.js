#!/usr/bin/env node

const esbuild = require('esbuild');
const fs = require('fs');
const path = require('path');

const distPath = path.resolve(__dirname, './dynamic-test-app/dist');

if (!fs.existsSync(distPath)) {
    fs.mkdirSync(distPath);
}

const staticSource = path.resolve(__dirname, './dynamic-test-app/static');
const staticTarget = path.resolve(distPath, './static');
fs.rmSync(staticTarget, { recursive: true, force: true });
fs.cpSync(staticSource, staticTarget, { recursive: true });

/* Build testApp frontend */
esbuild
    .build({
        logLevel: 'info',
        entryPoints: ['./node/dynamic-test-app/src/index.tsx'],
        bundle: true,
        platform: 'browser',
        outfile: './node/dynamic-test-app/dist/index.js',
    })
    .catch(() => process.exit(1));
/* Build testApp backend */
esbuild
    .build({
        logLevel: 'info',
        entryPoints: ['./node/dynamic-test-app/src/server.ts'],
        bundle: true,
        platform: 'node',
        outfile: './node/dynamic-test-app/dist/server.js',
        /* plugins: [nodeExternalsPlugin()], */
    })
    .catch(() => process.exit(1));
