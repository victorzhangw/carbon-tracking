# 📱 碳排放追蹤系統 - 轉換為 Android App 指南

## 🎯 三種主要方案比較

| 方案                | 難度          | 開發時間 | 效能 | 原生功能 | 維護成本 |
| ------------------- | ------------- | -------- | ---- | -------- | -------- |
| **1. WebView 包裝** | ⭐ 簡單       | 1-2 天   | 中   | 有限     | 低       |
| **2. PWA + TWA**    | ⭐⭐ 中等     | 3-5 天   | 中高 | 中等     | 低       |
| **3. React Native** | ⭐⭐⭐⭐ 困難 | 2-4 週   | 高   | 完整     | 高       |

---

## 🚀 方案一：WebView 包裝（最快速）

### 優點

✅ 最快速（1-2 天完成）  
✅ 無需重寫程式碼  
✅ 維護簡單  
✅ 適合快速上架

### 缺點

❌ 效能較差  
❌ 原生功能有限  
❌ 需要網路連線

### 實作步驟

#### Step 1: 安裝 Android Studio

```bash
# 下載 Android Studio
https://developer.android.com/studio

# 安裝 JDK 17+
https://www.oracle.com/java/technologies/downloads/
```

#### Step 2: 建立 Android 專案

```bash
# 在 Android Studio 中
1. New Project
2. 選擇 "Empty Activity"
3. 設定：
   - Name: CarbonTracking
   - Package: com.yourcompany.carbontracking
   - Language: Kotlin
   - Minimum SDK: API 24 (Android 7.0)
```

#### Step 3: 修改 AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.yourcompany.carbontracking">

    <!-- 網路權限 -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <!-- GPS 權限（如需定位功能） -->
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="碳排放追蹤"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.CarbonTracking"
        android:usesCleartextTraffic="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

#### Step 4: MainActivity.kt

```kotlin
package com.yourcompany.carbontracking

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebSettings
import androidx.appcompat.app.AppCompatActivity
import android.view.KeyEvent

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    // 你的後端伺服器網址
    private val SERVER_URL = "http://your-server-ip:5000/carbon/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webview)
        setupWebView()

        // 載入網頁
        webView.loadUrl(SERVER_URL)
    }

    private fun setupWebView() {
        webView.webViewClient = WebViewClient()

        val webSettings: WebSettings = webView.settings
        webSettings.javaScriptEnabled = true
        webSettings.domStorageEnabled = true
        webSettings.databaseEnabled = true
        webSettings.cacheMode = WebSettings.LOAD_DEFAULT
        webSettings.allowFileAccess = true
        webSettings.allowContentAccess = true

        // 支援縮放
        webSettings.setSupportZoom(true)
        webSettings.builtInZoomControls = true
        webSettings.displayZoomControls = false

        // 自適應螢幕
        webSettings.useWideViewPort = true
        webSettings.loadWithOverviewMode = true
    }

    // 支援返回鍵
    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }
}
```

#### Step 5: activity_main.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

