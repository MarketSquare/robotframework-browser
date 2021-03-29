const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require("copy-webpack-plugin");

const sharedAll = {
    mode: 'development',
    devtool: 'inline-source-map',
    performance: { hints: false } ,
    stats: 'minimal',
    resolve: {
        extensions: [ '.tsx', '.ts', '.js' ],
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
}

const testappFrontend = {
    entry: './node/dynamic-test-app/src/index.tsx',
    target: 'web',

    plugins: [
        new HtmlWebpackPlugin({
            title: 'Output Management',
            template: './node/dynamic-test-app/static/index.html',
        }),
    ],
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, './dynamic-test-app/dist')
    },
    ...sharedAll
};

const sharedNode = {
    target: 'node',
    node: {
        __filename: true,
        __dirname: true
    },
}

const testappBackend = {
    entry: './node/dynamic-test-app/src/server.ts',
    output: {
        filename: 'server.js',
        path: path.resolve(__dirname, './dynamic-test-app/dist')
    },
    ...sharedNode,
    ...sharedAll,
}

const playwrightWrapper = {
    entry: './node/playwright-wrapper/index.ts',
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, '../Browser/wrapper')
    },
    externals: {
        grpc: 'commonjs grpc',
        playwright: 'commonjs playwright'
    },
    plugins: [
        new CopyPlugin({
          patterns: [
            {
                from: "./node/playwright-wrapper/static",
                to: path.resolve(__dirname, '../Browser/wrapper/static')
            },
          ],
        }),
    ],
    ...sharedNode,
    ...sharedAll,
}

module.exports = [testappFrontend, testappBackend, playwrightWrapper]
