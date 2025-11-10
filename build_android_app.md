# 📱 建立 Android App (TWA) 完整指南

## ✅ 前置準備完成

已完成的 PWA 設定：

- ✅ manifest.json - PWA 配置檔
- ✅ sw.js - Service Worker
- ✅ pwa-register.js - PWA 註冊腳本
- ✅ Icons - 所有尺寸的圖示
- ✅ 所有 HTML 頁面已加入 PWA 支援

---

## 🚀 方法一：使用 Bubblewrap（推薦）

### Step 1: 安裝 Node.js

```bash
# 下載並安裝 Node.js 18+
https://nodejs.org/
```

### Step 2: 安裝 Bubblewrap CLI

```bash
npm install -g @bubblewrap/cli
```

### Step 3: 安裝 JDK 17

```bash
# 下載並安裝 JDK 17
https://www.oracle.com/java/technologies/downloads/#java17

# 設定環境變數
JAVA_HOME=C:\Program Files\Java\jdk-17
```

### Step 4: 安裝 Android SDK

```bash
# 方法 A: 安裝 Android Studio（推薦）
https://developer.android.com/studio

# 方法 B: 只安裝 Command Line Tools
https://developer.android.com/studio#command-tools

# 設定環境變數
ANDROID_HOME=C:\Users\你的使用者名稱\AppData\Local\Android\Sdk
```

### Step 5: 部署後端到雲端

**重要：TWA 需要 HTTPS 網址！**

#### 選項 A: 使用 Heroku（免費）

```bash
# 安裝 Heroku CLI
https://devcenter.heroku.com/articles/heroku-cli

# 登入
heroku login

# 建立應用程式
heroku create carbon-tracking-app

# 部署
git push heroku main

# 你的網址：https://carbon-tracking-app.herokuapp.com
```

#### 選項 B: 使用 Render（免費）

```bash
# 1. 註冊 Render: https://render.com
# 2. 連接 GitHub repository
# 3. 選擇 Web Service
# 4. 設定：
#    - Build Command: pip install -r requirements.txt
#    - Start Command: python app.py
# 5. 部署完成後獲得 HTTPS 網址
```

#### 選項 C: 使用 Railway（免費）

```bash
# 1. 註冊 Railway: https://railway.app
# 2. New Project > Deploy from GitHub
# 3. 選擇你的 repository
# 4. 自動部署並獲得 HTTPS 網址
```

### Step 6: 初始化 TWA 專案

```bash
# 替換成你的實際網址
bubblewrap init --manifest https://your-domain.com/static/manifest.json
```

系統會詢問以下資訊：

```
? Domain being opened in the TWA: your-domain.com
? Name of the application: 碳排放追蹤系統
? Short name of the application: 碳追蹤
? Color for the status bar: #689F38
? Color for the splash screen: #F1F8E9
? Display mode: standalone
? Orientation: portrait
? Icon URL: https://your-domain.com/static/icons/icon-512x512.png
? Maskable Icon URL: https://your-domain.com/static/icons/icon-512x512.png
? Package ID: com.yourcompany.carbontracking
? Include app shortcuts: Yes
```

### Step 7: 建立簽署金鑰

```bash
# 生成金鑰庫
keytool -genkey -v -keystore carbon-tracking.keystore -alias carbon -keyalg RSA -keysize 2048 -validity 10000

# 系統會詢問：
# - 密碼（記住它！）
# - 姓名
# - 組織單位
# - 組織
# - 城市
# - 省份
# - 國家代碼（TW）
```

### Step 8: 建立 APK

```bash
# 建立 Debug 版本（測試用）
bubblewrap build

# 建立 Release 版本（上架用）
bubblewrap build --signingKeyPath carbon-tracking.keystore --signingKeyAlias carbon
```

### Step 9: 測試 APK

```bash
# 安裝到手機
adb install app-release-signed.apk

# 或直接複製 APK 到手機安裝
```

---

## 🚀 方法二：使用 PWABuilder（最簡單）

### Step 1: 訪問 PWABuilder

```
https://www.pwabuilder.com/
```

### Step 2: 輸入網址

```
輸入你的 PWA 網址：https://your-domain.com/carbon/
```

