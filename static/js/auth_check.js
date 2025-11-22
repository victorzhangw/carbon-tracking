/**
 * 通用登入檢查模組
 * 在需要登入的頁面中引入此文件
 */

// 檢查登入狀態
function checkLoginStatus() {
  const currentUser = localStorage.getItem("currentUser");
  if (!currentUser) {
    // 未登入，跳轉到登入頁面
    window.location.href =
      "/login?return=" + encodeURIComponent(window.location.pathname);
    return false;
  }

  try {
    const userData = JSON.parse(currentUser);
    console.log("✅ 用戶已登入:", userData.full_name || userData.username);
    return userData;
  } catch (error) {
    console.error("解析用戶資訊失敗:", error);
    localStorage.removeItem("currentUser");
    window.location.href = "/login";
    return false;
  }
}

// 獲取當前用戶資訊
function getCurrentUser() {
  const currentUser = localStorage.getItem("currentUser");
  if (!currentUser) {
    return null;
  }

  try {
    return JSON.parse(currentUser);
  } catch (error) {
    console.error("解析用戶資訊失敗:", error);
    return null;
  }
}

// 顯示用戶資訊（在頁面右上角）
function showUserInfo(options = {}) {
  const userData = getCurrentUser();
  if (!userData) return;

  const {
    position = "top-right",
    showLogout = true,
    customStyle = "",
  } = options;

  // 檢查是否已存在用戶資訊元素
  let userInfo = document.getElementById("userInfoDisplay");
  if (userInfo) {
    userInfo.remove();
  }

  // 創建用戶資訊元素
  userInfo = document.createElement("div");
  userInfo.id = "userInfoDisplay";

  // 設置位置樣式
  let positionStyle = "";
  switch (position) {
    case "top-right":
      positionStyle = "top: 20px; right: 20px;";
      break;
    case "top-left":
      positionStyle = "top: 20px; left: 20px;";
      break;
    case "bottom-right":
      positionStyle = "bottom: 20px; right: 20px;";
      break;
    case "bottom-left":
      positionStyle = "bottom: 20px; left: 20px;";
      break;
  }

  userInfo.style.cssText = `
    position: fixed;
    ${positionStyle}
    background: white;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    z-index: 1000;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    ${customStyle}
  `;

  const userName = document.createElement("span");
  userName.style.color = "#666";
  userName.textContent = "👤 " + (userData.full_name || userData.username);
  userInfo.appendChild(userName);

  if (showLogout) {
    const logoutBtn = document.createElement("button");
    logoutBtn.textContent = "登出";
    logoutBtn.style.cssText = `
      padding: 4px 12px;
      border: 1px solid #e9ecef;
      border-radius: 4px;
      background: white;
      cursor: pointer;
      font-size: 12px;
      transition: all 0.2s;
    `;
    logoutBtn.onmouseover = function () {
      this.style.background = "#f8f9fa";
    };
    logoutBtn.onmouseout = function () {
      this.style.background = "white";
    };
    logoutBtn.onclick = logout;
    userInfo.appendChild(logoutBtn);
  }

  document.body.appendChild(userInfo);
}

// 登出功能
function logout() {
  if (confirm("確定要登出嗎？")) {
    localStorage.removeItem("currentUser");
    window.location.href = "/login";
  }
}

// 驗證用戶是否有特定權限（可擴展）
function hasPermission(permission) {
  const userData = getCurrentUser();
  if (!userData) return false;

  // 這裡可以根據實際需求實現權限檢查
  // 例如：return userData.permissions?.includes(permission);
  return true;
}

// 自動初始化（頁面載入時檢查登入）
if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", function () {
    // 檢查是否在登入頁面
    if (window.location.pathname !== "/login") {
      const userData = checkLoginStatus();
      if (userData) {
        // 自動顯示用戶資訊（可選）
        // showUserInfo();
      }
    }
  });
}

// 導出函數供其他腳本使用
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    checkLoginStatus,
    getCurrentUser,
    showUserInfo,
    logout,
    hasPermission,
  };
}
