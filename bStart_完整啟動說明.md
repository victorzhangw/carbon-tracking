# bStart.bat 完整啟動說明

## 📋 修改內容

### 新增功能

`bStart.bat` 現在會自動啟動：

1. ✅ Flask 應用（端口 5000）
2. ✅ GPT-SoVITS WebUI（端口 9874，繁體中文）
3. ✅ GPT-SoVITS TTS API（端口 9880）

### 修改步驟

1. **清理 Python 緩存** - 確保使用最新代碼
2. **啟動 GPT-SoVITS WebUI** - 繁體中文，無 MIT 聲明
3. **啟動 GPT-SoVITS TTS API** - 用於語音合成
4. **啟動 Flask 應用** - 主應用

## 🚀 使用方式

### 一鍵啟動

```bash
bStart.bat
```

### 啟動流程

```
[1/5] 停止舊服務器
  ↓
[2/5] 清理 Python 緩存
  ↓
[3/5] 啟動 GPT-SoVITS WebUI (9874)
  ↓
[4/5] 啟動 GPT-SoVITS TTS API (9880)
  ↓
[5/5] 啟動 Flask 應用 (5000)
  ↓
自動開啟瀏覽器
```

## 📊 啟動的服務

| 服務               | 端口 | 窗口標題                    | 說明         |
| ------------------ | ---- | --------------------------- | ------------ |
| Flask Server       | 5000 | Flask Server                | 主應用       |
| GPT-SoVITS WebUI   | 9874 | GPT-SoVITS WebUI (繁體中文) | 訓練界面     |
| GPT-SoVITS TTS API | 9880 | GPT-SoVITS TTS API          | 語音合成 API |

## 🎯 訪問地址

### 主要入口

- **系統入口**: http://localhost:5000/portal
- **語音測試**: http://localhost:5000/voice-testing

### GPT-SoVITS

- **WebUI (訓練)**: http://localhost:9874
- **TTS API**: http://localhost:9880

### 點擊 TTS 訓練卡片

在 http://localhost:5000/voice-testing 點擊「TTS 語音合成訓練」：

1. 在新分頁開啟
2. 重定向到 http://localhost:9874
3. 顯示繁體中文界面
4. 無 MIT 聲明

## ✨ 特點

### 1. 自動清理緩存

```batch
if exist "GPT-SoVITS-v2pro-20250604\__pycache__" (
    rmdir /s /q "GPT-SoVITS-v2pro-20250604\__pycache__" 2>nul
)
if exist "GPT-SoVITS-v2pro-20250604\tools\__pycache__" (
    rmdir /s /q "GPT-SoVITS-v2pro-20250604\tools\__pycache__" 2>nul
)
```

### 2. 繁體中文 WebUI

```batch
start "GPT-SoVITS WebUI (繁體中文)" cmd /k "cd GPT-SoVITS-v2pro-20250604 && go-webui.bat"
```

`go-webui.bat` 使用 `zh_TW` 參數：

```batch
runtime\python.exe -I webui.py zh_TW
```

### 3. 停止舊服務

```batch
REM 停止 Flask (5000)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
REM 停止 GPT-SoVITS WebUI (9874)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9874 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
REM 停止 GPT-SoVITS TTS API (9880)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9880 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
```

## 🔍 啟動輸出

```
════════════════════════════════════════════════════════════
  🎧 AI 語音互動平台 - 完整啟動
════════════════════════════════════════════════════════════

[1/5] 停止舊服務器（如果有）...
   ✅ 完成

[2/5] 清理 GPT-SoVITS Python 緩存...
   ✅ 緩存已清理

[3/5] 啟動 GPT-SoVITS WebUI（端口 9874，繁體中文）...
   ✅ GPT-SoVITS WebUI 已啟動（繁體中文，無 MIT 聲明）

[4/5] 啟動 GPT-SoVITS TTS API（端口 9880）...
   ✅ GPT-SoVITS TTS API 已啟動

[5/5] 啟動 Flask 服務器（使用虛擬環境）...
   ✅ 完成

[完成] 打開系統入口頁面...

════════════════════════════════════════════════════════════
  🌐 系統已啟動！
════════════════════════════════════════════════════════════

  🚀 系統入口：
     http://localhost:5000/portal

  📱 可用模組：
     • AI 語音互動平台（含情緒識別系統）
     • 碳排放追蹤系統
     • 智慧語音關懷系統
     • AI 廣播劇系統

  🎤 GPT-SoVITS 服務：
     • WebUI (訓練): http://localhost:9874 (繁體中文)
     • TTS API: http://localhost:9880

  💡 使用說明：
     在入口頁面選擇您要使用的系統模組

  ⚠️  服務器在另外的窗口運行：
     • Flask Server (端口 5000)
     • GPT-SoVITS WebUI (端口 9874)
     • GPT-SoVITS TTS API (端口 9880)

  🛑 關閉對應窗口即可停止服務器

════════════════════════════════════════════════════════════
```

