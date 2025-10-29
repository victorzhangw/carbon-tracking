# AI 客服語音克隆系統 - 後端技術說明文件

## 📋 系統概述

本系統是一個基於 Flask 的 AI 客服語音克隆與情緒識別系統，提供語音錄製、情緒分析、語音合成、以及智能對話等功能。

## 🏗️ 技術架構

### 核心技術棧

- **Web 框架**: Flask 3.1.0
- **資料庫**: SQLite3 (可擴展至 PostgreSQL/MySQL)
- **音頻處理**: librosa, pydub, soundfile
- **機器學習**: scikit-learn, torch, transformers
- **語音識別**: SpeechRecognition
- **API 設計**: RESTful API
- **身份驗證**: Flask-JWT-Extended
- **跨域支援**: Flask-CORS

### 系統架構圖

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 Vue.js   │───▶│  Flask API 層   │───▶│   服務層 (AI)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   資料庫層      │    │   外部 AI 服務  │
                       │   (SQLite)      │    │   (OpenAI等)    │
                       └─────────────────┘    └─────────────────┘
```

## 🎯 核心功能模組

### 1. 音頻管理模組 (`routes/audio.py`)

#### 技術路線

- **檔案上傳**: 使用 `werkzeug.utils.secure_filename` 確保檔案安全
- **檔案儲存**: 按客服專員代號分類儲存
- **音頻處理**: 使用 `librosa` 提取音頻時長和基本資訊
- **檔案管理**: 支援 CRUD 操作和檔案串流

#### 關鍵 API 端點

```python
POST /api/audio/upload          # 音頻上傳
GET  /api/audio                 # 音頻列表 (分頁)
GET  /api/audio/<id>            # 單個音頻詳情
PUT  /api/audio/<id>            # 更新音頻資訊
DELETE /api/audio/<id>          # 刪除音頻
GET  /api/audio/stream/<id>     # 音頻串流播放
GET  /api/audio/download/<id>   # 音頻下載
```

#### 資料串接模式

```python
# 上傳流程
FormData → 檔案驗證 → 安全儲存 → 資料庫記錄 → 回傳結果

# 資料庫結構
audio: {
    id: UUID,
    name: String,
    staff_id: UUID,
    file_path: String,
    duration: Integer,
    file_size: String,
    emotion: String,           # 情緒分析結果
    emotion_confidence: Float, # 置信度
    created_at: Timestamp
}
```

### 2. 情緒識別模組 (`services/emotion_recognition.py`)

#### 技術路線

**基礎版本 (預設)**:

- **音頻特徵提取**: 使用 librosa 提取 MFCC、光譜質心、零交叉率、節拍
- **分類演算法**: 基於規則的簡單分類器
- **支援情緒**: 6 種基礎情緒 (happy, sad, angry, neutral, fear, surprise)

**進階版本 (可選)**:

- **深度學習模型**: Wav2Vec2ForSequenceClassification
- **預訓練模型**: `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`
- **支援情緒**: 8 種進階情緒 (angry, calm, disgust, fearful, happy, neutral, sad, surprised)

#### 演算法實作

**基礎版本演算法**:

```python
def _simple_emotion_detection(self, audio_path):
    # 1. 音頻載入
    y, sr = librosa.load(audio_path, duration=10)

    # 2. 特徵提取
    rms_energy = np.sqrt(np.mean(y**2))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # 3. 規則分類
    if rms_energy > 0.02 and tempo > 120:
        return "happy"
    elif rms_energy < 0.01 and tempo < 90:
        return "sad"
    # ... 其他規則
```

**進階版本演算法**:

```python
def predict_emotion(self, audio_path):
    # 1. 音頻預處理
    speech, sample_rate = librosa.load(audio_path, sr=16000)

    # 2. 特徵提取 (Wav2Vec2)
    inputs = self.feature_extractor(speech, sampling_rate=sample_rate,
                                   return_tensors="pt", padding=True)

    # 3. 模型推理
    with torch.no_grad():
        logits = self.model(**inputs).logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        predicted_id = torch.argmax(logits, dim=-1).item()

    return self.emotion_labels[predicted_id]
