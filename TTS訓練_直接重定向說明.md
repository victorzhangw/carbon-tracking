# TTS 訓練 - 直接重定向到 GPT-SoVITS 說明

## 📋 最終修改

### 問題分析

用戶反映：

1. ❌ 還是有 iframe（`/tts-training` 頁面使用 iframe 載入 GPT-SoVITS）
2. ❌ 還是簡體中文（GPT-SoVITS 服務沒有重啟）
3. ❌ MIT 聲明還在（GPT-SoVITS 服務沒有重啟，使用舊代碼）

### 解決方案

**改為直接重定向到 GPT-SoVITS WebUI**

## 🔧 修改內容

### 1. 修改路由 ✅

**文件**: `routes/gptsovits.py`

**修改前**:

```python
@gptsovits_bp.route('/tts-training')
def tts_training():
    """TTS 語音合成訓練頁面"""
    # 啟動 GPT-SoVITS
    thread = threading.Thread(target=start_in_background, daemon=True)
    thread.start()

    # 返回中間頁面（包含 iframe）
    return render_template('tts_training.html')
```

**修改後**:

```python
from flask import Blueprint, render_template, jsonify, redirect

@gptsovits_bp.route('/tts-training')
def tts_training():
    """TTS 語音合成訓練頁面 - 直接重定向到 GPT-SoVITS WebUI"""
    # 啟動 GPT-SoVITS
    thread = threading.Thread(target=start_in_background, daemon=True)
    thread.start()

    # 直接重定向到 GPT-SoVITS WebUI
    return redirect('http://localhost:9874')
```

### 2. 清理 Python 緩存 ✅

```bash
# 刪除緩存目錄
GPT-SoVITS-v2pro-20250604/__pycache__
GPT-SoVITS-v2pro-20250604/tools/__pycache__
```

### 3. 重啟 GPT-SoVITS ✅

使用新的啟動腳本，確保：

- ✅ 使用繁體中文 (`zh_TW`)
- ✅ 移除 MIT 聲明
- ✅ 清理緩存

## 🎯 完整流程

### 用戶操作流程

```
1. 訪問 http://localhost:5000/voice-testing
   ↓
2. 點擊「TTS 語音合成訓練」卡片
   ↓
3. 在新分頁開啟 /tts-training
   ↓
4. Flask 後台啟動 GPT-SoVITS（如果未運行）
   ↓
5. 立即重定向到 http://localhost:9874
   ↓
6. 顯示 GPT-SoVITS WebUI（繁體中文，無 MIT 聲明）
```

### 技術流程

```
voice_testing_hub.html
  ↓ (點擊卡片)
<a href="/tts-training" target="_blank">
  ↓ (新分頁)
routes/gptsovits.py: /tts-training
  ↓ (啟動服務)
gptsovits_service.start()
  ↓ (重定向)
redirect('http://localhost:9874')
  ↓ (顯示)
GPT-SoVITS WebUI (繁體中文)
```

## ✨ 優點

### 1. 無 iframe

- ✅ 直接顯示 GPT-SoVITS WebUI
- ✅ 無嵌套頁面
- ✅ 完整的瀏覽器功能

### 2. 繁體中文

- ✅ 使用 `zh_TW` 語言設定
- ✅ 所有界面文字為繁體中文

### 3. 無 MIT 聲明

- ✅ `webui.py` 已註釋聲明
- ✅ `assets.py` 已簡化 `top_html`
- ✅ 清理 Python 緩存

### 4. 更簡潔

- ✅ 不需要中間頁面
- ✅ 不需要狀態檢查
- ✅ 不需要 iframe 管理

## 🚀 使用方式

### 自動化腳本（推薦）

```bash
完整重啟GPT-SoVITS.bat
```

這個腳本會：

1. 停止所有 GPT-SoVITS 進程
2. 清理 Python 緩存
3. 驗證修改（MIT 聲明 + 繁體中文）
4. 啟動 GPT-SoVITS（繁體中文）
5. 啟動 Flask 應用

### 手動步驟

```bash
# 1. 停止進程
taskkill /F /IM python.exe /FI "COMMANDLINE eq *webui.py*"

# 2. 清理緩存
cd GPT-SoVITS-v2pro-20250604
rmdir /s /q __pycache__
rmdir /s /q tools\__pycache__
cd ..

# 3. 啟動 GPT-SoVITS
cd GPT-SoVITS-v2pro-20250604
go-webui.bat
cd ..

# 4. 啟動 Flask
bStart.bat
```

## 🧪 驗證

### 1. 檢查修改

```bash
# 驗證 MIT 聲明移除
python 驗證MIT聲明移除.py

# 驗證繁體中文設定
python 驗證繁體中文設定.py
```

### 2. 測試流程

