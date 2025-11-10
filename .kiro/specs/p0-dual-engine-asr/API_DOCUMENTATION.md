# P0-1 雙引擎 ASR API 文檔

**版本**: 1.0.0  
**基礎 URL**: `http://localhost:5000/api/asr`  
**認證**: JWT Bearer Token（除健康檢查外）

---

## API 端點總覽

| 端點               | 方法 | 認證 | 描述         |
| ------------------ | ---- | ---- | ------------ |
| `/health`          | GET  | ❌   | 健康檢查     |
| `/recognize`       | POST | ✅   | 單個音頻識別 |
| `/batch-recognize` | POST | ✅   | 批次音頻識別 |
| `/status`          | GET  | ✅   | 獲取系統狀態 |
| `/clear-cache`     | POST | ✅   | 清理系統快取 |

---

## 1. 健康檢查

**端點**: `GET /api/asr/health`  
**認證**: 不需要  
**描述**: 檢查 ASR 服務是否正常運行

### 請求範例

```bash
curl http://localhost:5000/api/asr/health
```

### 響應範例

```json
{
  "status": "healthy",
  "timestamp": "2024-10-29T16:30:00",
  "service": "ASR API",
  "version": "1.0.0"
}
```

### 響應欄位

| 欄位      | 類型   | 描述                         |
| --------- | ------ | ---------------------------- |
| status    | string | 服務狀態 (healthy/unhealthy) |
| timestamp | string | ISO 8601 時間戳              |
| service   | string | 服務名稱                     |
| version   | string | API 版本                     |

---

## 2. 單個音頻識別

**端點**: `POST /api/asr/recognize`  
**認證**: 需要 JWT Token  
**描述**: 識別單個音頻文件

### 請求參數

**Headers**:

```
Authorization: Bearer <your_jwt_token>
Content-Type: multipart/form-data
```

**Form Data**:
| 參數 | 類型 | 必填 | 描述 |
|------|------|------|------|
| file | file | ✅ | 音頻文件 (WAV/MP3/M4A/FLAC) |
| language_hint | string | ❌ | 語言提示 (zh/zh-TW/minnan) |
| return_details | boolean | ❌ | 是否返回詳細信息 (true/false) |
| enable_minnan_optimization | boolean | ❌ | 是否啟用閩南語優化 (true/false) |

### 請求範例

```bash
curl -X POST http://localhost:5000/api/asr/recognize \
  -H "Authorization: Bearer <token>" \
  -F "file=@audio.wav" \
  -F "language_hint=zh" \
  -F "return_details=true"
```

### 響應範例

```json
{
  "success": true,
  "text": "使用軟件者傳播軟件導出的聲音者自負全責",
  "confidence": 0.859,
  "language": "zh",
  "audio_duration": 8.39,
  "processing_time": 2.96,
  "details": {
    "features": {
      "is_minnan": false,
      "is_elderly": false,
      "is_low_snr": false,
      "snr_db": -3.0
    },
    "fusion_info": {
      "mode": "single",
      "reason": "funasr_unavailable"
    }
  }
}
```

### 響應欄位

| 欄位            | 類型    | 描述             |
| --------------- | ------- | ---------------- |
| success         | boolean | 是否成功         |
| text            | string  | 識別的文本       |
| confidence      | float   | 置信度 (0-1)     |
| language        | string  | 識別的語言       |
| audio_duration  | float   | 音頻時長（秒）   |
| processing_time | float   | 處理時間（秒）   |
| details         | object  | 詳細信息（可選） |

---

## 3. 批次音頻識別

**端點**: `POST /api/asr/batch-recognize`  
**認證**: 需要 JWT Token  
**描述**: 批次識別多個音頻文件

### 請求參數

**Headers**:

```
Authorization: Bearer <your_jwt_token>
Content-Type: multipart/form-data
```

**Form Data**:
| 參數 | 類型 | 必填 | 描述 |
|------|------|------|------|
| files | file[] | ✅ | 多個音頻文件 |
| language_hint | string | ❌ | 語言提示 |
| return_details | boolean | ❌ | 是否返回詳細信息 |

### 請求範例

```bash
curl -X POST http://localhost:5000/api/asr/batch-recognize \
  -H "Authorization: Bearer <token>" \
  -F "files=@audio1.wav" \
  -F "files=@audio2.wav" \
  -F "files=@audio3.wav" \
  -F "language_hint=zh"
```

### 響應範例