```

#### API 端點

```python
POST /api/emotion/analyze/<audio_id>      # 分析指定音檔
POST /api/emotion/batch-analyze           # 批量分析
POST /api/emotion/upload-and-analyze      # 上傳並分析
GET  /api/emotion/models/status           # 模型狀態
POST /api/emotion/models/load-advanced    # 載入進階模型
```

### 3. 語音合成模組 (`routes/voice_clone.py`)

#### 技術路線

- **語音克隆**: 整合 GPT-SoVITS-v2pro 深度學習模型
- **模型微調**: 基於客服專員語音數據進行個人化訓練
- **語音生成**: 支援多種語調和風格的高品質語音合成
- **音頻後處理**: 格式轉換、降噪和品質優化

#### GPT-SoVITS 架構分析

**模型架構** (基於 `D:\python\GPT-SoVITS-v2pro-20250604`):

```
GPT-SoVITS-v2pro/
├── GPT_SoVITS/           # 核心模型代碼
│   ├── module/           # 神經網路模組
│   ├── text/            # 文字處理
│   ├── AR.py            # 自回歸模型
│   └── SynthesizerTrn.py # VITS 合成器
├── tools/               # 工具腳本
│   ├── asr/            # 自動語音識別
│   ├── uvr5/           # 人聲分離
│   └── slice_audio.py  # 音頻切片
├── configs/            # 配置檔案
├── pretrained_models/  # 預訓練模型
└── logs/              # 訓練日誌
```

**技術原理**:

- **GPT 模型**: 基於 Transformer 的語義理解和韻律預測
- **SoVITS 模型**: 改進版 VITS，支援零樣本語音克隆
- **說話人編碼**: 通過參考音頻學習說話人特徵
- **情感控制**: 支援情感和語調的精細控制

#### GPT-SoVITS 微調工作流程

**1. 環境準備階段**

```python
# GPT-SoVITS 環境配置
class GPTSoVITSEnvironment:
    def __init__(self, base_path="D:/python/GPT-SoVITS-v2pro-20250604"):
        self.base_path = base_path
        self.python_path = f"{base_path}/runtime/python.exe"
        self.config_path = f"{base_path}/configs"
        self.pretrained_path = f"{base_path}/pretrained_models"

    def setup_environment(self):
        """設置 GPT-SoVITS 環境"""
        # 1. 檢查 CUDA 環境
        if not torch.cuda.is_available():
            raise RuntimeError("需要 CUDA 支援進行模型訓練")

        # 2. 載入預訓練模型
        self.download_pretrained_models()

        # 3. 設置環境變數
        os.environ['PYTHONPATH'] = self.base_path
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'

        return True
```

**2. 數據預處理階段**

```python
# 音頻數據預處理管道
class AudioPreprocessingPipeline:
    def __init__(self, gpt_sovits_path):
        self.gpt_sovits_path = gpt_sovits_path
        self.tools_path = f"{gpt_sovits_path}/tools"

    def preprocess_audio_data(self, staff_code, raw_audio_files):
        """完整的音頻預處理管道"""
        processed_data = []

        for audio_file in raw_audio_files:
            try:
                # 1. 人聲分離 (使用 UVR5)
                vocal_file = self.separate_vocals(audio_file)

                # 2. 音頻切片 (3-10秒片段)
                segments = self.slice_audio(vocal_file)

                # 3. 自動語音識別 (ASR)
                for segment in segments:
                    transcript = self.transcribe_audio(segment)

                    # 4. 音頻品質檢查
                    if self.validate_audio_quality(segment, transcript):
                        processed_data.append({
                            'audio_path': segment,
                            'transcript': transcript,
                            'speaker_id': staff_code,
                            'duration': self.get_duration(segment)
                        })

            except Exception as e:
                print(f"處理音頻失敗 {audio_file}: {e}")
                continue

        return processed_data
```

**3. 模型微調階段**

```python
# GPT-SoVITS 微調訓練器
class GPTSoVITSFineTuner:
    def __init__(self, gpt_sovits_path, staff_code):
        self.gpt_sovits_path = gpt_sovits_path
        self.staff_code = staff_code
        self.output_dir = f"models/{staff_code}"

        # 微調配置
        self.config = {
            # GPT 模型配置
            'gpt_config': {
                'batch_size': 4,
                'learning_rate': 0.0001,
                'epochs': 15,
                'save_every_epoch': 5,
                'warmup_epoch': 2
            },
            # SoVITS 模型配置
            'sovits_config': {
                'batch_size': 8,
                'learning_rate': 0.0002,
                'epochs': 100,
                'save_every_epoch': 10,
                'total_epoch': 100
            }
        }

    def fine_tune_gpt_model(self, training_data):
        """微調 GPT 模型"""
        print("🚀 開始 GPT 模型微調...")

        # 1. 準備訓練列表
        train_list_path = self.prepare_gpt_train_list(training_data)

        # 2. 執行 GPT 微調
        cmd = [
            self.python_path,
            f"{self.gpt_sovits_path}/GPT_SoVITS/s1_train.py",
            "--config_path", f"{self.gpt_sovits_path}/configs/s1longer.yaml",
            "--train_list", train_list_path,
            "--output_dir", f"{self.output_dir}/gpt",
            "--batch_size", str(self.config['gpt_config']['batch_size']),
            "--learning_rate", str(self.config['gpt_config']['learning_rate']),
            "--epochs", str(self.config['gpt_config']['epochs'])
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 監控訓練進度
        for line in process.stdout:
            print(f"GPT 訓練: {line.strip()}")

        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"GPT 模型微調失敗: {process.stderr.read()}")

        return self.get_best_gpt_checkpoint()

    def fine_tune_sovits_model(self, training_data, gpt_model_path):
        """微調 SoVITS 模型"""
        print("🚀 開始 SoVITS 模型微調...")

        # 1. 準備訓練列表
        train_list_path = self.prepare_sovits_train_list(training_data)

        # 2. 執行 SoVITS 微調
        cmd = [
            self.python_path,
            f"{self.gpt_sovits_path}/GPT_SoVITS/s2_train.py",
            "--config_path", f"{self.gpt_sovits_path}/configs/s2.json",
            "--train_list", train_list_path,
            "--output_dir", f"{self.output_dir}/sovits",
            "--gpt_model", gpt_model_path,
            "--batch_size", str(self.config['sovits_config']['batch_size']),
            "--learning_rate", str(self.config['sovits_config']['learning_rate']),
            "--total_epoch", str(self.config['sovits_config']['total_epoch'])
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 監控訓練進度
        for line in process.stdout:
            print(f"SoVITS 訓練: {line.strip()}")

        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"SoVITS 模型微調失敗: {process.stderr.read()}")

        return self.get_best_sovits_checkpoint()