1. 訪問: http://localhost:5000/voice-testing
2. 點擊「TTS 語音合成訓練」卡片
3. 應該在新分頁開啟 http://localhost:9874
4. 檢查：
   - ✅ 無 iframe（直接顯示 GPT-SoVITS）
   - ✅ 繁體中文界面
   - ✅ 頂部無 MIT 聲明

### 3. 檢查界面文字

應該看到繁體中文：

- ✅ 「前置資料集獲取工具」
- ✅ 「UVR5 人聲伴奏分離」
- ✅ 「音頻切分工具」
- ✅ 「語音識別」

## 📊 對比

| 特性       | 之前（iframe）                      | 現在（重定向）           |
| ---------- | ----------------------------------- | ------------------------ |
| 頁面層級   | 3 層（hub → tts_training → iframe） | 2 層（hub → GPT-SoVITS） |
| iframe     | ✅ 有                               | ❌ 無                    |
| 中間頁面   | ✅ 有                               | ❌ 無                    |
| 狀態檢查   | ✅ 需要                             | ❌ 不需要                |
| 載入動畫   | ✅ 有                               | ❌ 無（直接顯示）        |
| 代碼複雜度 | 高                                  | 低                       |
| 用戶體驗   | 較複雜                              | 簡單直接                 |

## ⚠️ 注意事項

### 1. GPT-SoVITS 必須重啟

修改 `webui.py`、`assets.py` 或 `go-webui.bat` 後，必須：

- 停止現有進程
- 清理 Python 緩存
- 重新啟動

### 2. Python 緩存問題

Python 會緩存編譯後的代碼（`.pyc` 文件），如果不清理緩存：

- ❌ 修改不會生效
- ❌ 仍然使用舊代碼
- ❌ 仍然顯示 MIT 聲明

### 3. 語言設定

`go-webui.bat` 中的語言參數：

```batch
runtime\python.exe -I webui.py zh_TW
                                 ^^^^^ 必須是 zh_TW
```

### 4. 端口衝突

確保端口未被佔用：

- Flask: 5000
- GPT-SoVITS: 9874

## 🔍 故障排除

### 問題 1: 仍然顯示 MIT 聲明

**原因**: Python 緩存未清理
**解決**: 執行 `完整重啟GPT-SoVITS.bat`

### 問題 2: 仍然是簡體中文

**原因**: GPT-SoVITS 未重啟或語言設定錯誤
**解決**:

1. 檢查 `go-webui.bat` 是否為 `zh_TW`
2. 執行 `完整重啟GPT-SoVITS.bat`

### 問題 3: 重定向失敗

**原因**: GPT-SoVITS 服務未啟動
**解決**:

1. 手動啟動 GPT-SoVITS
2. 等待 20-30 秒
3. 重新訪問

### 問題 4: 仍然有 iframe

**原因**: Flask 應用未重啟
**解決**: 重啟 Flask 應用（`bStart.bat`）

## 📁 相關文件

```
項目根目錄/
├── routes/
│   └── gptsovits.py                    # 路由（已修改為重定向）
├── templates/
│   ├── voice_testing_hub.html          # 入口頁面（已修改為新分頁）
│   └── tts_training.html               # 中間頁面（不再使用）
├── GPT-SoVITS-v2pro-20250604/
│   ├── webui.py                        # 主程式（已註釋 MIT 聲明）
│   ├── webui.py.backup                 # 備份
│   ├── go-webui.bat                    # 啟動腳本（已改為 zh_TW）
│   ├── go-webui.bat.backup             # 備份
│   └── tools/
│       ├── assets.py                   # 資源（已簡化 top_html）
│       └── assets.py.backup            # 備份
├── 完整重啟GPT-SoVITS.bat              # 自動化重啟腳本
├── 驗證MIT聲明移除.py                   # 驗證腳本
└── 驗證繁體中文設定.py                  # 驗證腳本
```

## 📅 修改記錄

- **日期**: 2025-11-22
- **修改者**: Kiro AI Assistant
- **修改原因**:
  1. 移除 iframe
  2. 確保繁體中文
  3. 確保移除 MIT 聲明
- **修改文件**:
  - `routes/gptsovits.py` (改為重定向)
  - `GPT-SoVITS-v2pro-20250604/webui.py` (註釋 MIT 聲明)
  - `GPT-SoVITS-v2pro-20250604/tools/assets.py` (簡化 top_html)
  - `GPT-SoVITS-v2pro-20250604/go-webui.bat` (改為 zh_TW)
- **測試狀態**: ⏳ 待用戶測試

## 🎯 最終效果

點擊「TTS 語音合成訓練」後：

1. ✅ 在新分頁開啟
2. ✅ 直接顯示 GPT-SoVITS WebUI（無 iframe）
3. ✅ 繁體中文界面
4. ✅ 頂部無 MIT 聲明
5. ✅ 完整的 GPT-SoVITS 功能

這是最簡潔、最直接的解決方案！✨
