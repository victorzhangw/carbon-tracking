# P0-1: 雙引擎 ASR 架構與閩南語支援 - 設計文檔

## 概述

本文檔描述雙引擎 ASR 系統的技術設計，整合 Whisper 和 FunASR 模型，並特別優化閩南語識別。

**設計版本**: v1.0  
**基於需求**: requirements.md v1.0  
**目標**: 達到 94.2% 整體準確率，89.3% 閩南語準確率

---

## 系統架構

### 高層架構

```
┌─────────────────────────────────────────────────────────────┐
│                    雙引擎 ASR 系統架構                       │
├─────────────────────────────────────────────────────────────┤
│  API 層 (Flask)                                             │
│  ├── /api/asr/recognize        # 單個音頻識別              │
│  ├── /api/asr/batch-recognize  # 批次識別                  │
│  └── /api/asr/status           # 系統狀態                  │
├─────────────────────────────────────────────────────────────┤
│  協調層 (ASR Coordinator)                                   │
│  ├── 音頻預處理                                             │
│  ├── 雙引擎並行調度                                         │
│  ├── 結果融合                                               │
│  └── 後處理與格式化                                         │
├─────────────────────────────────────────────────────────────┤
│  引擎層                                                     │
│  ├── Whisper Engine            ├── FunASR Engine           │
│  │   ├── 模型載入              │   ├── 模型載入            │
│  │   ├── 特徵提取              │   ├── 特徵提取            │
│  │   ├── 推理                  │   ├── 推理                │
│  │   └── 置信度計算            │   └── 置信度計算          │
├─────────────────────────────────────────────────────────────┤
│  支援層                                                     │
│  ├── 閩南語檢測器                                           │
│  ├── 高齡語音檢測器                                         │
│  ├── 噪音處理器                                             │
│  └── 日誌與監控                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心組件設計

### 1. ASR Coordinator（協調器）

**職責**: 協調雙引擎工作流程，管理音頻處理生命週期

**主要方法**:

```python
class ASRCoordinator:
    def __init__(self):
        self.whisper_engine = WhisperEngine()
        self.funasr_engine = FunASREngine()
        self.fusion_algorithm = ConfidenceFusion()
        self.minnan_detector = MinnanLanguageDetector()
        self.elderly_detector = ElderlyVoiceDetector()

    async def recognize(self, audio_data, options=None):
        # 1. 音頻預處理
        processed_audio = self.preprocess_audio(audio_data)

        # 2. 特徵檢測
        features = self.detect_features(processed_audio)

        # 3. 並行調用雙引擎
        whisper_result, funasr_result = await asyncio.gather(
            self.whisper_engine.recognize(processed_audio, features),
            self.funasr_engine.recognize(processed_audio, features)
        )

        # 4. 結果融合
        final_result = self.fusion_algorithm.fuse(
            whisper_result,
            funasr_result,
            features
        )

        # 5. 後處理
        return self.postprocess_result(final_result, features)
```

### 2. Whisper Engine（Whisper 引擎）

**模型**: openai/whisper-large-v3  
**優勢**: 多語言支援、魯棒性強、處理噪音能力好

**配置**:

```python
whisper_config = {
    "model_name": "large-v3",
    "language": "zh",  # 中文
    "task": "transcribe",
    "beam_size": 5,
    "best_of": 5,
    "temperature": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    "compression_ratio_threshold": 2.4,
    "logprob_threshold": -1.0,
    "no_speech_threshold": 0.6
}
```

**實現**:

```python
class WhisperEngine:
    def __init__(self, model_path="models/whisper-large-v3"):
        self.model = whisper.load_model("large-v3")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    async def recognize(self, audio_data, features):
        # 特徵調整
        if features.get('is_minnan'):
            # 閩南語優化參數
            options = {"language": "zh", "initial_prompt": "這是台灣閩南語"}
        elif features.get('is_elderly'):
            # 高齡語音優化參數
            options = {"temperature": 0.2, "beam_size": 10}
        else:
            options = {}

        # 推理
        result = self.model.transcribe(
            audio_data,
            **options
        )

        # 計算置信度
        confidence = self.calculate_confidence(result)

        return {
            "text": result["text"],
            "confidence": confidence,
            "language": result.get("language"),
            "segments": result.get("segments", [])
        }
