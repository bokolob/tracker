module.exports = {
    entry: [
        './src/index.js',
        './src/calendar.js',
        './src/coordinates.js',
        './src/forms.js',
        './src/models.js',
    ],
    optimization: {
        minimize: false
    },
    devtool: "source-map",
    module: {
        rules: [
          {
            test: /\.js$/,
            exclude: /node_modules/,
            use: {
              loader: "babel-loader"
            },
          },
          {
            test: require.resolve("jquery"),
            loader: "expose-loader",
            options: {
              exposes: ["$", "jQuery"],
            },
          },
        ]
    },
    resolve: {
        alias: {
          'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' для webpack 1
        }
    },
    output: {
      path: __dirname + "/../static",
      filename: 'bundle.js',
    }
  };