```

**4. 推理服務整合**

```python
# GPT-SoVITS 推理服務
class GPTSoVITSInferenceService:
    def __init__(self, gpt_sovits_path, staff_code):
        self.gpt_sovits_path = gpt_sovits_path
        self.staff_code = staff_code
        self.model_loaded = False

    def load_fine_tuned_model(self, gpt_model_path, sovits_model_path, reference_audio):
        """載入微調後的模型"""
        try:
            # 啟動 GPT-SoVITS 推理服務
            self.inference_process = self.start_inference_server(
                gpt_model_path,
                sovits_model_path,
                reference_audio
            )

            # 等待服務啟動
            time.sleep(10)

            # 測試連接
            if self.test_inference_connection():
                self.model_loaded = True
                print(f"✅ {self.staff_code} 模型載入成功")
                return True
            else:
                raise RuntimeError("推理服務連接失敗")

        except Exception as e:
            print(f"❌ 模型載入失敗: {e}")
            return False

    def synthesize_speech(self, text, emotion="neutral", speed=1.0):
        """語音合成"""
        if not self.model_loaded:
            raise RuntimeError("模型未載入")

        # 調用 GPT-SoVITS API
        api_url = f"http://localhost:900{hash(self.staff_code) % 100}/synthesize"

        payload = {
            "text": text,
            "text_language": "zh",
            "ref_audio_path": self.reference_audio,
            "aux_ref_audio_paths": [],
            "prompt_text": "",
            "prompt_language": "zh",
            "top_k": 5,
            "top_p": 1.0,
            "temperature": 1.0,
            "text_split_method": "cut5",
            "batch_size": 1,
            "speed_factor": speed,
            "split_bucket": True,
            "return_fragment": False,
            "fragment_interval": 0.3
        }

        response = requests.post(api_url, json=payload, timeout=60)

        if response.status_code == 200:
            return response.content
        else:
            raise RuntimeError(f"語音合成失敗: {response.text}")