```json
{
  "success": true,
  "results": [
    {
      "index": 0,
      "success": true,
      "text": "第一段音頻內容",
      "confidence": 0.85,
      "processing_time": 2.5
    },
    {
      "index": 1,
      "success": true,
      "text": "第二段音頻內容",
      "confidence": 0.92,
      "processing_time": 2.3
    }
  ],
  "total": 2,
  "successful": 2,
  "failed": 0
}
```

---

## 4. 獲取系統狀態

**端點**: `GET /api/asr/status`  
**認證**: 需要 JWT Token  
**描述**: 獲取 ASR 系統的詳細狀態信息

### 請求範例

```bash
curl http://localhost:5000/api/asr/status \
  -H "Authorization: Bearer <token>"
```

### 響應範例

```json
{
  "status": "ready",
  "system_info": {
    "coordinator": {
      "version": "1.0.0",
      "enable_funasr": false,
      "target_sample_rate": 16000,
      "max_audio_length": 60
    },
    "whisper_engine": {
      "engine": "whisper",
      "model_size": "base",
      "device": "cuda",
      "cuda_available": true,
      "model_loaded": true,
      "memory_usage": {
        "device": "cuda",
        "gpu_memory_allocated": "0.28 GB",
        "gpu_memory_reserved": "0.50 GB",
        "gpu_memory_total": "4.00 GB"
      }
    }
  }
}
```

---

## 5. 清理快取

**端點**: `POST /api/asr/clear-cache`  
**認證**: 需要 JWT Token  
**描述**: 清理 GPU 快取，釋放記憶體

### 請求範例

```bash
curl -X POST http://localhost:5000/api/asr/clear-cache \
  -H "Authorization: Bearer <token>"
```

### 響應範例

```json
{
  "success": true,
  "message": "快取已清理"
}
```

---

## 錯誤碼

| 狀態碼 | 描述                |
| ------ | ------------------- |
| 200    | 成功                |
| 400    | 請求參數錯誤        |
| 401    | 未認證或 Token 無效 |
| 403    | 權限不足            |
| 500    | 服務器內部錯誤      |
| 503    | 服務不可用          |

### 錯誤響應格式

```json
{
  "success": false,
  "error": "錯誤描述"
}
```

---

## 使用範例

### Python 範例

```python
import requests

# 1. 登入
login_response = requests.post(
    "http://localhost:5000/api/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = login_response.json()['access_token']

# 2. 識別音頻
with open('audio.wav', 'rb') as f:
    response = requests.post(
        "http://localhost:5000/api/asr/recognize",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": f},
        data={"language_hint": "zh", "return_details": "true"}
    )

result = response.json()
print(f"識別文本: {result['text']}")
print(f"置信度: {result['confidence']}")
```

### JavaScript 範例

```javascript
// 1. 登入
const loginResponse = await fetch("http://localhost:5000/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ username: "admin", password: "admin123" }),
});
const { access_token } = await loginResponse.json();

// 2. 識別音頻
const formData = new FormData();
formData.append("file", audioFile);
formData.append("language_hint", "zh");

const response = await fetch("http://localhost:5000/api/asr/recognize", {
  method: "POST",
  headers: { Authorization: `Bearer ${access_token}` },
  body: formData,
});

const result = await response.json();
console.log("識別文本:", result.text);
console.log("置信度:", result.confidence);
```

---

## 性能指標

### 預期性能

| 指標     | 目標值 | 當前值 |
| -------- | ------ | ------ |
| 處理時間 | < 2 秒 | ~3 秒  |
| 準確率   | 94.2%  | 測試中 |
| 併發支援 | 100    | 測試中 |
| 可用性   | 99.2%  | 測試中 |

### 優化建議

1. **使用更大的模型**: medium 或 large-v3（需要更多 VRAM）
2. **啟用 FunASR**: 雙引擎融合提升準確率
3. **模型量化**: INT8 量化提升速度
4. **批次處理**: 多個請求並行處理

---

## 注意事項

1. **音頻格式**: 支援 WAV, MP3, M4A, FLAC
2. **音頻長度**: 最大 60 秒（超過會自動截取）
3. **文件大小**: 建議 < 10MB
4. **併發限制**: 建議不超過 10 個並發請求（取決於 GPU 記憶體）
5. **Token 有效期**: 8 小時（需要定期刷新）

---

**文檔版本**: 1.0.0  
**最後更新**: 2024-10-29  
**維護者**: AI 系統開發團隊
