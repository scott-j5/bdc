const Path = require('path');

const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const CopyWebpackPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require("terser-webpack-plugin");

const opts = {
    rootDir: process.cwd(),
    staticSrcDir: './assets/',
    devBuild: process.env.NODE_ENV !== "production"
};

module.exports = {
    entry: {
        app: opts.staticSrcDir + 'js/index.js',
    },
    watch: true,
    mode: process.env.NODE_ENV === "production" ? "production" : "development",
    devtool:
      process.env.NODE_ENV === "production" ? "source-map" : "inline-source-map",
    output: {
      path: Path.join(opts.rootDir, "dist"),
      pathinfo: opts.devBuild,
      filename: "[name].js",
      chunkFilename: '[name].js',
      clean: true,
    },
    performance: { hints: false },
    optimization: {
		minimize: true,
        minimizer: [
          new TerserPlugin({
            parallel: true,
            terserOptions: {
              ecma: 5
            }
          }),
          new CssMinimizerPlugin({}),
        ],
        runtimeChunk: false
    },
    plugins: [
        // Extract css files to seperate bundle
        new MiniCssExtractPlugin({
            filename: "app.css",
            chunkFilename: "app.css"
        }),
        // Copy fonts and images to dist
        new CopyWebpackPlugin({
            patterns: [
                { from: opts.staticSrcDir + "fonts", to: "fonts" },
                { from: opts.staticSrcDir + "img", to: "img" }
            ]
        }),
    ],
    module: {
        rules: [
            // Babel-loader
            {
                test: /\.m?js$/,
                exclude: /node_modules/,
                use: {
					loader: 'babel-loader?cacheDirectory=true',
                }
            },
            
            // Css-loader & sass-loader
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
					"css-loader",
					{
						// Run postcss actions
						loader: 'postcss-loader',
						options: {
							// `postcssOptions` is needed for postcss 8.x;
							// if you use postcss 7.x skip the key
							postcssOptions: {
								// postcss plugins, can be exported to postcss.config.js
								plugins: function () {
									return [
										require('autoprefixer')
									];
								}
							}
						}
					},
                    "sass-loader"
                ]
            },
            // Load fonts
            {
				test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                type: "asset/resource",
                generator: {
                    filename: 'fonts/[hash][ext][query]',
                }
            },
            // Load images
            {
				test: /\.(png|jpg|jpeg|gif)(\?v=\d+\.\d+\.\d+)?$/,
				type: "asset/resource",
                generator: {
                    filename: 'img/[hash][ext][query]',
                }
            }
        ]
    },
    resolve: {
        extensions: [".js", ".scss"],
        modules: ["node_modules"],
        alias: {
            request$: "xhr"
        }
    },
    watchOptions: {
        aggregateTimeout: 500,
        poll: 1500,
        ignored: /node_modules/,
    },
    /*
    devServer: {
        contentBase: Path.join(__dirname, "static"),
        compress: true,
        port: 8080,
        open: true
    },*/
}