```

### 3. FunASR Engine（FunASR 引擎）

**模型**: damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch  
**優勢**: 中文優化、識別速度快、準確率高

**配置**:

```python
funasr_config = {
    "model": "paraformer-zh",
    "model_revision": "v2.0.4",
    "vad_model": "fsmn-vad",
    "punc_model": "ct-punc",
    "spk_model": "cam++",  # 說話人識別
    "device": "cuda:0"
}
```

**實現**:

```python
class FunASREngine:
    def __init__(self, model_path="models/paraformer-zh"):
        from funasr import AutoModel

        self.model = AutoModel(
            model="paraformer-zh",
            vad_model="fsmn-vad",
            punc_model="ct-punc",
            device="cuda" if torch.cuda.is_available() else "cpu"
        )

    async def recognize(self, audio_data, features):
        # 特徵調整
        if features.get('is_minnan'):
            # 閩南語優化：使用微調模型
            self.load_finetuned_model("minnan")

        # 推理
        result = self.model.generate(
            input=audio_data,
            batch_size_s=300,
            hotword="",
            use_itn=True
        )

        # 提取結果
        text = result[0]["text"]
        confidence = self.calculate_confidence(result[0])

        return {
            "text": text,
            "confidence": confidence,
            "timestamp": result[0].get("timestamp", [])
        }
```

### 4. Confidence Fusion（置信度融合算法）

**策略**: 動態加權融合，基於置信度和語言特徵

**算法設計**:

```python
class ConfidenceFusion:
    def fuse(self, whisper_result, funasr_result, features):
        w_conf = whisper_result["confidence"]
        f_conf = funasr_result["confidence"]

        # 基礎權重計算
        if features.get('is_minnan'):
            # 閩南語：FunASR 微調模型更準確
            base_weight_whisper = 0.4
            base_weight_funasr = 0.6
        else:
            # 一般華語：平衡權重
            base_weight_whisper = 0.5
            base_weight_funasr = 0.5

        # 動態調整權重
        if w_conf > 0.9 and f_conf < 0.7:
            weight_whisper = 0.8
            weight_funasr = 0.2
        elif f_conf > 0.9 and w_conf < 0.7:
            weight_whisper = 0.2
            weight_funasr = 0.8
        else:
            # 使用置信度加權
            total_conf = w_conf + f_conf
            weight_whisper = base_weight_whisper * (w_conf / total_conf)
            weight_funasr = base_weight_funasr * (f_conf / total_conf)

        # 文本融合
        final_text = self.merge_texts(
            whisper_result["text"],
            funasr_result["text"],
            weight_whisper,
            weight_funasr
        )

        # 最終置信度
        final_confidence = (
            weight_whisper * w_conf +
            weight_funasr * f_conf
        )

        return {
            "text": final_text,
            "confidence": final_confidence,
            "whisper_weight": weight_whisper,
            "funasr_weight": weight_funasr,
            "fusion_method": "dynamic_confidence_weighted"
        }
```

### 5. Minnan Language Detector（閩南語檢測器）

**目的**: 自動檢測音頻中的閩南語成分

**實現**:

```python
class MinnanLanguageDetector:
    def __init__(self):
        # 載入語言識別模型
        self.lid_model = self.load_language_id_model()

        # 閩南語特徵詞彙
        self.minnan_keywords = [
            "啥物", "按怎", "佗位", "啥人", "敢有",
            "毋是", "毋知", "毋好", "足", "誠"
        ]

    def detect(self, audio_data, text_hint=None):
        # 1. 音頻特徵檢測
        audio_features = self.extract_audio_features(audio_data)
        audio_score = self.lid_model.predict(audio_features)

        # 2. 文本特徵檢測（如果有初步轉錄）
        text_score = 0.0
        if text_hint:
            text_score = self.detect_minnan_text(text_hint)

        # 3. 綜合判斷
        is_minnan = (audio_score > 0.5) or (text_score > 0.3)
        confidence = max(audio_score, text_score)

        # 4. 混合程度估計
        mix_ratio = self.estimate_mix_ratio(audio_features, text_hint)

        return {
            "is_minnan": is_minnan,
            "confidence": confidence,
            "mix_ratio": mix_ratio,  # 0=純華語, 1=純閩南語
            "audio_score": audio_score,
            "text_score": text_score
        }
```

---

## 數據模型

### ASR Request（識別請求）

```python
@dataclass
class ASRRequest:
    audio_data: bytes
    audio_format: str  # wav, mp3, m4a, flac
    sample_rate: int = 16000
    language_hint: Optional[str] = None  # zh, zh-TW, minnan
    return_details: bool = False
    enable_minnan_optimization: bool = True
