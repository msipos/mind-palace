const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const devMode = process.env.NODE_ENV !== "production";

module.exports = {
  plugins: [new MiniCssExtractPlugin({
    filename: "site.css"
  })],
  entry: './index.js',
  output: {
    filename: 'site.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: [
            MiniCssExtractPlugin.loader,
            'css-loader'
        ],
      },
      {
        test: /\.(js)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ],
  },
};