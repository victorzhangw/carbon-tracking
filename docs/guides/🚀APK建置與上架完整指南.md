# 🚀 APK 建置與上架完整指南

## 📋 目錄

1. [前置準備](#前置準備)
2. [部署後端到雲端](#部署後端到雲端)
3. [建置 APK](#建置-apk)
4. [測試 APK](#測試-apk)
5. [準備上架素材](#準備上架素材)
6. [上架 Google Play](#上架-google-play)

---

## 🎯 前置準備

### 必要工具清單

```
✅ Android Studio（已有專案）
✅ JDK 11+
✅ Android SDK
⏳ 雲端伺服器帳號（Heroku/Render/Railway）
⏳ Google Play 開發者帳號（$25 USD）
```

### 檢查清單

- [x] Android 專案已建立（android_app/）
- [x] 所有功能已完成
- [x] PWA 已設定
- [ ] 後端已部署到 HTTPS
- [ ] APK 已建置
- [ ] 上架素材已準備

---

## 🌐 Step 1: 部署後端到雲端

### 為什麼需要部署？

```
Android App 需要連接到 HTTPS 網址
本地的 http://localhost:5000 無法在手機上使用
必須部署到有 HTTPS 的雲端伺服器
```

### 方案選擇

#### 🎯 推薦：Render（免費、簡單）

**優點：**

- ✅ 完全免費
- ✅ 自動 HTTPS
- ✅ 支援 Python
- ✅ 自動部署
- ✅ 無需信用卡

**步驟：**

1. **註冊 Render**

   ```
   訪問：https://render.com
   使用 GitHub 帳號註冊
   ```

2. **準備部署檔案**

   建立 `config/requirements/base.txt`：

   ```txt
   Flask==3.0.0
   Flask-CORS==4.0.0
   Flask-JWT-Extended==4.5.3
   openpyxl==3.1.5
   ```

   建立 `config/deployment/render.yaml`：

   ```yaml
   services:
     - type: web
       name: carbon-tracking
       env: python
       buildCommand: pip install -r config/requirements/base.txt
       startCommand: python app.py
       envVars:
         - key: PYTHON_VERSION
           value: 3.10.0
   ```

   修改 `app.py` 最後幾行：

   ```python
   if __name__ == '__main__':
       import os
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port)
   ```

3. **部署到 Render**
   ```
   1. 登入 Render Dashboard
   2. 點擊 "New +" > "Web Service"
   3. 連接 GitHub repository
   4. 設定：
      - Name: carbon-tracking
      - Environment: Python 3
      - Build Command: pip install -r config/requirements/base.txt
      - Start Command: python app.py
   5. 點擊 "Create Web Service"
   6. 等待部署完成（約 5 分鐘）
   7. 獲得網址：https://carbon-tracking.onrender.com
   ```

#### 備選：Heroku（需信用卡驗證）

**步驟：**

```bash
# 1. 安裝 Heroku CLI
https://devcenter.heroku.com/articles/heroku-cli

# 2. 登入
heroku login

# 3. 建立應用程式
heroku create carbon-tracking-app

# 4. 建立 Procfile
echo "web: python app.py" > Procfile

# 5. 部署
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 6. 獲得網址
https://carbon-tracking-app.herokuapp.com
```

#### 備選：Railway（簡單快速）

**步驟：**

```
1. 訪問：https://railway.app
2. 使用 GitHub 登入
3. New Project > Deploy from GitHub
4. 選擇你的 repository
5. 自動偵測 Python 並部署
6. 獲得網址：https://carbon-tracking.up.railway.app
```

---

## 📱 Step 2: 建置 APK

### 2.1 更新後端網址

編輯 `android_app/app/src/main/java/com/carbontracking/app/MainActivity.kt`：

```kotlin
// 第 24 行左右
// 將本地網址改為雲端網址
private val SERVER_URL = "https://carbon-tracking.onrender.com/carbon/"
// 或你的實際網址
```

### 2.2 更新 App 資訊

編輯 `android_app/app/build.gradle`：

```gradle
android {
    defaultConfig {
        applicationId "com.carbontracking.app"
        minSdk 24
        targetSdk 34
        versionCode 1          // 版本號碼（整數）
        versionName "1.0.0"    // 版本名稱（字串）
    }
}
```

### 2.3 建立簽署金鑰

```bash
# 在 android_app 目錄執行
cd android_app

# 生成金鑰（Windows）
keytool -genkey -v -keystore carbon-tracking.keystore -alias carbon -keyalg RSA -keysize 2048 -validity 10000

# 輸入資訊：
密碼：[輸入並記住]
姓名：[你的姓名]
組織單位：[你的組織]
組織：[你的公司/學校]
城市：[你的城市]
省份：[你的省份]
國家代碼：TW

# 確認：是
```

**重要：妥善保管 carbon-tracking.keystore 和密碼！**

### 2.4 設定簽署

編輯 `android_app/app/build.gradle`：

```gradle
android {
    signingConfigs {
        release {
            storeFile file("../carbon-tracking.keystore")
            storePassword "你的密碼"
            keyAlias "carbon"
            keyPassword "你的密碼"
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 2.5 建置 Release APK

```bash
# 在 android_app 目錄

# Windows
gradlew.bat assembleRelease

# 建置完成後，APK 位置：
# app/build/outputs/apk/release/app-release.apk
```

### 2.6 建置 AAB（推薦用於上架）

```bash
# AAB 是 Google Play 推薦的格式

# Windows
gradlew.bat bundleRelease

# 建置完成後，AAB 位置：
# app/build/outputs/bundle/release/app-release.aab
```

---

## 🧪 Step 3: 測試 APK

### 3.1 安裝到手機

```bash
# 1. 啟用手機 USB 除錯
設定 > 關於手機 > 連點版本號 7 次
返回 > 開發人員選項 > USB 除錯

# 2. 連接手機到電腦

# 3. 安裝 APK
adb install app/build/outputs/apk/release/app-release.apk

# 或直接複製 APK 到手機安裝
```

### 3.2 測試清單

```
功能測試：
- [ ] App 成功啟動
- [ ] 首頁正常載入
- [ ] 可以導航到各頁面
- [ ] 可以新增記錄
- [ ] 可以編輯記錄
- [ ] 可以刪除記錄
- [ ] 可以搜尋篩選
- [ ] 可以匯出資料
- [ ] 統計圖表正常
- [ ] 返回鍵正常
- [ ] 旋轉螢幕正常

效能測試：
- [ ] 載入速度快（< 3 秒）
- [ ] 操作流暢
- [ ] 無閃退
- [ ] 記憶體使用正常
```

---

## 🎨 Step 4: 準備上架素材

### 4.1 App Icon（已完成）

```
✅ 512x512 PNG
位置：static/icons/icon-512x512.png
```

### 4.2 Feature Graphic（需製作）

**規格：**

- 尺寸：1024 x 500 px
- 格式：PNG 或 JPG
- 內容：App 名稱 + 標語 + 視覺元素

**製作工具：**

- Canva：https://www.canva.com
- Figma：https://www.figma.com
- Photoshop

**範例內容：**

```
┌────────────────────────────────────────┐
│                                        │
│  🌱 碳排放追蹤系統                      │
│                                        │
│  智能管理社工訪視碳排放                 │
│  環保、高效、專業                       │
│                                        │
│  [儀表板截圖] [記錄截圖] [統計截圖]     │
│                                        │
└────────────────────────────────────────┘
```

### 4.3 Screenshots（需截圖）

**規格：**

- 數量：至少 2 張，建議 4-8 張
- 尺寸：1080 x 1920 px（手機）或 1080 x 2340 px
- 格式：PNG 或 JPG

**建議截圖：**

1. 首頁（導航）
2. 儀表板（統計數據）
3. 訪視記錄列表
4. 新增記錄表單
5. 編輯記錄
6. 搜尋功能
7. 統計報表
8. 匯出功能

**截圖方法：**

```
1. 在手機上開啟 App
2. 導航到要截圖的頁面
3. 按電源鍵 + 音量下鍵
4. 傳到電腦
5. 調整尺寸為 1080 x 1920
```

### 4.4 應用程式說明

**簡短說明（80 字）：**

```
社工訪視碳排放追蹤與管理系統，協助機構記錄、分析並減少交通碳排放，支援多種交通工具，自動計算碳排放量，提供完整統計報表。
```

**完整說明（4000 字）：**

```
【碳排放追蹤系統】

專為社福機構設計的訪視碳排放管理工具

🌱 功能特色

✅ 訪視記錄管理
- 快速記錄每次訪視的交通資訊
- 支援編輯和刪除記錄
- 自動計算碳排放量
- 工號自動帶出姓名

✅ 智能搜尋與篩選
- 關鍵字快速搜尋
- 依社工、日期、交通工具篩選
- 組合條件查詢
- 即時顯示結果統計

✅ 統計報表分析
- 月度碳排放統計
- 交通工具使用分析
- 社工績效統計
- 視覺化圖表呈現

✅ 資料匯出功能
- 匯出 Excel 格式
- 匯出 CSV 格式
- 支援篩選結果匯出
- 完整資料備份

✅ 多種交通工具支援
- 🏍️ 機車（碳排放係數：0.0695）
- 🚗 汽車（碳排放係數：0.1850）
- 🚌 大眾運輸（碳排放係數：0.0295）

✅ 離線功能
- PWA 技術支援
- 離線瀏覽記錄
- 自動同步資料

🎯 適用對象

- 社福機構社工人員
- 長照服務人員
- 環保管理人員
- 需要追蹤碳排放的組織

📊 主要功能

1. 訪視記錄
   - 記錄訪視日期、類型
   - 記錄社工和長者資訊
   - 記錄交通工具和里程
   - 自動計算碳排放量
   - 編輯和刪除記錄

2. 儀表板
   - 總體統計數據
   - 月度趨勢圖表
   - 交通工具分布
   - 碳排放分析

3. 搜尋與篩選
   - 關鍵字搜尋
   - 社工篩選
   - 日期範圍篩選
   - 交通工具篩選
   - 組合條件查詢

4. 統計報表
   - 月度統計明細
   - 交通工具統計
   - 社工績效分析
   - 多維度分析

5. 資料匯出
   - Excel 格式匯出
   - CSV 格式匯出
   - 篩選結果匯出
   - 完整資料備份

💡 技術特點

- PWA 技術，可離線使用
- 響應式設計，支援各種螢幕
- 快速載入，流暢體驗
- 資料本地儲存，保護隱私
- 自動計算碳排放
- 即時統計分析

🌍 環保理念

本系統協助機構：
- 追蹤和分析碳排放
- 發現減碳機會
- 優化訪視路線
- 促進環保意識
- 達成減碳目標

📈 使用效益

- 提升記錄效率
- 減少紙本作業
- 即時數據分析
- 支援決策制定
- 促進環保行動

🔒 資料安全

- HTTPS 加密傳輸
- 本地資料儲存
- 權限控制管理
- 定期資料備份

📞 支援與回饋

Email: [your-email]
網站: [your-website]

版本：1.0.0
更新日期：2024年11月
```

### 4.5 隱私權政策

```
已準備：https://your-domain.com/privacy
或使用：templates/privacy_policy.html
```

---

## 🚀 Step 5: 上架 Google Play

### 5.1 註冊開發者帳號

```
1. 訪問：https://play.google.com/console
2. 使用 Google 帳號登入
3. 支付 $25 USD 註冊費（一次性）
4. 填寫開發者資訊
5. 同意開發者協議
```

### 5.2 建立應用程式

```
1. 登入 Google Play Console
2. 點擊「建立應用程式」
3. 填寫資訊：
   - 應用程式名稱：碳排放追蹤系統
   - 預設語言：繁體中文（台灣）
   - 應用程式類型：應用程式
   - 免費/付費：免費
4. 勾選聲明
5. 點擊「建立應用程式」
```

### 5.3 填寫商店資訊

**應用程式詳細資料：**

```
簡短說明：（見 4.4）
完整說明：（見 4.4）
```

**圖片素材：**

```
- App Icon：512x512（已有）
- Feature Graphic：1024x500（需製作）
- Screenshots：至少 2 張（需截圖）
```

**分類：**

```
應用程式類別：生產力工具
標記：環保、管理、記錄、統計
```

### 5.4 設定內容分級

```
1. 填寫內容分級問卷
2. 問題範例：
   - 是否包含暴力內容？否
   - 是否包含成人內容？否
   - 是否包含賭博內容？否
3. 提交問卷
4. 獲得分級：適合所有年齡
```

### 5.5 設定目標對象

```
目標年齡層：18 歲以上
廣告：無廣告
應用程式內購：無
```

### 5.6 隱私權政策

```
隱私權政策網址：
https://your-domain.com/privacy
```

### 5.7 上傳 AAB

```
1. 進入「正式版」
2. 點擊「建立新版本」
3. 上傳 app-release.aab
4. 填寫版本資訊：
   - 版本名稱：1.0.0
   - 版本說明：
     首次發布
     - 訪視記錄管理
     - 搜尋與篩選
     - 統計報表
     - 資料匯出
5. 儲存
```

### 5.8 提交審核

```
1. 檢查所有必填項目
2. 點擊「提交審核」
3. 等待審核（通常 1-3 天）
4. 審核通過後發布
```

---

## ✅ 檢查清單

### 部署前

- [ ] 所有功能已測試
- [ ] 後端已部署到 HTTPS
- [ ] 網址已更新到 MainActivity.kt
- [ ] 簽署金鑰已建立
- [ ] APK/AAB 已建置

### 上架前

- [ ] App Icon 已準備（512x512）
- [ ] Feature Graphic 已製作（1024x500）
- [ ] Screenshots 已截圖（至少 2 張）
- [ ] 應用程式說明已撰寫
- [ ] 隱私權政策已發布
- [ ] Google Play 開發者帳號已註冊

### 上架時

- [ ] 應用程式已建立
- [ ] 商店資訊已填寫
- [ ] 圖片素材已上傳
- [ ] 內容分級已完成
- [ ] 目標對象已設定
- [ ] 隱私權政策已提供
- [ ] AAB 已上傳
- [ ] 已提交審核

---

## 🎯 快速行動計畫

### 今天（2-3 小時）

1. ✅ 部署後端到 Render
2. ✅ 更新 MainActivity.kt 網址
3. ✅ 建立簽署金鑰
4. ✅ 建置 Release APK
5. ✅ 測試 APK

### 明天（2-3 小時）

6. ⏳ 製作 Feature Graphic
7. ⏳ 截取 Screenshots
8. ⏳ 撰寫應用程式說明
9. ⏳ 註冊 Google Play 開發者

### 後天（1-2 小時）

10. ⏳ 建立應用程式
11. ⏳ 填寫商店資訊
12. ⏳ 上傳素材
13. ⏳ 提交審核

### 3-5 天後

14. ⏳ 審核通過
15. ⏳ 正式發布！

---

## 💡 重要提示

### 必須使用 HTTPS

```
❌ http://localhost:5000
❌ http://10.0.2.2:5000
✅ https://carbon-tracking.onrender.com
```

### 妥善保管金鑰

```
⚠️ carbon-tracking.keystore 和密碼非常重要
⚠️ 遺失後無法更新 App
⚠️ 建議備份到雲端
```

### 審核時間

```
首次審核：通常 1-3 天
更新審核：通常 1-2 天
被拒絕：修正後重新提交
```

---

## 📞 需要協助？

如果遇到問題：

1. 檢查錯誤訊息
2. 查看 Logcat
3. 參考官方文件
4. 詢問我！

**準備好開始了嗎？讓我們一步步完成！** 🚀
