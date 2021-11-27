const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

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

const testappBackend = {
    entry: './node/dynamic-test-app/src/server.ts',
    output: {
        filename: 'server.js',
        path: path.resolve(__dirname, './dynamic-test-app/dist')
    },
    target: 'node',
    node: {
        global: false,
        __filename: false,
        __dirname: false,
    },
    ...sharedAll,
}

module.exports = [testappFrontend, testappBackend]
