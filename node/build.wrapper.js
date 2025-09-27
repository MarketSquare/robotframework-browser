#!/usr/bin/env node
const esbuild = require('esbuild');
const { nodeExternalsPlugin } = require('esbuild-node-externals');

esbuild.build(
  {
    logLevel: "info",
    entryPoints: ["./node/playwright-wrapper/index.ts"],
    bundle: true,
    platform: "node",
    outfile: "./Browser/wrapper/index.js",
    plugins: [nodeExternalsPlugin({
      // Allow UUID to be bundled instead of external
      // Needed when building with pkg
      allowList: ['uuid']
    })],
    external: [
      'playwright-core/*',
    ],
  }
).catch(() => process.exit(1));