### Step 3: 下載 Android Package

```
1. 點擊 "Package For Stores"
2. 選擇 "Android"
3. 填寫資訊：
   - Package ID: com.yourcompany.carbontracking
   - App name: 碳排放追蹤系統
   - Launcher name: 碳追蹤
   - Theme color: #689F38
   - Background color: #F1F8E9
4. 點擊 "Generate"
5. 下載 APK 或 AAB
```

---

## 📦 上架 Google Play

### Step 1: 註冊開發者帳號

```
1. 訪問：https://play.google.com/console
2. 支付 $25 USD 註冊費
3. 填寫開發者資訊
```

### Step 2: 建立應用程式

```
1. 點擊 "建立應用程式"
2. 填寫：
   - 應用程式名稱：碳排放追蹤系統
   - 預設語言：繁體中文
   - 應用程式類型：應用程式
   - 免費/付費：免費
```

### Step 3: 準備商店資訊

#### 應用程式圖示

```
尺寸：512x512 PNG
已生成：static/icons/icon-512x512.png
```

#### Feature Graphic

```
尺寸：1024x500 PNG/JPG
建議使用設計工具製作，包含：
- App 名稱
- 簡短標語
- 視覺元素
```

#### 螢幕截圖

```
至少 2 張，建議 4-8 張
尺寸：1080x1920 或 1080x2340
內容：
- 首頁
- 儀表板
- 訪視記錄
- 新增記錄
- 統計報表
```

#### 應用程式說明

```
簡短說明（80字）：
社工訪視碳排放追蹤與管理系統，協助機構記錄、分析並減少交通碳排放，支援多種交通工具，自動計算碳排放量。

完整說明（4000字）：
【功能特色】
✅ 訪視記錄管理 - 快速記錄每次訪視的交通資訊
✅ 碳排放自動計算 - 依據環保署係數自動計算
✅ 統計報表分析 - 月度、年度碳排放統計
✅ 視覺化儀表板 - 圖表呈現碳排放趨勢
✅ 多種交通工具 - 支援機車、汽車、大眾運輸
✅ 離線功能 - 無網路時也能使用

【適用對象】
- 社福機構社工人員
- 長照服務人員
- 環保管理人員
- 需要追蹤碳排放的組織

【主要功能】
1. 訪視記錄
   - 記錄訪視日期、類型
   - 記錄社工和長者資訊
   - 記錄交通工具和里程
   - 自動計算碳排放量

2. 儀表板
   - 總體統計數據
   - 月度趨勢圖表
   - 交通工具分布
   - 碳排放分析

3. 統計報表
   - 月度統計明細
   - 交通工具統計
   - 資料匯出功能
   - 多維度分析

4. 資料管理
   - 分頁瀏覽記錄
   - 搜尋和篩選
   - 資料備份
   - 安全保護

【技術特點】
- PWA 技術，可離線使用
- 響應式設計，支援各種螢幕
- 快速載入，流暢體驗
- 資料本地儲存，保護隱私

【環保理念】
本系統協助機構：
- 追蹤和分析碳排放
- 發現減碳機會
- 優化訪視路線
- 促進環保意識
- 達成減碳目標

【支援與回饋】
Email: your-email@example.com
網站: https://your-domain.com
```

### Step 4: 設定內容分級

```
1. 填寫內容分級問卷
2. 通常會得到：適合所有年齡
```

### Step 5: 設定目標對象

```
- 目標年齡層：18 歲以上
- 廣告：無廣告
- 應用程式內購：無
```

### Step 6: 建立隱私權政策

