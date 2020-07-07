const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const frontConfig = {
    target: 'web',
    mode: 'development',
    entry: './atest/dynamic-test-app/src/index.tsx',
    devtool: 'inline-source-map',
    performance: { hints: false } ,
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'Output Management',
            template: './atest/dynamic-test-app/static/index.html',
        }),
    ],
    resolve: {
        extensions: [ '.tsx', '.ts', '.js' ],
    },
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, './atest/dynamic-test-app/dist')
    },
};

const backConfig = {
    target: 'node',
    mode: 'development',
    entry: './atest/dynamic-test-app/src/server.ts',
    devtool: 'inline-source-map',
    performance: { hints: false } ,
    node: {
        __filename: true,
        __dirname: true
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
    output: {
        filename: 'server.js',
        path: path.resolve(__dirname, 'atest/dynamic-test-app/dist')
    },
}

module.exports = [frontConfig, backConfig]
