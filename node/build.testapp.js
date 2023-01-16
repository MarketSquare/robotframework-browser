#!/usr/bin/env node

const esbuild = require('esbuild');
const { nodeExternalsPlugin } = require('esbuild-node-externals');
const fs = require('fs');
const path = require('path')

const distPath = path.resolve(__dirname, './dynamic-test-app/dist')

if (!fs.existsSync(distPath)) {
  fs.mkdirSync(distPath);
}

const indexHtmlSource = path.resolve(__dirname, './dynamic-test-app/static/index.html')
const indexHtmlTarget = path.resolve(distPath, './index.html')
fs.copyFileSync(indexHtmlSource,  indexHtmlTarget)

const frontendContext = await esbuild.context({
  logLevel: "info",
  entryPoints: ['./node/dynamic-test-app/src/index.tsx'],
  bundle: true,
  platform: "browser",
  outfile: "./node/dynamic-test-app/dist/index.js",
}).catch(() => process.exit(1));
/* Build testApp frontend */
await frontendContext.build().catch(() => process.exit(1));

/* Build testApp backend */
const backendContext = await esbuild.context({
  logLevel: "info",
  entryPoints: ["./node/dynamic-test-app/src/server.ts"],
  bundle: true,
  platform: "node",
  outfile: "./node/dynamic-test-app/dist/server.js",
  /* plugins: [nodeExternalsPlugin()], */
}).catch(() => process.exit(1));
await backendContext.build().catch(() => process.exit(1));
