# 即時語音互動系統規格書

## 1. 系統概述

### 1.1 功能描述

實作即時語音互動系統 `voice_interaction_realtime`，整合以下三個核心功能：

1. **即時語音辨識（ASR）**：使用 Qwen-ASR-Realtime 進行即時語音轉文字
2. **LLM 對話處理**：使用專案既有的 DeepSeek LLM 進行對話分析與回應生成
3. **即時語音合成（TTS）**：使用 Qwen TTS 的 `qwen3-tts-flash-realtime` 模型進行流式語音輸出

### 1.2 技術架構

```
用戶語音輸入
  ↓
[Qwen-ASR-Realtime] 即時語音辨識（WebSocket）
  ↓
[DeepSeek LLM] 對話分析與回應生成
  ↓
[Qwen TTS Realtime] 流式語音合成（WebSocket）
  ↓
用戶語音輸出
```

## 2. 技術規格

### 2.1 ASR（語音辨識）

- **模型**：`qwen3-asr-flash-realtime`
- **連接方式**：WebSocket
- **端點**：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime`
- **輸入格式**：PCM 16kHz 單聲道
- **輸出**：即時文字流（stash + final transcript）

**關鍵事件**：

- 客戶端：`session.update`, `input_audio_buffer.append`, `input_audio_buffer.commit`
- 服務端：`conversation.item.input_audio_transcription.text`, `conversation.item.input_audio_transcription.completed`

### 2.2 LLM（對話處理）

- **模型**：DeepSeek-V3（透過 SiliconFlow API）
- **功能**：使用專案既有的 `services/ai.py` 中的 `analyze_and_respond_with_context` 函數
- **輸入**：辨識完成的文字
- **輸出**：JSON 格式 `{sentiment, response, confidence}`

### 2.3 TTS（語音合成）

- **模型**：`qwen3-tts-flash-realtime`（流式輸出）
- **連接方式**：WebSocket
- **端點**：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime`
- **輸入**：LLM 生成的回應文字
- **輸出**：即時音頻流（PCM 24kHz）

**語音角色**：

- **Roy**：閩南語版本（專用頁面）
- **Nofish**：國語版本（專用頁面）

**關鍵參數**：

- `voice`: "Roy"（閩南語）或 "Nofish"（國語）
- `speech_rate`: 0.8（適合長者的語速）
- `stream`: True（啟用流式輸出）

## 3. 模組設計

### 3.1 檔案結構

```
routes/
  └── voice_interaction_realtime.py    # Flask 路由（API 端點）

services/
  └── realtime_interaction_service.py  # 核心服務邏輯

templates/
  ├── voice_interaction_realtime_roy.html     # 閩南語版本（Roy）
  └── voice_interaction_realtime_nofish.html  # 國語版本（Nofish）

static/js/
  └── voice_interaction_realtime.js    # 前端 WebSocket 處理（共用）
```

### 3.2 核心類別：RealtimeInteractionService

```python
class RealtimeInteractionService:
    """即時語音互動服務"""

    def __init__(self, api_key):
        """初始化服務"""
        pass

    def start_asr_session(self):
        """啟動 ASR WebSocket 連接"""
        pass

    def start_tts_session(self):
        """啟動 TTS WebSocket 連接"""
        pass

    def process_audio_input(self, audio_chunk):
        """處理音頻輸入（發送到 ASR）"""
        pass

    def on_transcript_received(self, transcript):
        """處理辨識結果（觸發 LLM）"""
        pass

    def generate_llm_response(self, user_text, context):
        """生成 LLM 回應"""
        pass

    def synthesize_response(self, response_text):
        """合成回應語音（流式）"""
        pass

    def close_sessions(self):
        """關閉所有連接"""
        pass
```

## 4. API 端點設計

### 4.1 WebSocket 端點

```
/voice_interaction_realtime/ws
```

**功能**：雙向即時通訊

- 接收：客戶端音頻流
- 發送：辨識文字、LLM 回應、合成音頻流

**訊息格式**：

```json
// 客戶端 → 服務端（音頻輸入）
{
  "type": "audio_input",
  "audio": "<base64_encoded_pcm>",
  "timestamp": 1234567890
}

// 服務端 → 客戶端（辨識中）
{
  "type": "transcript_partial",
  "text": "你好",
  "stash": "我想問"
}

// 服務端 → 客戶端（辨識完成）
{
  "type": "transcript_final",
  "text": "你好我想問一個問題"
}

// 服務端 → 客戶端（LLM 回應）
{
  "type": "llm_response",
  "text": "您好！我很樂意幫助您...",
  "sentiment": "正面",
  "confidence": 0.95
}

// 服務端 → 客戶端（音頻輸出）
{
  "type": "audio_output",
  "audio": "<base64_encoded_pcm>",
  "is_final": false
}
```

### 4.2 HTTP 端點

#### 4.2.1 演示頁面

**閩南語版本（Roy）**

```
GET /voice_interaction_realtime/roy
```

返回：閩南語互動頁面（使用 Roy 語音）

**國語版本（Nofish）**

```
GET /voice_interaction_realtime/nofish
```

返回：國語互動頁面（使用 Nofish 語音）

#### 4.2.2 會話管理

```
POST /voice_interaction_realtime/session/start
```

**功能**：啟動新的即時互動會話

**請求**：

```json
{
  "language": "zh",
  "voice": "Roy", // 或 "Nofish"
  "speech_rate": 0.8,
  "enable_vad": true
}
```

