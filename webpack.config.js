const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: './dynamic-test-app/index.tsx',
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
            template: './dynamic-test-app/index.html',
        }),
    ],
    resolve: {
        extensions: [ '.tsx', '.ts', '.js' ],
    },
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, 'atest/demoapp/html/dist/')
    },
};
