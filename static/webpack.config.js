const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require('webpack');

module.exports = {
  entry: {
    app: "./src/js/index.js",
  },
  mode: "development",
  watch: true,
  devtool: "source-map",
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "dist"),
  },
  module: {
    rules: [{
      test: /\.(scss)$/,
      use: [
        "babel-loader",
        MiniCssExtractPlugin.loader,
        "css-loader",
        "sass-loader",

      ],
    }, ],
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
    }),
    new MiniCssExtractPlugin({
      filename: "[name].bundle.css",
      path: path.resolve(__dirname, "dist"),
    }),
  ],
  resolve: {
    extensions: [".js"],
  },
};