# 🎤 TTS 語音播放修復說明

## 📋 問題診斷

### 已發現的問題

1. ✅ **GPT-SoVITS Python 環境衝突** - 已修復（添加 `-s` 參數）
2. ✅ **參考音頻路徑錯誤** - 已修復（更新為 `TTS/vc.wav`）
3. ✅ **genvoice 目錄缺失** - 已修復（添加到 `ensure_directories()`）
4. ✅ **Flask 靜態文件路由缺失** - 已修復（添加 `/genvoice/<filename>` 路由）

### 測試結果

- ✅ GPT-SoVITS API 正常工作（端口 9880）
- ✅ TTS 音頻文件成功生成（genvoice 目錄）
- ✅ Flask API `/api/generate-tts` 正常返回
- ⚠️ **需要重啟 Flask 服務器**以應用靜態文件路由

## 🔧 已修改的文件

### 1. bStart.bat

```batch
# 添加 -s 參數避免 Python 環境衝突
runtime\python.exe -s api_v2.py -a 127.0.0.1 -p 9880 ...
```

### 2. services/tts.py

```python
# 修正參考音頻路徑
self.default_ref_audio = "TTS/vc.wav"  # 相對於 GPT-SoVITS 運行目錄
```

### 3. config.py

```python
def ensure_directories():
    directories = [
        'assets/audio/mockvoice',
        'assets/audio/genvoice',
        'static/audio',
        AUDIO_UPLOAD_FOLDER,
        'genvoice'  # TTS 輸出目錄
    ]
```

### 4. app.py

```python
# 添加 genvoice 靜態文件路由
@app.route('/genvoice/<path:filename>')
def serve_genvoice(filename):
    from flask import send_from_directory
    return send_from_directory('genvoice', filename)
```

## 🚀 重啟步驟

### 方法 1：使用 bStart.bat（推薦）

```batch
bStart.bat
```

這會自動：

1. 停止舊的 Flask 和 GPT-SoVITS 服務
2. 使用修復後的配置重新啟動
3. 自動創建 genvoice 目錄
4. GPT-SoVITS 使用隔離的 Python 環境

### 方法 2：手動重啟

1. 關閉當前的 Flask 服務器窗口
2. 關閉當前的 GPT-SoVITS 服務器窗口
3. 執行 `bStart.bat`

## ✅ 驗證步驟

重啟後，請驗證以下功能：

### 1. 檢查服務狀態

```powershell
# 檢查 Flask（端口 5000）
netstat -ano | findstr ":5000"

# 檢查 GPT-SoVITS（端口 9880）
netstat -ano | findstr ":9880"
```

### 2. 測試 TTS API

訪問：http://localhost:5000/emotion-analysis

1. 點擊麥克風按鈕錄音
2. 說一句話（例如："你好，今天天氣很好"）
3. 停止錄音
4. 等待 AI 回應
5. **應該能聽到語音回應** 🔊

### 3. 檢查瀏覽器控制台

打開開發者工具（F12），查看 Console：

- ✅ 應該看到 "完整音頻 URL: http://localhost:5000/genvoice/tts_xxxxx.wav"
- ✅ 應該看到 "音頻可以播放"
- ✅ 應該看到 "開始播放 AI 語音回應"
- ❌ 不應該看到 404 錯誤

### 4. 檢查音頻文件

```powershell
# 查看生成的音頻文件
dir genvoice
```

應該看到新生成的 `tts_xxxxx.wav` 文件。

## 🐛 如果還是沒有聲音

### 檢查清單

1. **瀏覽器自動播放政策**

   - 某些瀏覽器會阻止自動播放音頻
   - 解決方法：先點擊頁面任意位置，再進行錄音

2. **音量設置**

   - 檢查系統音量
   - 檢查瀏覽器標籤頁是否靜音

3. **音頻文件路徑**

   - 打開瀏覽器開發者工具（F12）
   - 查看 Network 標籤
   - 找到 `/genvoice/tts_xxxxx.wav` 請求
   - 確認狀態碼是 200（不是 404）

4. **Flask 路由**

   - 確認 Flask 已重啟
   - 測試直接訪問：http://localhost:5000/genvoice/tts_1763713712.wav
   - 應該能下載音頻文件

5. **GPT-SoVITS 服務**
   - 確認 GPT-SoVITS 正在運行
   - 檢查 GPT-SoVITS 窗口是否有錯誤

## 📊 技術細節

### 音頻生成流程

```
用戶錄音
  → Flask /process_audio API
  → services/tts.py (generate_speech)
  → GPT-SoVITS API (http://127.0.0.1:9880/tts)
  → 保存到 genvoice/tts_xxxxx.wav
  → 返回 audio_url: /genvoice/tts_xxxxx.wav
  → 前端創建 Audio 對象
  → 播放音頻
```

### 關鍵配置

- **GPT-SoVITS 端口**: 9880
- **Flask 端口**: 5000
- **參考音頻**: GPT-SoVITS-v2pro-20250604/TTS/vc.wav
- **輸出目錄**: genvoice/
- **音頻格式**: WAV
- **播放速度**: 0.55x（較慢，更清晰）

## 🎉 預期結果

重啟後，情緒識別系統應該：

1. ✅ 正確識別語音
2. ✅ 分析情緒
3. ✅ 生成 AI 回應文字
4. ✅ **播放 AI 語音回應** 🔊
5. ✅ 顯示完整的對話歷史

---

**最後更新**: 2025-11-21  
**狀態**: 等待重啟驗證