```

### ASR Response（識別響應）

```python
@dataclass
class ASRResponse:
    text: str
    confidence: float
    language: str
    processing_time: float

    # 詳細信息（可選）
    whisper_result: Optional[Dict] = None
    funasr_result: Optional[Dict] = None
    fusion_details: Optional[Dict] = None
    features_detected: Optional[Dict] = None
```

### Training Data（訓練數據）

```python
@dataclass
class TrainingData:
    audio_path: str
    transcript: str
    language: str  # zh, minnan, mixed
    dialect: Optional[str]  # taipei, taichung, tainan, kaohsiung
    speaker_age: Optional[int]
    snr: Optional[float]
    duration: float
    quality_score: float
```

---

## 閩南語優化策略

### 1. 數據準備

- 收集 200 小時台灣閩南語音頻
- 四種地區口音各 50 小時
- 混合程度分布：純閩南語 30%、混合 50%、口音華語 20%

### 2. 模型微調

```python
# FunASR 閩南語微調配置
minnan_finetune_config = {
    "base_model": "paraformer-zh",
    "training_data": "data/minnan_200h",
    "learning_rate": 5e-5,
    "batch_size": 16,
    "epochs": 20,
    "warmup_steps": 1000,
    "gradient_accumulation": 4,
    "mixed_precision": "fp16"
}
```

### 3. 特殊處理

- 閩南語詞彙表擴充
- 閩南語語言模型整合
- 閩南語發音規則適配

---

## 性能優化

### 1. 模型量化

```python
# INT8 量化配置
quantization_config = {
    "whisper": {
        "method": "dynamic",
        "dtype": "int8",
        "reduce_range": True
    },
    "funasr": {
        "method": "static",
        "calibration_data": "data/calibration_100samples"
    }
}
```

### 2. 批次處理

- 支援最多 8 個音頻同時處理
- 動態批次大小調整
- GPU 記憶體管理

### 3. 快取策略

- 模型權重快取
- 特徵提取結果快取
- 常見詞彙快取

---

## 錯誤處理

### 錯誤類型

1. **音頻格式錯誤**: 返回 400，提示支援的格式
2. **音頻過長**: 自動分段處理（每段 30 秒）
3. **音頻品質過低**: 警告但繼續處理
4. **模型載入失敗**: 重試 3 次，失敗則降級到單引擎
5. **GPU 記憶體不足**: 自動切換到 CPU

### 降級策略

```python
class DegradationStrategy:
    def handle_failure(self, error_type):
        if error_type == "whisper_failed":
            # 降級到 FunASR 單引擎
            return "funasr_only"
        elif error_type == "funasr_failed":
            # 降級到 Whisper 單引擎
            return "whisper_only"
        elif error_type == "both_failed":
            # 使用備用模型
            return "fallback_model"
```

---

## 測試策略

### 1. 單元測試

- 每個組件獨立測試
- Mock 外部依賴
- 覆蓋率 ≥ 80%

### 2. 整合測試

- 雙引擎協作測試
- 融合算法測試
- 端到端流程測試

### 3. 專項測試

- 閩南語測試集（100 樣本）
- 高齡語音測試集（100 樣本）
- 低 SNR 測試集（50 樣本）

### 4. 性能測試

- 負載測試（100 併發）
- 壓力測試（500 併發）
- 持久性測試（24 小時）

---

## 部署架構

### 開發環境

```yaml
services:
  asr-service:
    image: asr-dual-engine:dev
    ports:
      - "5000:5000"
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - MODEL_PATH=/models
    volumes:
      - ./models:/models
      - ./data:/data
```

### 生產環境

```yaml
services:
  asr-service:
    image: asr-dual-engine:prod
    replicas: 3
    resources:
      limits:
        cpus: "4"
        memory: 8G
        nvidia.com/gpu: 1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## 監控指標

### 關鍵指標

1. **準確率**: 整體、閩南語、高齡語音
2. **WER**: 整體、閩南語
3. **處理時間**: P50, P95, P99
4. **吞吐量**: 每秒處理請求數
5. **錯誤率**: 各類錯誤的發生率
6. **資源使用**: CPU、GPU、記憶體

### 告警規則

- 準確率 < 90%: 警告
- 處理時間 > 5 秒: 警告
- 錯誤率 > 5%: 嚴重
- GPU 記憶體 > 90%: 警告

---

**設計版本**: v1.0  
**下一步**: 創建實現任務列表（tasks.md）
