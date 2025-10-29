// vue.config.js
module.exports = {
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
        timeout: 120000,  // 120秒超时
      },
      "/process_audio": {
        target: "http://localhost:5000",
        changeOrigin: true,
        timeout: 60000,   // 60秒超时
      },
      "/voice_clone": {
        target: "http://localhost:5000",
        changeOrigin: true,
        timeout: 120000,  // 120秒超时 (语音生成需要更长时间)
      },
      "/genvoice": {
        target: "http://localhost:5000",
        changeOrigin: true,
        timeout: 30000,   // 30秒超时
      },
      "/mockvoice": {
        target: "http://localhost:5000",
        changeOrigin: true,
        timeout: 30000,   // 30秒超时
      },
    },
  },
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/assets/styles/variables.scss";`,
      },
    },
  },
  productionSourceMap: false,
  publicPath: "/",
};
