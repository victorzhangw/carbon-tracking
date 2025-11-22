# 即時語音互動系統

## 📋 系統概述

即時語音互動系統整合了三個核心技術：

1. **Qwen-ASR-Realtime**：即時語音辨識
2. **DeepSeek LLM**：智能對話處理
3. **Qwen TTS Realtime**：流式語音合成

## 🎯 功能特點

- ✅ 即時語音辨識（支援 VAD 自動斷句）
- ✅ 智能對話回應（使用專案既有 LLM）
- ✅ 流式語音輸出（降低延遲）
- ✅ 雙語支援（閩南語 Roy / 國語 Nofish）
- ✅ 多輪對話上下文管理
- ✅ 美觀的 UI 介面（橙色/藍色主題）

## 📁 文件結構

```
routes/
  └── voice_interaction_realtime.py          # Flask 路由

services/
  └── realtime_interaction_service.py        # 核心服務邏輯

templates/
  ├── voice_interaction_realtime_roy.html    # 閩南語版本
  └── voice_interaction_realtime_nofish.html # 國語版本

static/js/
  └── voice_interaction_realtime.js          # 前端邏輯

docs/語音互動/RealTime-辨識/
  ├── voice_interaction_realtime_spec.md     # 規格書
  ├── INSTALLATION.md                        # 安裝指南
  └── README.md                              # 本文件
```

## 🚀 快速開始

### 1. 安裝依賴套件

```bash
pip install flask-socketio dashscope websocket-client
```

### 2. 設置 API 密鑰

**Windows CMD:**

```cmd
set DASHSCOPE_API_KEY=your_api_key_here
```

**Windows PowerShell:**

```powershell
$env:DASHSCOPE_API_KEY="your_api_key_here"
```

**Linux/macOS:**

```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 運行測試腳本

```bash
python test_realtime_interaction.py
```

### 4. 啟動服務

```bash
python app.py
```

### 5. 訪問頁面

- **閩南語版（Roy）**: http://localhost:5000/voice_interaction_realtime/roy
- **國語版（Nofish）**: http://localhost:5000/voice_interaction_realtime/nofish

## 🎨 頁面特色

### 閩南語版本（Roy）

- 🟠 橙色主題（代表閩南文化）
- 🎤 Roy 語音角色
- 📍 路由：`/voice_interaction_realtime/roy`

### 國語版本（Nofish）

- 🔵 藍色主題（代表標準語言）
- 🎤 Nofish 語音角色
- 📍 路由：`/voice_interaction_realtime/nofish`

## 🔧 技術架構

### 後端

- **Flask**: Web 框架
- **Flask-SocketIO**: WebSocket 支援
- **dashscope**: Qwen API 客戶端
- **websocket-client**: WebSocket 客戶端

### 前端

- **Socket.IO**: 即時雙向通訊
- **Web Audio API**: 音頻處理與播放
- **MediaRecorder API**: 麥克風錄音

### 流程圖

```
用戶說話
  ↓
[麥克風] → PCM 16kHz
  ↓
[WebSocket] → 發送音頻
  ↓
[Qwen ASR] → 即時辨識
  ↓
[DeepSeek LLM] → 生成回應
  ↓
[Qwen TTS] → 流式合成
  ↓
[瀏覽器] → 播放語音
```

## 📊 效能指標

- **ASR 延遲**: < 500ms
- **LLM 延遲**: < 2s
- **TTS 延遲**: < 500ms（首字節）
- **端到端延遲**: < 3s
- **並發支援**: 10 個同時會話

## 🛠️ 故障排除

### 問題：路由 404

**解決方案**：

1. 確認已在 `app.py` 中註冊路由
2. 重啟服務器
3. 檢查 URL 是否正確

### 問題：無法連接 WebSocket

**解決方案**：

1. 確認 `flask-socketio` 已安裝
2. 檢查防火牆設置
3. 查看瀏覽器控制台錯誤

### 問題：麥克風無法訪問

**解決方案**：

1. 使用 HTTPS 或 localhost
2. 檢查瀏覽器權限設置
3. 確認麥克風硬體正常

### 問題：語音無法播放

**解決方案**：

1. 檢查音量設置
2. 確認瀏覽器音頻權限
3. 查看控制台錯誤訊息

## 📝 API 端點

### HTTP 端點

| 端點                                        | 方法 | 說明           |
| ------------------------------------------- | ---- | -------------- |
| `/voice_interaction_realtime/roy`           | GET  | 閩南語版本頁面 |
| `/voice_interaction_realtime/nofish`        | GET  | 國語版本頁面   |
| `/voice_interaction_realtime/session/start` | POST | 啟動會話       |
| `/voice_interaction_realtime/session/stop`  | POST | 結束會話       |

### WebSocket 事件

| 事件                 | 方向            | 說明         |
| -------------------- | --------------- | ------------ |
| `connect`            | Client → Server | 建立連接     |
| `join_session`       | Client → Server | 加入會話     |
| `audio_input`        | Client → Server | 發送音頻     |
| `transcript_partial` | Server → Client | 即時辨識結果 |
| `transcript_final`   | Server → Client | 最終辨識結果 |
| `llm_response`       | Server → Client | LLM 回應     |
| `audio_output`       | Server → Client | 語音輸出     |
| `error`              | Server → Client | 錯誤訊息     |

## 🔐 安全性

- ✅ API 密鑰不在前端暴露
- ✅ 會話隔離（每個用戶獨立）
- ✅ 資源限制（5 分鐘/會話）
- ✅ 錯誤日誌記錄

## 📚 相關文件

- [規格書](voice_interaction_realtime_spec.md)
- [安裝指南](INSTALLATION.md)
- [Sample.py](Sample.py) - Qwen ASR 範例
- [客戶端事件說明](实时语音识别（Qwen-ASR-Realtime）客户端事件.txt)
- [服務端事件說明](实时语音识别（Qwen-ASR-Realtime）服务端事件.txt)

## 🎓 使用範例

### 啟動會話（API）

```bash
curl -X POST http://localhost:5000/voice_interaction_realtime/session/start \
  -H "Content-Type: application/json" \
  -d '{"voice": "Roy", "enable_vad": true}'
```

### 結束會話（API）

```bash
curl -X POST http://localhost:5000/voice_interaction_realtime/session/stop \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id"}'
```

## 🤝 貢獻

如需改進或報告問題，請：

1. 查看規格書了解系統設計
2. 運行測試腳本驗證環境
3. 查看瀏覽器控制台和服務器日誌
4. 提供詳細的錯誤訊息

## 📞 技術支援

遇到問題時，請提供：

- 瀏覽器類型和版本
- 錯誤訊息（控制台 + 服務器）
- 操作步驟
- 系統環境（OS、Python 版本）

---

**版本**: 1.0.0  
**最後更新**: 2025-11-20  
**作者**: Kiro AI Assistant