```

**5. 完整工作流程整合**

```python
# 完整的 GPT-SoVITS 微調工作流程
class GPTSoVITSWorkflow:
    def __init__(self, staff_code, gpt_sovits_path="D:/python/GPT-SoVITS-v2pro-20250604"):
        self.staff_code = staff_code
        self.gpt_sovits_path = gpt_sovits_path
        self.workflow_status = "initialized"

    async def execute_full_workflow(self, raw_audio_files, reference_texts):
        """執行完整的微調工作流程"""
        try:
            # 1. 環境準備
            self.workflow_status = "preparing_environment"
            env = GPTSoVITSEnvironment(self.gpt_sovits_path)
            env.setup_environment()

            # 2. 數據預處理
            self.workflow_status = "preprocessing_data"
            preprocessor = AudioPreprocessingPipeline(self.gpt_sovits_path)
            training_data = preprocessor.preprocess_audio_data(self.staff_code, raw_audio_files)

            if len(training_data) < 10:
                raise ValueError(f"訓練數據不足，需要至少10個樣本，目前只有{len(training_data)}個")

            # 3. GPT 模型微調
            self.workflow_status = "fine_tuning_gpt"
            fine_tuner = GPTSoVITSFineTuner(self.gpt_sovits_path, self.staff_code)
            gpt_model_path = fine_tuner.fine_tune_gpt_model(training_data)

            # 4. SoVITS 模型微調
            self.workflow_status = "fine_tuning_sovits"
            sovits_model_path = fine_tuner.fine_tune_sovits_model(training_data, gpt_model_path)

            # 5. 模型品質評估
            self.workflow_status = "evaluating_model"
            quality_metrics = self.evaluate_model_quality(
                gpt_model_path,
                sovits_model_path,
                training_data[:5]
            )

            # 6. 部署推理服務
            self.workflow_status = "deploying_model"
            if quality_metrics['overall_score'] > 0.7:
                inference_service = GPTSoVITSInferenceService(self.gpt_sovits_path, self.staff_code)
                reference_audio = training_data[0]['audio_path']

                success = inference_service.load_fine_tuned_model(
                    gpt_model_path,
                    sovits_model_path,
                    reference_audio
                )

                if success:
                    self.workflow_status = "completed"

                    # 更新資料庫記錄
                    self.update_voice_model_record(
                        gpt_model_path,
                        sovits_model_path,
                        quality_metrics
                    )

                    return {
                        'status': 'success',
                        'gpt_model_path': gpt_model_path,
                        'sovits_model_path': sovits_model_path,
                        'quality_metrics': quality_metrics,
                        'inference_service': inference_service
                    }
                else:
                    raise RuntimeError("推理服務部署失敗")
            else:
                raise ValueError(f"模型品質不達標: {quality_metrics['overall_score']}")

        except Exception as e:
            self.workflow_status = "error"
            return {
                'status': 'error',
                'message': str(e),
                'workflow_status': self.workflow_status
            }
```

#### 資料串接模式更新

```python
# 完整的 GPT-SoVITS 語音合成流程
"""
數據收集階段:
原始音頻 → UVR5人聲分離 → 音頻切片 → ASR轉錄 → 品質檢查 → 訓練數據集

模型微調階段:
訓練數據 → GPT模型微調 → SoVITS模型微調 → 模型驗證 → 品質評估 → 模型部署

語音合成階段:
文字輸入 → GPT語義編碼 → SoVITS聲學合成 → 音頻後處理 → 高品質語音輸出

服務部署階段:
微調模型 → 推理服務啟動 → API接口暴露 → 負載均衡 → 監控告警
"""
```

### 4. 資料庫管理 (`database.py`)

#### 資料庫設計

**核心資料表**:

```sql
-- 用戶表
users: id, username, email, password_hash, full_name, is_active, created_at

-- 客服專員表
staff: id, name, code, phone, email, status, description, created_at

-- 音頻記錄表
audio: id, name, staff_id, file_path, duration, file_size,
       emotion, emotion_confidence, emotion_analysis_data, created_at

-- 情緒分析結果表
emotion_analysis: id, audio_id, method, predicted_emotion, confidence,
                  all_emotions_json, features_json, analyzed_at

-- 語音模型表
voice_models: id, staff_code, original_audio_path, processed_audio_path,
              reference_text, model_status, quality_score, created_at
```

#### 資料存取模式

- **ORM 模式**: 使用原生 SQL + 字典映射
- **連接池**: SQLite 連接管理
- **事務處理**: 支援 ACID 特性
- **分頁查詢**: 高效能分頁實作

## 🔐 安全機制

### 身份驗證

```python
# JWT Token 驗證
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)

# 密碼加密
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```

### 檔案安全

```python
# 檔案名稱安全化
filename = secure_filename(f"{audio_id}_{file.filename}")

# 檔案類型驗證
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'ogg'}

# 檔案大小限制
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

## 📊 效能優化

### 音頻處理優化

- **異步處理**: 情緒分析不阻塞主流程
- **檔案快取**: 臨時檔案自動清理
- **記憶體管理**: 大檔案分塊處理

### 資料庫優化

- **索引設計**: 關鍵欄位建立索引
- **查詢優化**: 分頁查詢和條件篩選
- **連接管理**: 適當的連接池大小

## 🚀 模型儲存與部署架構

### 📦 模型儲存策略

#### 1. 本地端儲存架構 (目前實作)

**目錄結構**:

