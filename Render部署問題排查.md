# 🔧 Render 部署問題排查

## 🚨 當前狀態

測試顯示 502 錯誤，這表示服務可能：

1. 正在啟動中（首次部署需要時間）
2. 部署失敗
3. 應用程式啟動失敗

## 📋 立即檢查步驟

### Step 1: 檢查 Render Dashboard

1. **訪問 Render Dashboard**

   - 前往：https://dashboard.render.com
   - 登入你的帳號

2. **查看服務狀態**

   - 找到 `carbon-tracking` 服務
   - 查看狀態指示器：
     - 🟢 綠色 = 運行中
     - 🟡 黃色 = 部署中
     - 🔴 紅色 = 失敗

3. **查看部署日誌**
   - 點擊服務名稱
   - 點擊 "Logs" 標籤
   - 查看最新的日誌訊息

### Step 2: 常見問題與解決方案

#### 問題 A: 部署中（黃色）

**症狀：** 狀態顯示 "Deploying" 或 "Building"

**解決：**

- 等待 5-10 分鐘
- 首次部署需要安裝所有套件
- 完成後會自動變成綠色

#### 問題 B: 啟動失敗（紅色）

**症狀：** 日誌顯示錯誤訊息

**可能原因 1：套件安裝失敗**

```
錯誤訊息：ERROR: Could not find a version...
解決：檢查 requirements.txt 中的套件版本
```

**可能原因 2：缺少依賴**

```
錯誤訊息：ModuleNotFoundError: No module named...
解決：確認所有必要套件都在 requirements.txt 中
```

**可能原因 3：資料庫初始化失敗**

```
錯誤訊息：database error...
解決：Render 的檔案系統是臨時的，需要使用外部資料庫
```

#### 問題 C: 套件太多導致記憶體不足

**症狀：** 日誌顯示 "Out of memory" 或建置超時

**解決：** 簡化 requirements.txt

### Step 3: 簡化 requirements.txt（如果需要）

目前的 requirements.txt 包含很多不需要的套件（ASR、情緒識別等）。

建立一個最小化版本：

```txt
# 最小化版本 - 只包含碳排放系統需要的套件
Flask==3.1.0
Flask-Cors==5.0.0
openpyxl==3.1.5
Werkzeug==3.1.3
```

## 🔍 診斷步驟

### 1. 查看 Render 日誌

在 Render Dashboard 的 Logs 中，尋找：

**成功的訊息：**

```
✅ 應用程序初始化成功
正在啟動 Flask 服務器...
服務器將在 http://0.0.0.0:5000 上運行
```

**失敗的訊息：**

```
❌ 啟動失敗: ...
ModuleNotFoundError: ...
ERROR: ...
```

### 2. 檢查環境變數

確認 Render 設定：

- PORT: 應該自動設定
- PYTHON_VERSION: 3.10.0

### 3. 檢查啟動命令

在 Render Dashboard > Settings 中確認：

```
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

## 🛠️ 解決方案

### 方案 A: 等待部署完成

如果是首次部署，可能需要 10-15 分鐘。

### 方案 B: 簡化 requirements.txt

1. 建立最小化版本（見上方）
2. 提交並推送：

```bash
git add requirements.txt
git commit -m "簡化 requirements.txt 用於部署"
git push
```

3. Render 會自動重新部署

### 方案 C: 使用 Render 的 PostgreSQL

如果資料庫是問題：

1. 在 Render 建立 PostgreSQL 資料庫
2. 更新 app.py 使用環境變數中的資料庫 URL
3. 重新部署

### 方案 D: 檢查 app.py 的資料庫路徑

確認 `database_carbon_tracking.py` 中的資料庫路徑：

```python
# 應該使用相對路徑或環境變數
DATABASE = os.environ.get('DATABASE_PATH', 'customer_service.db')
```

## 📞 下一步行動

### 立即行動：

1. **訪問 Render Dashboard**

   - https://dashboard.render.com
   - 查看服務狀態和日誌

2. **截圖日誌**

   - 如果有錯誤訊息，截圖給我
   - 我可以協助診斷

3. **等待或修復**
   - 如果正在部署：等待完成
   - 如果失敗：根據錯誤訊息修復

### 如果需要協助：

告訴我：

- Render Dashboard 顯示的狀態
- 日誌中的錯誤訊息
- 我會協助你解決

## 💡 臨時方案

在修復 Render 部署的同時，你可以：

### 選項 1: 本地測試 Android App

```bash
# 啟動本地伺服器
python app.py

# 修改 MainActivity.kt 使用本地網址
# private val SERVER_URL = "http://10.0.2.2:5000/carbon/"

# 建置並測試 APK
```

### 選項 2: 使用其他部署平台

- Heroku
- Railway
- PythonAnywhere
- Vercel

## 🎯 目標

讓 Render 部署成功運行，然後：

1. ✅ 測試網站功能
2. 📱 建置 Android APK
3. 🚀 準備上架

**不要擔心，我們會解決這個問題！** 💪