**回應**：

```json
{
  "status": "success",
  "session_id": "sess_abc123",
  "ws_url": "/voice_interaction_realtime/ws?session_id=sess_abc123"
}
```

#### 4.2.3 會話結束

```
POST /voice_interaction_realtime/session/stop
```

**功能**：結束會話並清理資源

## 5. 前端設計

### 5.1 頁面版本

#### 5.1.1 閩南語版本（Roy）

- **路由**：`/voice_interaction_realtime/roy`
- **語音角色**：Roy（閩南語）
- **頁面標題**：「即時語音互動 - 閩南語版」
- **UI 主色調**：橙色系（代表閩南文化）
- **模板檔案**：`voice_interaction_realtime_roy.html`

#### 5.1.2 國語版本（Nofish）

- **路由**：`/voice_interaction_realtime/nofish`
- **語音角色**：Nofish（國語）
- **頁面標題**：「即時語音互動 - 國語版」
- **UI 主色調**：藍色系（代表標準語言）
- **模板檔案**：`voice_interaction_realtime_nofish.html`

### 5.2 功能需求（兩個版本共用）

1. **錄音控制**：開始/停止錄音按鈕
2. **即時顯示**：
   - 辨識中的文字（灰色）
   - 辨識完成的文字（黑色）
   - LLM 回應文字（藍色）
3. **音頻播放**：即時播放合成的語音
4. **狀態指示**：連接狀態、處理狀態
5. **語音角色顯示**：明確標示當前使用的語音（Roy 或 Nofish）

### 5.3 關鍵技術

- **音頻錄製**：使用 `MediaRecorder` API 或 `AudioContext`
- **WebSocket**：雙向通訊
- **音頻播放**：使用 `Web Audio API` 進行流式播放
- **格式轉換**：將瀏覽器音頻轉換為 PCM 16kHz
- **頁面參數化**：透過 URL 參數或模板變數傳遞語音角色

## 6. 實作流程

### 6.1 階段一：ASR 整合

1. 建立 WebSocket 連接到 Qwen-ASR
2. 實作音頻流發送
3. 處理辨識結果（partial + final）
4. 測試辨識準確度

### 6.2 階段二：LLM 整合

1. 整合既有的 `analyze_and_respond_with_context`
2. 實作對話上下文管理
3. 測試回應品質

### 6.3 階段三：TTS 整合

1. 建立 WebSocket 連接到 Qwen TTS Realtime
2. 實作流式音頻接收
3. 實作音頻播放緩衝
4. 測試語音品質與延遲

### 6.4 階段四：整合測試

1. 端到端流程測試
2. 延遲優化
3. 錯誤處理
4. 前端 UI 優化

## 7. 配置需求

### 7.1 環境變數

```bash
DASHSCOPE_API_KEY=sk-xxx  # Qwen API 密鑰
DEEPSEEK_API_KEY=sk-xxx   # DeepSeek API 密鑰（已存在）
```

### 7.2 依賴套件

```
dashscope>=1.14.0
websocket-client>=1.5.0
flask-socketio>=5.3.0  # 用於 WebSocket 支援
```

## 8. 錯誤處理

### 8.1 ASR 錯誤

- 連接失敗：重試機制（最多 3 次）
- 辨識失敗：提示用戶重新說話
- 超時：自動結束當前輸入

### 8.2 LLM 錯誤

- API 錯誤：使用預設回應
- 超時：提示用戶稍後再試

### 8.3 TTS 錯誤

- 連接失敗：降級使用非即時 TTS
- 合成失敗：返回文字回應

## 9. 效能指標

### 9.1 延遲目標

- ASR 延遲：< 500ms
- LLM 延遲：< 2s
- TTS 延遲：< 500ms（首字節）
- 端到端延遲：< 3s

### 9.2 品質目標

- ASR 準確率：> 95%（標準國語）
- LLM 回應相關性：> 90%
- TTS 自然度：> 4.0/5.0

## 10. 安全性考量

1. **API 密鑰保護**：不在前端暴露密鑰
2. **會話隔離**：每個用戶獨立會話
3. **資源限制**：
   - 單次對話最長 5 分鐘
   - 音頻緩衝最大 10MB
4. **錯誤日誌**：記錄但不暴露敏感資訊

## 11. 測試計畫

### 11.1 單元測試

- ASR 連接與辨識
- LLM 回應生成
- TTS 合成與流式輸出

### 11.2 整合測試

- 完整對話流程
- 多輪對話
- 錯誤恢復

### 11.3 壓力測試

- 並發用戶數：10 個同時會話
- 長時間運行：30 分鐘連續對話

---

## 確認事項

請確認以下事項後再開始實作：

1. ✅ 是否使用 Qwen-ASR-Realtime 進行即時辨識？
2. ✅ 是否使用專案既有的 DeepSeek LLM（`services/ai.py`）？
3. ✅ 是否使用 Qwen TTS 的 `qwen3-tts-flash-realtime` 模型？
4. ✅ 是否需要支援 VAD（語音活動檢測）模式？
5. ✅ 是否需要支援多輪對話上下文？
6. ✅ 前端是否需要即時顯示辨識中的文字（partial results）？
7. ✅ 是否拆分為兩個獨立頁面（Roy 閩南語 / Nofish 國語）？
8. ✅ 兩個頁面是否使用不同的 UI 配色？

請回覆「確認」或提出修改建議，我將開始實作。