```
project_root/
├── models/                          # 模型儲存根目錄
│   ├── pretrained/                  # 預訓練模型
│   │   ├── emotion_recognition/     # 情緒識別預訓練模型
│   │   │   ├── wav2vec2_base.pt    # Wav2Vec2 基礎模型
│   │   │   └── librosa_features.pkl # librosa 特徵提取器
│   │   └── gpt_sovits/             # GPT-SoVITS 預訓練模型
│   │       ├── s1bert25hz.ckpt     # GPT 預訓練模型
│   │       ├── s2G488k.pth         # SoVITS G 模型
│   │       └── s2D488k.pth         # SoVITS D 模型
│   ├── fine_tuned/                 # 微調模型
│   │   ├── staff001/               # 客服專員 001
│   │   │   ├── gpt_model.pt        # 微調後的 GPT 模型
│   │   │   ├── sovits_model.pt     # 微調後的 SoVITS 模型
│   │   │   ├── speaker_embedding.pt # 說話人嵌入
│   │   │   ├── model_config.json   # 模型配置
│   │   │   └── quality_metrics.json # 品質指標
│   │   └── staff002/               # 客服專員 002
│   │       └── ...
│   ├── cache/                      # 模型快取
│   │   ├── inference_cache/        # 推理快取
│   │   └── feature_cache/          # 特徵快取
│   └── backups/                    # 模型備份
│       ├── daily/                  # 每日備份
│       └── weekly/                 # 每週備份
```

**本地端模型管理器**:

```python
class LocalModelManager:
    def __init__(self, base_path="./models"):
        self.base_path = base_path
        self.pretrained_path = f"{base_path}/pretrained"
        self.fine_tuned_path = f"{base_path}/fine_tuned"
        self.cache_path = f"{base_path}/cache"
        self.backup_path = f"{base_path}/backups"

    def save_fine_tuned_model(self, staff_code, model_data, quality_metrics):
        """儲存微調後的模型"""
        model_dir = f"{self.fine_tuned_path}/{staff_code}"
        os.makedirs(model_dir, exist_ok=True)

        # 儲存模型檔案
        torch.save(model_data['gpt_model'], f"{model_dir}/gpt_model.pt")
        torch.save(model_data['sovits_model'], f"{model_dir}/sovits_model.pt")
        torch.save(model_data['speaker_embedding'], f"{model_dir}/speaker_embedding.pt")

        # 儲存配置和指標
        with open(f"{model_dir}/model_config.json", 'w') as f:
            json.dump(model_data['config'], f, indent=2)

        with open(f"{model_dir}/quality_metrics.json", 'w') as f:
            json.dump(quality_metrics, f, indent=2)

        # 創建備份
        self.create_backup(staff_code)

        return model_dir

    def load_fine_tuned_model(self, staff_code):
        """載入微調後的模型"""
        model_dir = f"{self.fine_tuned_path}/{staff_code}"

        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"找不到 {staff_code} 的模型")

        # 載入模型
        gpt_model = torch.load(f"{model_dir}/gpt_model.pt")
        sovits_model = torch.load(f"{model_dir}/sovits_model.pt")
        speaker_embedding = torch.load(f"{model_dir}/speaker_embedding.pt")

        # 載入配置
        with open(f"{model_dir}/model_config.json", 'r') as f:
            config = json.load(f)

        return {
            'gpt_model': gpt_model,
            'sovits_model': sovits_model,
            'speaker_embedding': speaker_embedding,
            'config': config
        }

    def create_backup(self, staff_code):
        """創建模型備份"""
        source_dir = f"{self.fine_tuned_path}/{staff_code}"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"{self.backup_path}/daily/{staff_code}_{timestamp}"

        shutil.copytree(source_dir, backup_dir)

        # 清理舊備份（保留最近 7 天）
        self.cleanup_old_backups(staff_code, days=7)

    def get_model_info(self, staff_code):
        """獲取模型資訊"""
        model_dir = f"{self.fine_tuned_path}/{staff_code}"

        if not os.path.exists(model_dir):
            return None

        # 讀取品質指標
        metrics_file = f"{model_dir}/quality_metrics.json"
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                quality_metrics = json.load(f)
        else:
            quality_metrics = {}

        # 獲取檔案資訊
        model_files = os.listdir(model_dir)
        file_sizes = {
            file: os.path.getsize(os.path.join(model_dir, file))
            for file in model_files
        }

        return {
            'staff_code': staff_code,
            'model_path': model_dir,
            'quality_metrics': quality_metrics,
            'file_sizes': file_sizes,
            'last_modified': os.path.getmtime(model_dir),
            'total_size': sum(file_sizes.values())
        }
```

#### 2. GCP 雲端部署架構 (未來擴展)

**GCP 服務架構**:

```
Google Cloud Platform 部署架構
├── Compute Engine                   # 主要運算資源
│   ├── AI Training Instances        # 模型訓練專用實例
│   │   ├── GPU: NVIDIA T4/V100     # GPU 加速訓練
│   │   ├── CPU: 8-16 vCPUs         # 高效能 CPU
│   │   └── RAM: 32-64 GB           # 大記憶體支援
│   └── Inference Instances          # 推理服務實例
│       ├── GPU: NVIDIA T4          # 推理加速
│       ├── Auto Scaling Group      # 自動擴展
│       └── Load Balancer           # 負載均衡
├── Cloud Storage                    # 模型和數據儲存
│   ├── Model Bucket                # 模型檔案儲存
│   │   ├── pretrained-models/      # 預訓練模型
│   │   ├── fine-tuned-models/      # 微調模型
│   │   └── model-backups/          # 模型備份
│   ├── Audio Bucket                # 音頻檔案儲存
│   │   ├── raw-audio/              # 原始音頻
│   │   ├── processed-audio/        # 處理後音頻
│   │   └── generated-audio/        # 生成音頻
│   └── Training Data Bucket        # 訓練數據
├── Cloud SQL                       # 關聯式資料庫
│   ├── PostgreSQL Instance         # 主資料庫
│   ├── Read Replicas              # 讀取副本
│   └── Backup & Recovery          # 備份恢復
├── Cloud Memorystore              # Redis 快取
│   ├── Model Cache                # 模型快取
│   ├── Session Cache              # 會話快取
│   └── Feature Cache              # 特徵快取
├── Cloud Run                      # 容器化服務
│   ├── API Gateway                # API 閘道
│   ├── Authentication Service     # 身份驗證服務
│   └── Monitoring Service         # 監控服務
├── AI Platform                    # 機器學習平台
│   ├── Training Jobs              # 訓練任務
│   ├── Prediction Services        # 預測服務
│   └── Model Registry             # 模型註冊表
└── Cloud Functions                # 無伺服器函數
    ├── Model Deployment           # 模型部署函數
    ├── Data Processing            # 數據處理函數
    └── Webhook Handlers           # Webhook 處理
```

**GCP 模型管理器**:

```python
from google.cloud import storage, aiplatform
from google.cloud.sql import connector
import redis

class GCPModelManager:
    def __init__(self, project_id, region="asia-east1"):
        self.project_id = project_id
        self.region = region
        self.storage_client = storage.Client()
        self.model_bucket = "ai-customer-service-models"
        self.audio_bucket = "ai-customer-service-audio"

        # 初始化 AI Platform
        aiplatform.init(project=project_id, location=region)

        # Redis 快取連接
        self.redis_client = redis.Redis(
            host='redis-instance-ip',
            port=6379,
            decode_responses=True
        )

    def upload_model_to_gcs(self, staff_code, local_model_path):
        """上傳模型到 Google Cloud Storage"""
        bucket = self.storage_client.bucket(self.model_bucket)

        # 上傳模型檔案
        model_files = os.listdir(local_model_path)
        uploaded_files = []

        for file_name in model_files:
            local_file_path = os.path.join(local_model_path, file_name)
            gcs_path = f"fine-tuned-models/{staff_code}/{file_name}"

            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_file_path)

            uploaded_files.append({
                'file_name': file_name,
                'gcs_path': gcs_path,
                'size': os.path.getsize(local_file_path)
            })

        # 更新模型註冊表
        self.register_model_in_ai_platform(staff_code, uploaded_files)

        return uploaded_files

    def register_model_in_ai_platform(self, staff_code, model_files):
        """在 AI Platform 註冊模型"""
        model_display_name = f"voice-clone-{staff_code}"

        # 創建模型
        model = aiplatform.Model.upload(
            display_name=model_display_name,
            artifact_uri=f"gs://{self.model_bucket}/fine-tuned-models/{staff_code}/",
            serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/pytorch-gpu.1-9:latest",
            description=f"GPT-SoVITS voice cloning model for staff {staff_code}"
        )

        return model

    def deploy_model_endpoint(self, staff_code, machine_type="n1-standard-4"):
        """部署模型端點"""
        model_display_name = f"voice-clone-{staff_code}"
        endpoint_display_name = f"voice-clone-endpoint-{staff_code}"

        # 獲取模型
        models = aiplatform.Model.list(
            filter=f'display_name="{model_display_name}"'
        )

        if not models:
            raise ValueError(f"找不到模型: {model_display_name}")

        model = models[0]

        # 創建端點
        endpoint = aiplatform.Endpoint.create(
            display_name=endpoint_display_name
        )

        # 部署模型到端點
        endpoint.deploy(
            model=model,
            deployed_model_display_name=f"deployed-{staff_code}",
            machine_type=machine_type,
            min_replica_count=1,
            max_replica_count=5,
            accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=1
        )

        return endpoint

    def setup_auto_scaling(self, staff_code):
        """設置自動擴展"""
        endpoint_name = f"voice-clone-endpoint-{staff_code}"

        # 配置自動擴展策略
        scaling_config = {
            "min_replica_count": 1,
            "max_replica_count": 10,
            "target_cpu_utilization": 70,
            "target_memory_utilization": 80
        }

        return scaling_config

    def setup_model_monitoring(self, staff_code):
        """設置模型監控"""
        monitoring_config = {
            "model_performance": {
                "latency_threshold": 2000,  # 2秒
                "error_rate_threshold": 0.05,  # 5%
                "throughput_threshold": 100  # 每分鐘 100 請求
            },
            "resource_usage": {
                "cpu_threshold": 80,  # 80%
                "memory_threshold": 85,  # 85%
                "gpu_threshold": 90  # 90%
            },
            "alerts": {
                "email": ["admin@company.com"],
                "slack_webhook": "https://hooks.slack.com/..."
            }
        }

        return monitoring_config
```

