#!/usr/bin/env node
const esbuild = require('esbuild');
const { nodeExternalsPlugin } = require('esbuild-node-externals');

esbuild.build({
    logLevel: "info",
    entryPoints: ["./node/playwright-wrapper/index.ts"],
    bundle: true,
    platform: "node",
    outfile: "./Browser/wrapper/index.js",
    plugins: [nodeExternalsPlugin()],
  })
  .catch(() => process.exit(1));
