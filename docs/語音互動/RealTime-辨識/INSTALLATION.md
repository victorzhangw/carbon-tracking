# 即時語音互動系統安裝指南

## 1. 安裝依賴套件

```bash
pip install dashscope websocket-client flask-socketio
```

## 2. 設置環境變數

### Windows CMD

```cmd
set DASHSCOPE_API_KEY=your_api_key_here
```

### Windows PowerShell

```powershell
$env:DASHSCOPE_API_KEY="your_api_key_here"
```

### Linux/macOS

```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

## 3. 啟動服務

```bash
python app.py
```

## 4. 訪問頁面

### 閩南語版本（Roy）

```
http://localhost:5000/voice_interaction_realtime/roy
```

### 國語版本（Nofish）

```
http://localhost:5000/voice_interaction_realtime/nofish
```

## 5. 系統需求

- Python 3.8+
- 麥克風權限
- 現代瀏覽器（Chrome、Edge、Firefox）
- 穩定的網路連接

## 6. 故障排除

### 問題：無法訪問麥克風

**解決方案**：

- 確保瀏覽器有麥克風權限
- 使用 HTTPS 或 localhost

### 問題：WebSocket 連接失敗

**解決方案**：

- 確保 flask-socketio 已安裝
- 檢查防火牆設置
- 確認服務器正常運行

### 問題：ASR 辨識失敗

**解決方案**：

- 確認 DASHSCOPE_API_KEY 已正確設置
- 檢查 API 配額
- 確保網路連接穩定

### 問題：TTS 語音無法播放

**解決方案**：

- 檢查瀏覽器音頻權限
- 確認音量設置
- 查看瀏覽器控制台錯誤訊息

## 7. 開發模式

如果需要調試，可以啟用 DEBUG 模式：

```bash
set DEBUG=True
python app.py
```

## 8. 技術支援

如遇到問題，請檢查：

1. 瀏覽器控制台（F12）
2. 服務器日誌
3. 網路連接狀態