### 🔄 模型版本管理

#### 版本控制策略

```python
class ModelVersionManager:
    def __init__(self, storage_backend="local"):  # "local" or "gcp"
        self.storage_backend = storage_backend
        self.version_format = "v{major}.{minor}.{patch}"

    def create_new_version(self, staff_code, model_data, quality_metrics):
        """創建新的模型版本"""
        # 獲取當前最新版本
        current_version = self.get_latest_version(staff_code)

        # 決定版本號增量策略
        new_version = self.calculate_next_version(
            current_version,
            quality_metrics
        )

        # 儲存新版本
        version_path = self.save_versioned_model(
            staff_code,
            new_version,
            model_data,
            quality_metrics
        )

        # 更新版本索引
        self.update_version_index(staff_code, new_version, quality_metrics)

        return new_version, version_path

    def calculate_next_version(self, current_version, quality_metrics):
        """計算下一個版本號"""
        if current_version is None:
            return "v1.0.0"

        major, minor, patch = self.parse_version(current_version)

        # 根據品質指標決定版本增量
        if quality_metrics.get('overall_score', 0) > 0.9:
            # 重大改進
            major += 1
            minor = 0
            patch = 0
        elif quality_metrics.get('overall_score', 0) > 0.8:
            # 功能改進
            minor += 1
            patch = 0
        else:
            # 小幅改進
            patch += 1

        return f"v{major}.{minor}.{patch}"

    def rollback_to_version(self, staff_code, target_version):
        """回滾到指定版本"""
        version_path = self.get_version_path(staff_code, target_version)

        if not self.version_exists(staff_code, target_version):
            raise ValueError(f"版本 {target_version} 不存在")

        # 備份當前版本
        current_version = self.get_latest_version(staff_code)
        if current_version:
            self.backup_current_version(staff_code, current_version)

        # 恢復目標版本
        self.restore_version(staff_code, target_version)

        return version_path
```

### 🚀 部署環境配置

#### 本地端部署

```bash
# 開發環境設置
# 1. 依賴安裝
pip install -r requirements.txt

# 2. 模型目錄初始化
mkdir -p models/{pretrained,fine_tuned,cache,backups}

# 3. 下載預訓練模型
python scripts/download_pretrained_models.py

# 4. 資料庫初始化
python -c "from database import init_db; init_db()"

# 5. 啟動服務
python app.py
```

#### GCP 雲端部署

```yaml
# docker-compose.gcp.yml
version: "3.8"
services:
  flask-app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=production
      - GOOGLE_CLOUD_PROJECT=${PROJECT_ID}
      - GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:5432/${DB_NAME}
      - REDIS_URL=redis://${REDIS_HOST}:6379
      - MODEL_STORAGE_BACKEND=gcp
      - GCS_MODEL_BUCKET=${MODEL_BUCKET}
      - GCS_AUDIO_BUCKET=${AUDIO_BUCKET}
    volumes:
      - ./service-account.json:/app/service-account.json:ro
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "2"
          memory: 4G
        reservations:
          cpus: "1"
          memory: 2G

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - flask-app
```

#### Kubernetes 部署配置

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-customer-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-customer-service
  template:
    metadata:
      labels:
        app: ai-customer-service
    spec:
      containers:
        - name: flask-app
          image: gcr.io/${PROJECT_ID}/ai-customer-service:latest
          ports:
            - containerPort: 8080
          env:
            - name: GOOGLE_CLOUD_PROJECT
              value: ${PROJECT_ID}
            - name: MODEL_STORAGE_BACKEND
              value: "gcp"
          resources:
            requests:
              memory: "2Gi"
              cpu: "1"
              nvidia.com/gpu: 1
            limits:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: 1
          volumeMounts:
            - name: service-account
              mountPath: /app/service-account.json
              subPath: service-account.json
              readOnly: true
      volumes:
        - name: service-account
          secret:
            secretName: gcp-service-account

---
apiVersion: v1
kind: Service
metadata:
  name: ai-customer-service-service
spec:
  selector:
    app: ai-customer-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

### 📊 效能與成本比較

#### 本地端 vs GCP 比較表

