const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './src/index.js',
    module: {
        rules: [
            { test: /\.s[ac]ss$/i, use: ['style-loader','css-loader','sass-loader'] },
            { test: /\.css$/i, use: ['style-loader','css-loader','sass-loader'] },
            { test: /\.(js)$/, use: 'babel-loader' },
        ]
    },
    output: {
       path: path.resolve(__dirname, '../chemate/webapp/static'),
       filename: 'index.js'
    },
    plugins: [
        new HtmlWebpackPlugin({template: 'src/index.html'}),
    ]
}