```html
<!-- 建立 privacy.html 並上傳到你的網站 -->
<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>隱私權政策 - 碳排放追蹤系統</title>
    <style>
      body {
        font-family: "Microsoft JhengHei", Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        line-height: 1.6;
      }
      h1 {
        color: #689f38;
      }
      h2 {
        color: #7cb342;
        margin-top: 30px;
      }
    </style>
  </head>
  <body>
    <h1>隱私權政策</h1>
    <p>最後更新：2024年11月</p>

    <h2>1. 資料收集</h2>
    <p>本應用程式收集以下資料：</p>
    <ul>
      <li>訪視記錄（日期、地點、里程）</li>
      <li>社工資訊（編號、姓名）</li>
      <li>長者資訊（編號）</li>
      <li>交通工具類型</li>
      <li>碳排放計算結果</li>
    </ul>

    <h2>2. 資料使用</h2>
    <p>收集的資料僅用於：</p>
    <ul>
      <li>碳排放計算與統計</li>
      <li>產生分析報表</li>
      <li>系統功能運作</li>
      <li>改善服務品質</li>
    </ul>

    <h2>3. 資料儲存</h2>
    <p>所有資料儲存於：</p>
    <ul>
      <li>本地裝置（離線模式）</li>
      <li>機構伺服器（線上模式）</li>
      <li>不會傳送給第三方</li>
    </ul>

    <h2>4. 資料安全</h2>
    <p>我們採取以下措施保護您的資料：</p>
    <ul>
      <li>HTTPS 加密傳輸</li>
      <li>資料庫加密儲存</li>
      <li>存取權限控制</li>
      <li>定期安全更新</li>
    </ul>

    <h2>5. 使用者權利</h2>
    <p>您有權：</p>
    <ul>
      <li>查看您的資料</li>
      <li>修改您的資料</li>
      <li>刪除您的資料</li>
      <li>匯出您的資料</li>
    </ul>

    <h2>6. Cookie 使用</h2>
    <p>本應用程式使用 Cookie 用於：</p>
    <ul>
      <li>維持登入狀態</li>
      <li>儲存使用者偏好</li>
      <li>改善使用體驗</li>
    </ul>

    <h2>7. 第三方服務</h2>
    <p>本應用程式不使用任何第三方追蹤或分析服務。</p>

    <h2>8. 兒童隱私</h2>
    <p>本應用程式不針對 13 歲以下兒童，不會故意收集兒童的個人資訊。</p>

    <h2>9. 政策變更</h2>
    <p>我們可能會更新本隱私權政策。重大變更時會在應用程式中通知您。</p>

    <h2>10. 聯絡方式</h2>
    <p>如有任何問題，請聯絡：</p>
    <ul>
      <li>Email: your-email@example.com</li>
      <li>網站: https://your-domain.com</li>
    </ul>
  </body>
</html>
```

### Step 7: 上傳 APK/AAB

```
1. 進入 "正式版" > "建立新版本"
2. 上傳 app-release-signed.aab（推薦）或 .apk
3. 填寫版本資訊：
   - 版本名稱：1.0.0
   - 版本說明：首次發布
4. 儲存並提交審核
```

### Step 8: 等待審核

```
審核時間：通常 1-3 天
審核通過後即可發布
```

---

## 🔧 測試清單

### PWA 功能測試

- [ ] 可以安裝到主畫面
- [ ] 離線時可以開啟
- [ ] Service Worker 正常運作
- [ ] 快取策略正確
- [ ] 圖示顯示正確

### Android App 測試

- [ ] 安裝成功
- [ ] 啟動正常
- [ ] 所有頁面可訪問
- [ ] API 呼叫正常
- [ ] 返回鍵正常
- [ ] 旋轉螢幕正常
- [ ] 通知權限正常

### 效能測試

- [ ] 載入速度快
- [ ] 切換頁面流暢
- [ ] 記憶體使用正常
- [ ] 電池消耗正常

---

## 📝 常見問題

### Q: 為什麼需要 HTTPS？

A: TWA 要求網站必須使用 HTTPS，這是 Google 的安全要求。

### Q: 可以使用 localhost 測試嗎？

A: 開發時可以，但上架必須使用真實的 HTTPS 網址。

### Q: APK 和 AAB 有什麼差別？

A: AAB 是 Google Play 推薦的格式，檔案更小，支援動態功能。

### Q: 審核被拒絕怎麼辦？

A: 查看拒絕原因，修正後重新提交。常見原因：

- 隱私權政策不完整
- 圖示不符合規範
- 功能描述不清楚
- 缺少必要權限說明

### Q: 如何更新 App？

A: 修改程式碼後，增加版本號，重新建立 APK/AAB 並上傳。

---

## 🎉 完成！

完成以上步驟後，你的碳排放追蹤系統就可以在 Google Play 上架了！

需要協助？隨時詢問！
