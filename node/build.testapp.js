#!/usr/bin/env node

const esbuild = require('esbuild');
const { nodeExternalsPlugin } = require('esbuild-node-externals');
const fs = require('fs');

/* Build testApp frontend */
esbuild.build(
  {
    logLevel: "info",
    entryPoints: ['./node/dynamic-test-app/src/index.tsx'],
    bundle: true,
    platform: "browser",
    outfile: "./node/dynamic-test-app/dist/index.js",
  }
).catch(() => process.exit(1));

fs.copyFileSync('./node/dynamic-test-app/static/index.html', './node/dynamic-test-app/dist/index.html')

/* Build testApp backend */
esbuild.build(
  {
    logLevel: "info",
    entryPoints: ["./node/dynamic-test-app/src/server.ts"],
    bundle: true,
    platform: "node",
    outfile: "./node/dynamic-test-app/dist/server.js",
    plugins: [nodeExternalsPlugin()],

  }
).catch(() => process.exit(1));