</RelativeLayout>
```

#### Step 6: 建立 App Icon

```bash
# 使用 Android Studio 的 Image Asset Studio
1. 右鍵點擊 res 資料夾
2. New > Image Asset
3. 上傳你的 icon 圖片（建議 512x512 PNG）
4. 生成各種尺寸的 icon
```

---

## 🌐 方案二：PWA + TWA（推薦）

### 優點

✅ 接近原生體驗  
✅ 可離線使用  
✅ 自動更新  
✅ Google Play 認可  
✅ 無需重寫程式碼

### 缺點

❌ 需要 HTTPS  
❌ 需要設定 Service Worker

### 實作步驟

#### Step 1: 將網站改為 PWA

##### 1.1 建立 manifest.json

```json
{
  "name": "碳排放追蹤系統",
  "short_name": "碳追蹤",
  "description": "社工訪視碳排放追蹤與管理系統",
  "start_url": "/carbon/",
  "display": "standalone",
  "background_color": "#F1F8E9",
  "theme_color": "#689F38",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/static/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

##### 1.2 建立 Service Worker (sw.js)

```javascript
const CACHE_NAME = "carbon-tracking-v1";
const urlsToCache = [
  "/carbon/",
  "/carbon/dashboard",
  "/carbon/visit-records",
  "/carbon/add-visit",
  "/carbon/statistics",
  "/static/css/main.css",
  "/static/js/main.js",
];

// 安裝 Service Worker
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
});

// 攔截請求
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // 快取命中，返回快取
      if (response) {
        return response;
      }
      // 否則發送網路請求
      return fetch(event.request);
    })
  );
});

// 更新 Service Worker
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
```

##### 1.3 在 HTML 中註冊 Service Worker

```html
<!-- 在所有頁面的 <head> 中加入 -->
<link rel="manifest" href="/static/manifest.json" />
<meta name="theme-color" content="#689F38" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta
  name="apple-mobile-web-app-status-bar-style"
  content="black-translucent"
/>
<meta name="apple-mobile-web-app-title" content="碳追蹤" />

<!-- 在 </body> 前加入 -->
<script>
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .register("/static/sw.js")
      .then((reg) => console.log("Service Worker 註冊成功", reg))
      .catch((err) => console.log("Service Worker 註冊失敗", err));
  }
</script>
```

#### Step 2: 使用 Bubblewrap 建立 TWA

##### 2.1 安裝 Bubblewrap

```bash
npm install -g @bubblewrap/cli
```

##### 2.2 初始化專案

```bash
bubblewrap init --manifest https://your-domain.com/static/manifest.json
```

##### 2.3 建立 APK

```bash
bubblewrap build
```

##### 2.4 簽署 APK

```bash
# 生成金鑰
keytool -genkey -v -keystore carbon-tracking.keystore -alias carbon -keyalg RSA -keysize 2048 -validity 10000

# 簽署
bubblewrap build --signingKeyPath carbon-tracking.keystore --signingKeyAlias carbon
```

---

## 📦 方案三：React Native（完整原生）

### 適用情境

- 需要完整原生功能（相機、GPS、推播）
- 需要最佳效能
- 有充足開發時間和預算

### 架構設計

```
React Native App (前端)
    ↓ REST API
Flask Backend (後端)
    ↓
SQLite Database
```

### 技術棧

- **前端**：React Native + TypeScript
- **狀態管理**：Redux Toolkit
- **導航**：React Navigation
- **API**：Axios
- **圖表**：Victory Native
- **地圖**：React Native Maps

### 開發步驟概要

1. 設定 React Native 環境
2. 建立專案結構
3. 實作 API 連接層
4. 重建所有頁面 UI
5. 實作離線功能
6. 測試與優化
7. 打包上架

---

## 🚀 上架 Google Play 流程

### 準備工作

#### 1. 註冊 Google Play 開發者帳號

```
費用：一次性 $25 USD
網址：https://play.google.com/console
```

#### 2. 準備素材

- **App Icon**：512x512 PNG（32 位元）
- **Feature Graphic**：1024x500 PNG/JPG
- **Screenshots**：至少 2 張（手機、平板）
- **隱私權政策**：網頁連結
- **App 說明**：繁體中文

#### 3. 建立應用程式

```bash
1. 登入 Google Play Console
2. 建立應用程式
3. 填寫基本資訊：
   - 應用程式名稱：碳排放追蹤系統
   - 預設語言：繁體中文
   - 應用程式類型：應用程式
   - 免費/付費：免費
```

#### 4. 設定商店資訊

```
簡短說明（80字）：
社工訪視碳排放追蹤與管理系統，協助機構記錄、分析並減少交通碳排放。

完整說明（4000字）：
【功能特色】
✅ 訪視記錄管理
✅ 碳排放自動計算
✅ 統計報表分析
✅ 多種交通工具支援
✅ 視覺化儀表板

【適用對象】
- 社福機構社工
- 長照服務人員
- 環保管理人員

【主要功能】
1. 訪視記錄：快速記錄每次訪視的交通資訊
2. 碳排放計算：依據環保署係數自動計算
3. 統計分析：月度、年度碳排放統計
4. 視覺化報表：圖表呈現碳排放趨勢
5. 資料匯出：支援報表匯出功能
```

#### 5. 上傳 APK/AAB

```bash
# 建議使用 AAB 格式（Android App Bundle）
# 在 Android Studio 中：
Build > Generate Signed Bundle / APK > Android App Bundle

# 或使用指令
./gradlew bundleRelease
```

#### 6. 內容分級

```
填寫問卷，取得內容分級
通常會是：適合所有年齡
```

#### 7. 目標對象與內容

```
- 目標年齡層：18 歲以上
- 廣告：無廣告
- 應用程式內購：無
```

#### 8. 隱私權政策

```html
<!-- 建立簡單的隱私權政策頁面 -->
<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8" />
    <title>隱私權政策 - 碳排放追蹤系統</title>
  </head>
  <body>
    <h1>隱私權政策</h1>

    <h2>資料收集</h2>
    <p>本應用程式收集以下資料：</p>
    <ul>
      <li>訪視記錄（日期、地點、里程）</li>
      <li>社工資訊（編號、姓名）</li>
      <li>長者資訊（編號）</li>
    </ul>

    <h2>資料使用</h2>
    <p>收集的資料僅用於：</p>
    <ul>
      <li>碳排放計算與統計</li>
      <li>產生分析報表</li>
      <li>系統功能運作</li>
    </ul>

    <h2>資料安全</h2>
    <p>所有資料儲存於本地裝置或機構伺服器，不會傳送給第三方。</p>

    <h2>聯絡方式</h2>
    <p>Email: [your-email]</p>

    <p>最後更新：2024年11月</p>
  </body>
</html>
```

#### 9. 測試

```
1. 內部測試：上傳 APK 給內部測試人員
2. 封閉測試：邀請特定使用者測試
3. 開放測試：公開測試（可選）
4. 正式發布：通過審核後發布
```

---

## 💡 建議方案選擇

### 快速上架（1 週內）

**選擇：方案一（WebView）**

- 最快速
- 成本最低
- 適合驗證市場

### 最佳體驗（2-3 週）

**選擇：方案二（PWA + TWA）**

- 接近原生體驗
- 可離線使用
- 維護簡單
- **推薦！**

### 長期發展（1-2 月）

**選擇：方案三（React Native）**

- 完整原生功能
- 最佳效能
- 適合大規模使用

---

## 📋 檢查清單

### 上架前準備

- [ ] 完成 App 開發與測試
- [ ] 準備 App Icon 和截圖
- [ ] 撰寫 App 說明
- [ ] 建立隱私權政策頁面
- [ ] 註冊 Google Play 開發者帳號
- [ ] 生成簽署金鑰
- [ ] 建立 Release 版本
- [ ] 內部測試通過

### 上架流程

- [ ] 建立應用程式
- [ ] 填寫商店資訊
- [ ] 上傳 APK/AAB
- [ ] 設定內容分級
- [ ] 填寫目標對象
- [ ] 提供隱私權政策
- [ ] 提交審核
- [ ] 等待審核通過（通常 1-3 天）
- [ ] 正式發布

---

## 🔧 後端部署建議

### 選項 1：雲端伺服器

```bash
# 使用 Google Cloud Platform、AWS 或 Azure
# 部署 Flask 應用程式
# 設定 HTTPS（必須）
# 設定網域名稱
```

### 選項 2：內部伺服器

```bash
# 機構內部伺服器
# 設定固定 IP
# 設定防火牆規則
# 使用 VPN 連線
```

### 選項 3：Heroku（簡單）

```bash
# 免費方案可用於測試
heroku create carbon-tracking
git push heroku main
```

---

## 📞 需要協助？

如果你選擇了某個方案，我可以協助你：

1. 建立完整的專案結構
2. 撰寫所需的程式碼
3. 設定開發環境
4. 準備上架素材
5. 解決技術問題

**建議：先從方案二（PWA + TWA）開始，這是最平衡的選擇！**
