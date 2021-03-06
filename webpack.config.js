const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = (env, argv) => {
    const prodMode = argv.mode === 'production';

    return {
        context: __dirname,
        entry: './assets/js/index',
        output: {
            path: path.resolve('./assets/bundles/'),
            filename: prodMode ? '[name]-[hash].js' : '[name].js',
        },

        optimization: {
            minimizer: prodMode ? [
                new TerserPlugin({
                    cache: true,
                    parallel: true,
                }),
                new OptimizeCSSAssetsPlugin({})
            ] : [],
        },

        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: [
                        'babel-loader',
                    ]
                },
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        'css-loader',
                        'sass-loader',
                    ]
                },
                {
                    test: /\.(png|jpg|gif)$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {},
                        },
                    ],
                },
                {
                    test: /\.(woff(2)?|ttf|eot|svg|png|jpe?g|gif)(\?v=\d+\.\d+\.\d+)?$/,
                    use: [{
                        loader: 'url-loader',
                        options: {
                            limit: 1000,
                            // match ManifestStaticFilesStorage naming schema.
                            name: '[path][name].[md5:hash:hex:12].[ext]',
                        },
                    }]
                }
            ],
        },

        plugins: [
            new MiniCssExtractPlugin({
                // Options similar to the same options in webpackOptions.output
                // both options are optional
                filename: prodMode ? '[name].[contenthash].css' : '[name].css',
                chunkFilename: prodMode ? '[id].[contenthash].css' : '[id].css',
            }),
            new BundleTracker({filename: './webpack-stats.json'}),
            new webpack.HashedModuleIdsPlugin(),
        ]
    };
}
