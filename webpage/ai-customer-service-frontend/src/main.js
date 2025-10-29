// main.js
import Vue from "vue";
import App from "./App.vue";
import ViewUI from "view-design";
import router from "./router";
import store from "./store";

// 首先導入 iView UI 原始樣式
import "view-design/dist/styles/iview.css";
// 然後導入我們的主題樣式和自定義覆蓋樣式
import "./assets/styles/theme.scss";
import "./assets/styles/iview-override.scss";
import locale from "view-design/dist/locale/zh-TW";
import axios from "axios";

// 設定 ViewUI（iView）
Vue.use(ViewUI, {
  locale: locale,
});

// 自定義 ViewUI 全局配置
//ViewUI.config.colorPrimary = "#2d8cf0"; // 可自訂主色調

// 設定 axios
axios.defaults.baseURL = "http://127.0.0.1:5000"; // 設定 API 基礎路徑指向 Flask 後端
axios.defaults.timeout = 10000; // 設定請求超時
console.log('Axios baseURL 設置為:', axios.defaults.baseURL);
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    // 全局錯誤處理
    if (error.response) {
      const status = error.response.status;

      if (status === 401) {
        // 未授權處理
        Vue.prototype.$Message.warning("登入已過期，請重新登入");
      } else if (status === 403) {
        // 禁止訪問處理
        Vue.prototype.$Message.error("您沒有權限進行此操作");
      } else if (status === 404) {
        // 資源不存在處理
        Vue.prototype.$Message.error("請求的資源不存在");
      } else if (status === 500) {
        // 服務器錯誤處理
        Vue.prototype.$Message.error("伺服器發生錯誤，請稍後再試");
      }
    } else if (error.request) {
      // 請求已發送但沒有收到回應
      Vue.prototype.$Message.error("無法連接到伺服器，請檢查網路連接");
    } else {
      // 其他錯誤
      Vue.prototype.$Message.error("請求發生錯誤：" + error.message);
    }

    return Promise.reject(error);
  }
);

// 將 axios 添加到 Vue 原型，方便使用
Vue.prototype.$axios = axios;

// 全局設定
Vue.config.productionTip = false;

// 加入全局指令
Vue.directive("focus", {
  inserted: function (el) {
    // 對於一些複合元件，需要找到實際的輸入框
    if (el.tagName.toLowerCase() !== "input") {
      const input = el.querySelector("input");
      if (input) {
        input.focus();
      }
    } else {
      el.focus();
    }
  },
});

// 頁面加載時的進度條設定
ViewUI.LoadingBar.config({
  color: "#7cb342",
  height: 3,
});

// DOM 準備好後的處理函數
const handleDOMReady = () => {
  // 移除頁面載入動畫
  const loadingElement = document.getElementById("app-loading");
  if (loadingElement) {
    setTimeout(() => {
      loadingElement.classList.add("loaded");
      setTimeout(() => {
        loadingElement.style.display = "none";
      }, 500);
    }, 800);
  }

  // 滾動平滑化
  const links = document.querySelectorAll('a[href^="#"]');

  for (const link of links) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  }
};

// 確保 DOM 已完全加載
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", handleDOMReady);
} else {
  // 如果 DOMContentLoaded 已觸發，直接執行
  handleDOMReady();
}

// 初始化認證狀態
store.dispatch('auth/initializeAuth');

// 初始化 Vue 實例
new Vue({
  router,
  store,
  render: (h) => h(App),
  mounted() {
    // 啟動時的歡迎信息
    this.$Message.success({
      content: "歡迎使用 AI 客服管理系統",
      duration: 3,
    });

    // 確保根元素高度為視窗高度
    const setHeight = () => {
      document.documentElement.style.setProperty(
        "--vh",
        `${window.innerHeight * 0.01}px`
      );
    };

    // 初始設定
    setHeight();

    // 視窗大小變化時重新設定
    window.addEventListener("resize", setHeight);
  },
}).$mount("#app");