## 🎯 完整工作流程

### 1. 啟動系統

```bash
bStart.bat
```

### 2. 訪問語音測試

瀏覽器自動開啟 http://localhost:5000/portal
→ 點擊「語音測試訓練模組」
→ 進入 http://localhost:5000/voice-testing

### 3. 使用 TTS 訓練

點擊「TTS 語音合成訓練」卡片
→ 在新分頁開啟
→ 重定向到 http://localhost:9874
→ 顯示 GPT-SoVITS WebUI（繁體中文）

### 4. 確認效果

- ✅ 無 iframe（直接顯示 GPT-SoVITS）
- ✅ 繁體中文界面
- ✅ 頂部無 MIT 聲明
- ✅ 完整的訓練功能

## 📁 相關文件

```
項目根目錄/
├── bStart.bat                          # 完整啟動腳本（已修改）
├── GPT-SoVITS-v2pro-20250604/
│   ├── go-webui.bat                    # WebUI 啟動（zh_TW）
│   ├── webui.py                        # 主程式（已註釋 MIT）
│   ├── api_v2.py                       # TTS API
│   └── tools/
│       └── assets.py                   # 資源（已簡化）
├── routes/
│   └── gptsovits.py                    # 路由（重定向）
└── templates/
    └── voice_testing_hub.html          # 入口（新分頁）
```

## ⚠️ 注意事項

### 1. 虛擬環境

確保虛擬環境已創建：

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. GPT-SoVITS 目錄

確保 `GPT-SoVITS-v2pro-20250604` 目錄存在

### 3. 端口衝突

確保以下端口未被佔用：

- 5000 (Flask)
- 9874 (GPT-SoVITS WebUI)
- 9880 (GPT-SoVITS TTS API)

### 4. 窗口管理

每個服務在獨立窗口運行：

- 關閉窗口 = 停止服務
- 不要關閉窗口，除非要停止服務

## 🔧 故障排除

### 問題 1: GPT-SoVITS 未啟動

**檢查**: 是否存在 `GPT-SoVITS-v2pro-20250604\go-webui.bat`
**解決**: 確認目錄結構正確

### 問題 2: 仍然是簡體中文

**原因**: 緩存未清理或 `go-webui.bat` 未修改
**解決**:

1. 檢查 `go-webui.bat` 是否為 `zh_TW`
2. 手動刪除 `__pycache__` 目錄
3. 重新執行 `bStart.bat`

### 問題 3: 仍然有 MIT 聲明

**原因**: `webui.py` 或 `assets.py` 未修改
**解決**:

1. 執行 `python 驗證MIT聲明移除.py`
2. 確認修改正確
3. 重新執行 `bStart.bat`

### 問題 4: 端口被佔用

**錯誤**: `Address already in use`
**解決**:

```bash
# 查看佔用端口的進程
netstat -ano | findstr :5000
netstat -ano | findstr :9874
netstat -ano | findstr :9880

# 停止進程
taskkill /F /PID <PID>
```

## 📊 與其他啟動方式對比

| 啟動方式                 | Flask | GPT-SoVITS WebUI | GPT-SoVITS TTS | 清理緩存 |
| ------------------------ | ----- | ---------------- | -------------- | -------- |
| `bStart.bat`             | ✅    | ✅               | ✅             | ✅       |
| `完整重啟GPT-SoVITS.bat` | ✅    | ✅               | ❌             | ✅       |
| 手動啟動                 | ✅    | ❌               | ❌             | ❌       |

**推薦**: 使用 `bStart.bat` 一鍵啟動所有服務！

## 🎉 總結

現在 `bStart.bat` 是完整的一鍵啟動腳本：

1. ✅ 自動清理緩存
2. ✅ 啟動 GPT-SoVITS WebUI（繁體中文）
3. ✅ 啟動 GPT-SoVITS TTS API
4. ✅ 啟動 Flask 應用
5. ✅ 自動開啟瀏覽器

只需執行 `bStart.bat`，所有服務都會正確啟動！✨
