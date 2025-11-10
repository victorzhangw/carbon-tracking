// PWA Service Worker 註冊與管理

// 檢查瀏覽器支援
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    registerServiceWorker();
    checkForUpdates();
    setupInstallPrompt();
  });
}

// 註冊 Service Worker
async function registerServiceWorker() {
  try {
    const registration = await navigator.serviceWorker.register(
      "/static/sw.js",
      {
        scope: "/carbon/",
      }
    );

    console.log("✅ Service Worker 註冊成功:", registration.scope);

    // 監聽更新
    registration.addEventListener("updatefound", () => {
      const newWorker = registration.installing;
      console.log("🔄 發現新版本 Service Worker");

      newWorker.addEventListener("statechange", () => {
        if (
          newWorker.state === "installed" &&
          navigator.serviceWorker.controller
        ) {
          showUpdateNotification();
        }
      });
    });

    return registration;
  } catch (error) {
    console.error("❌ Service Worker 註冊失敗:", error);
  }
}

// 檢查更新
async function checkForUpdates() {
  if (!navigator.serviceWorker.controller) return;

  try {
    const registration = await navigator.serviceWorker.getRegistration(
      "/carbon/"
    );
    if (registration) {
      registration.update();
    }
  } catch (error) {
    console.error("檢查更新失敗:", error);
  }
}

// 顯示更新通知
function showUpdateNotification() {
  const notification = document.createElement("div");
  notification.id = "pwa-update-notification";
  notification.innerHTML = `
    <div style="
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: #689F38;
      color: white;
      padding: 15px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 10000;
      display: flex;
      align-items: center;
      gap: 15px;
      font-family: 'Microsoft JhengHei', Arial, sans-serif;
      font-size: 14px;
    ">
      <span>🎉 新版本已就緒！</span>
      <button onclick="updateServiceWorker()" style="
        background: white;
        color: #689F38;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
      ">
        立即更新
      </button>
      <button onclick="dismissUpdateNotification()" style="
        background: transparent;
        color: white;
        border: 1px solid white;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
      ">
        稍後
      </button>
    </div>
  `;
  document.body.appendChild(notification);
}

// 更新 Service Worker
window.updateServiceWorker = async function () {
  const registration = await navigator.serviceWorker.getRegistration(
    "/carbon/"
  );
  if (registration && registration.waiting) {
    registration.waiting.postMessage({ type: "SKIP_WAITING" });
    window.location.reload();
  }
};

// 關閉更新通知
window.dismissUpdateNotification = function () {
  const notification = document.getElementById("pwa-update-notification");
  if (notification) {
    notification.remove();
  }
};

// 設定安裝提示
let deferredPrompt;

function setupInstallPrompt() {
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallButton();
  });

  window.addEventListener("appinstalled", () => {
    console.log("✅ PWA 已安裝");
    deferredPrompt = null;
    hideInstallButton();
  });
}

// 顯示安裝按鈕
function showInstallButton() {
  const installBtn = document.getElementById("pwa-install-btn");
  if (installBtn) {
    installBtn.style.display = "block";
  }
}

// 隱藏安裝按鈕
function hideInstallButton() {
  const installBtn = document.getElementById("pwa-install-btn");
  if (installBtn) {
    installBtn.style.display = "none";
  }
}

// 安裝 PWA
window.installPWA = async function () {
  if (!deferredPrompt) {
    console.log("無法安裝：沒有安裝提示");
    return;
  }

  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;

  console.log(`使用者選擇: ${outcome}`);
  deferredPrompt = null;
  hideInstallButton();
};

// 檢查是否在獨立模式運行（已安裝為 PWA）
function isStandalone() {
  return (
    window.matchMedia("(display-mode: standalone)").matches ||
    window.navigator.standalone === true
  );
}

// 顯示 PWA 狀態
if (isStandalone()) {
  console.log("✅ 以 PWA 模式運行");
} else {
  console.log("ℹ️ 以瀏覽器模式運行");
}

// 網路狀態監控
window.addEventListener("online", () => {
  console.log("✅ 網路已連線");
  showNetworkStatus("online");
});

window.addEventListener("offline", () => {
  console.log("⚠️ 網路已斷線");
  showNetworkStatus("offline");
});

function showNetworkStatus(status) {
  const existingStatus = document.getElementById("network-status");
  if (existingStatus) {
    existingStatus.remove();
  }

  if (status === "offline") {
    const statusBar = document.createElement("div");
    statusBar.id = "network-status";
    statusBar.innerHTML = `
      <div style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #FF9800;
        color: white;
        padding: 8px;
        text-align: center;
        z-index: 10000;
        font-size: 14px;
        font-family: 'Microsoft JhengHei', Arial, sans-serif;
      ">
        ⚠️ 目前離線模式，部分功能可能受限
      </div>
    `;
    document.body.appendChild(statusBar);
  }
}

// 清除快取（開發用）
window.clearPWACache = async function () {
  if ("serviceWorker" in navigator) {
    const registration = await navigator.serviceWorker.getRegistration(
      "/carbon/"
    );
    if (registration) {
      registration.active.postMessage({ type: "CLEAR_CACHE" });
      console.log("✅ 快取已清除");
    }
  }
};

// 匯出功能供外部使用
window.PWA = {
  install: installPWA,
  update: updateServiceWorker,
  clearCache: clearPWACache,
  isStandalone: isStandalone,
};
