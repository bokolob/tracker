
module.exports = {
  // options...
  publicPath: '/app/',
  configureWebpack: {
    devtool: 'source-map',
    entry: ['share-api-polyfill', './src/main.js']
  }

}
