# 🚀 部署到 Render 完整指南

## 📋 前置準備

### 1. 確認檔案已準備好

- ✅ `config/requirements/base.txt` - Python 套件清單
- ✅ `config/deployment/render.yaml` - Render 部署設定
- ✅ `app.py` - 已更新支援環境變數

### 2. 準備 Git Repository

```bash
# 如果還沒有 git，先初始化
git init
git add .
git commit -m "準備部署碳排放追蹤系統"

# 推送到 GitHub
# 先在 GitHub 建立 repository: carbon-tracking
git remote add origin https://github.com/你的用戶名/carbon-tracking.git
git branch -M main
git push -u origin main
```

## 🌐 部署到 Render

### Step 1: 註冊 Render

1. 訪問：https://render.com
2. 點擊 "Get Started for Free"
3. 使用 GitHub 帳號註冊（推薦）

### Step 2: 建立 Web Service

1. 登入後，點擊右上角 "New +" 按鈕
2. 選擇 "Web Service"
3. 選擇 "Build and deploy from a Git repository"
4. 點擊 "Connect" 連接你的 GitHub 帳號
5. 選擇你的 repository（carbon-tracking）

### Step 3: 設定部署參數

```
Name: carbon-tracking
Environment: Python 3
Region: Singapore (最接近台灣)
Branch: main
Build Command: pip install -r config/requirements/base.txt
Start Command: python app.py
```

### Step 4: 選擇方案

- 選擇 "Free" 方案（適合測試）
- 注意：Free 方案會在 15 分鐘無活動後休眠

### Step 5: 環境變數設定（可選）

點擊 "Advanced" 可以設定：

```
DEBUG=False
PORT=5000
```

### Step 6: 開始部署

1. 點擊 "Create Web Service"
2. 等待部署（約 5-10 分鐘）
3. 觀察部署日誌，確認無錯誤

### Step 7: 獲取網址

部署完成後，你會獲得網址：

```
https://carbon-tracking.onrender.com
```

## ✅ 測試部署

### 1. 測試 API 端點

```bash
# 測試首頁
curl https://carbon-tracking.onrender.com/

# 測試碳排放 API
curl https://carbon-tracking.onrender.com/carbon/
```

### 2. 瀏覽器測試

訪問：https://carbon-tracking.onrender.com/carbon/

確認功能：

- ✅ 首頁載入正常
- ✅ 新增訪視記錄
- ✅ 查看統計資料
- ✅ 匯出 Excel

## 📱 更新 Android App

### 1. 更新 MainActivity.kt

已經更新為使用雲端網址：

```kotlin
private val SERVER_URL = "https://carbon-tracking.onrender.com/carbon/"
```

### 2. 建置 APK

```bash
cd android_app

# 建立簽署金鑰（只需執行一次）
keytool -genkey -v -keystore carbon-tracking.keystore -alias carbon -keyalg RSA -keysize 2048 -validity 10000

# 建置 Release APK
gradlew.bat assembleRelease

# APK 位置
# android_app/app/build/outputs/apk/release/app-release.apk
```

### 3. 安裝測試

```bash
# 連接手機後安裝
adb install app/build/outputs/apk/release/app-release.apk

# 測試所有功能
```

## 🔧 常見問題

### Q1: 部署失敗怎麼辦？

查看 Render 的部署日誌，常見問題：

- Python 版本不符：確認 `config/deployment/render.yaml` 中的版本
- 套件安裝失敗：檢查 `config/requirements/base.txt`
- 啟動失敗：確認 `app.py` 的 PORT 設定

### Q2: Free 方案的限制？

- 15 分鐘無活動會休眠
- 首次喚醒需要 30-60 秒
- 每月 750 小時免費運行時間

### Q3: 如何升級方案？

在 Render Dashboard 中：

1. 選擇你的 Service
2. 點擊 "Settings"
3. 選擇 "Instance Type"
4. 升級到 Starter ($7/月) 或更高方案

### Q4: 如何更新部署？

```bash
# 修改代碼後
git add .
git commit -m "更新功能"
git push

# Render 會自動重新部署
```

## 📊 監控與維護

### 查看日誌

在 Render Dashboard：

1. 選擇你的 Service
2. 點擊 "Logs" 標籤
3. 即時查看運行日誌

### 查看指標

- CPU 使用率
- 記憶體使用率
- 請求數量
- 回應時間

## 🎯 下一步

部署完成後：

1. ✅ 測試所有 API 功能
2. ✅ 建置並測試 Android APK
3. 📱 準備上架素材
4. 🚀 上架 Google Play

需要協助嗎？隨時問我！