| 項目         | 本地端部署   | GCP 雲端部署 |
| ------------ | ------------ | ------------ |
| **初始成本** | 硬體投資高   | 按使用付費   |
| **維護成本** | 人力維護高   | 託管服務低   |
| **擴展性**   | 硬體限制     | 彈性擴展     |
| **可用性**   | 單點故障風險 | 99.9% SLA    |
| **安全性**   | 自行管理     | 企業級安全   |
| **備份恢復** | 手動備份     | 自動備份     |
| **監控告警** | 基礎監控     | 完整監控     |
| **多地部署** | 困難         | 簡單         |

#### 成本估算 (月費用)

**本地端成本**:

- 硬體攤提: $2,000-5,000
- 電費: $200-500
- 維護人力: $3,000-8,000
- **總計**: $5,200-13,500/月

**GCP 成本** (中等負載):

- Compute Engine: $800-1,500
- Cloud Storage: $100-300
- Cloud SQL: $200-500
- AI Platform: $300-800
- 網路流量: $100-200
- **總計**: $1,500-3,300/月

### 🔧 遷移策略

#### 從本地端到 GCP 的遷移步驟

1. **評估階段** (1-2 週)

   - 分析現有模型和數據量
   - 評估網路頻寬需求
   - 制定遷移時程表

2. **準備階段** (2-3 週)

   - 設置 GCP 專案和服務
   - 配置網路和安全設定
   - 準備遷移腳本

3. **測試階段** (1-2 週)

   - 小規模數據遷移測試
   - 功能驗證測試
   - 效能基準測試

4. **遷移階段** (1 週)

   - 數據批量遷移
   - 服務切換
   - 監控和調優

5. **驗證階段** (1 週)
   - 全功能測試
   - 效能驗證
   - 用戶接受測試

這個模型儲存與部署架構提供了從本地端到雲端的完整解決方案，確保系統能夠隨著業務需求的增長而彈性擴展。

## 🔧 配置管理

### 環境配置 (`config.py`)

```python
# 檔案路徑配置
AUDIO_UPLOAD_FOLDER = 'audio_uploads'
VOICE_OUTPUT_FOLDER = 'voice_output'
DATABASE = 'customer_service.db'

# 支援的檔案格式
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'ogg'}

# API 配置
API_TIMEOUT = 60  # 秒
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
```

## 📈 監控與日誌

### 日誌記錄

```python
import logging

# 設定日誌級別
logging.basicConfig(level=logging.INFO)

# 關鍵操作記錄
logger.info(f"音頻上傳成功: {audio_id}")
logger.error(f"情緒分析失敗: {error}")
```

### 效能監控

- **API 回應時間**: 記錄各端點回應時間
- **檔案處理時間**: 監控音頻處理效能
- **錯誤率統計**: 追蹤系統穩定性

## 🧪 測試策略

### 單元測試

```python
# 情緒識別測試
def test_emotion_recognition():
    result = emotion_recognizer.predict_emotion('test_audio.wav')
    assert 'predicted_emotion' in result
    assert 'confidence' in result
```

### 整合測試

```python
# API 端點測試
def test_audio_upload():
    response = client.post('/api/audio/upload',
                          files={'file': test_audio_file})
    assert response.status_code == 201
```

## 🔮 擴展性考量

### 水平擴展

- **微服務架構**: 可拆分為獨立的情緒分析服務
- **負載均衡**: 支援多實例部署
- **快取層**: Redis 快取熱門資料

### 功能擴展

- **多語言支援**: 支援多種語言的情緒識別
- **即時處理**: WebSocket 支援即時音頻分析
- **AI 模型更新**: 支援模型熱更新機制

## 📚 重要技術決策

1. **SQLite vs PostgreSQL**: 開發階段使用 SQLite，生產環境建議 PostgreSQL
2. **同步 vs 異步**: 情緒分析採用異步處理，不影響主流程
3. **本地 vs 雲端**: 基礎情緒識別本地處理，進階版本可考慮雲端 API
4. **檔案儲存**: 本地檔案系統，可擴展至雲端儲存 (AWS S3, Azure Blob)

## 🛠️ 故障排除

### 常見問題

1. **音頻格式不支援**: 檢查 `ALLOWED_EXTENSIONS` 設定
2. **情緒識別失敗**: 檢查 librosa 和相關依賴
3. **檔案上傳失敗**: 檢查檔案大小和權限設定
4. **資料庫連接錯誤**: 檢查資料庫檔案權限和路徑

### 除錯工具

```python
# 開啟除錯模式
app.run(debug=True)

# 詳細錯誤日誌
import traceback
traceback.print_exc()
```

這份文件涵蓋了後端系統的核心技術架構、演算法實作、資料串接模式以及重要的技術決策，為系統的維護和擴展提供了完整的技術指南。
