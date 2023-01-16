#!/usr/bin/env node
const esbuild = require('esbuild');
const { nodeExternalsPlugin } = require('esbuild-node-externals');

const context = esbuild.context({
  logLevel: "info",
  entryPoints: ["./node/playwright-wrapper/index.ts"],
  bundle: true,
  platform: "node",
  outfile: "./Browser/wrapper/index.js",
  plugins: [nodeExternalsPlugin()],
}).catch(() => process.exit(1));

context.build().catch(() => process.exit(1));
