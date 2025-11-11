# GPT-SoVITS 模型微調完整指南

## 📋 概述

本指南詳細說明如何使用 GPT-SoVITS-v2pro 進行客服專員語音克隆的模型微調，包括環境設置、數據準備、模型訓練、品質評估和部署等完整流程。

## 🏗️ 系統架構

### GPT-SoVITS-v2pro 目錄結構

```
D:\python\GPT-SoVITS-v2pro-20250604/
├── GPT_SoVITS/              # 核心模型代碼
│   ├── module/              # 神經網路模組
│   │   ├── core.py         # 核心模組
│   │   ├── quantize.py     # 量化模組
│   │   └── losses.py       # 損失函數
│   ├── text/               # 文字處理
│   │   ├── chinese.py      # 中文處理
│   │   ├── english.py      # 英文處理
│   │   └── japanese.py     # 日文處理
│   ├── AR.py               # 自回歸模型
│   ├── SynthesizerTrn.py   # VITS 合成器
│   ├── s1_train.py         # GPT 模型訓練
│   └── s2_train.py         # SoVITS 模型訓練
├── tools/                  # 工具腳本
│   ├── asr/               # 自動語音識別
│   │   ├── funasr_asr.py  # FunASR 識別
│   │   └── whisper_asr.py # Whisper 識別
│   ├── uvr5/              # 人聲分離
│   │   ├── webui.py       # UVR5 網頁界面
│   │   └── separate.py    # 分離腳本
│   ├── slice_audio.py     # 音頻切片
│   └── resample_audio.py  # 音頻重採樣
├── configs/               # 配置檔案
│   ├── s1longer.yaml      # GPT 長文本配置
│   ├── s2.json           # SoVITS 配置
│   └── config.py         # 全局配置
├── pretrained_models/     # 預訓練模型
│   ├── chinese-roberta-wwm-ext-large/  # 中文 BERT
│   ├── chinese-hubert-base/            # 中文 HuBERT
│   ├── s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt  # GPT 預訓練
│   └── s2G488k.pth                     # SoVITS 預訓練
├── api.py                 # API 服務
├── webui.py              # 網頁界面
└── requirements.txt      # 依賴套件
```

## 🔧 環境準備

### 1. 硬體需求

- **GPU**: NVIDIA RTX 3080 或更高 (至少 10GB VRAM)
- **RAM**: 32GB 或更高
- **儲存**: 至少 100GB 可用空間
- **CUDA**: 11.8 或更高版本

### 2. 軟體環境設置

```bash
# 1. 創建 Python 虛擬環境
cd D:\python\GPT-SoVITS-v2pro-20250604
python -m venv venv
venv\Scripts\activate

# 2. 安裝依賴套件
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. 下載預訓練模型
python download_models.py
```

## 📊 數據準備流程

### 1. 原始音頻要求

- **格式**: WAV, MP3, M4A, FLAC
- **採樣率**: 22050Hz (推薦) 或 44100Hz
- **聲道**: 單聲道 (Mono)
- **時長**: 每個檔案 10 秒 - 5 分鐘
- **品質**: 清晰無雜音，SNR > 20dB
- **數量**: 至少 20 個檔案，推薦 50+ 個檔案

### 2. 數據預處理步驟

#### Step 1: 人聲分離

```python
# 使用 UVR5 進行人聲分離
def separate_vocals(input_audio, output_dir):
    cmd = [
        "python", "tools/uvr5/separate.py",
        "--input", input_audio,
        "--output", output_dir,
        "--model", "HP2-人声vocals+非人声instrumental.pth",
        "--device", "cuda"
    ]
    subprocess.run(cmd, check=True)
```

#### Step 2: 音頻切片

```python
# 將長音頻切成 3-10 秒片段
def slice_audio(input_audio, output_dir):
    cmd = [
        "python", "tools/slice_audio.py",
        "--input", input_audio,
        "--output", output_dir,
        "--min_length", "3000",    # 3秒
        "--max_length", "10000",   # 10秒
        "--min_interval", "300",   # 300ms 靜音間隔
        "--hop_size", "10",        # 10ms 跳躍
        "--max_sil_kept", "500"    # 保留 500ms 靜音
    ]
    subprocess.run(cmd, check=True)
```

#### Step 3: 自動語音識別

```python
# 使用 FunASR 進行語音識別
def transcribe_audio(audio_file):
    cmd = [
        "python", "tools/asr/funasr_asr.py",
        "--input", audio_file,
        "--output", f"{audio_file}.txt",
        "--language", "zh",
        "--model", "paraformer-zh"
    ]
    subprocess.run(cmd, check=True)

    with open(f"{audio_file}.txt", 'r', encoding='utf-8') as f:
        return f.read().strip()
```

## 🚀 模型微調流程

### 1. GPT 模型微調 (第一階段)

#### 配置檔案設置

```yaml
# configs/s1longer.yaml
model:
  semantic_frame_rate: 25
  max_sec: 30
  batch_size: 4
  learning_rate: 0.0001
  epochs: 15
  save_every_epoch: 5
  warmup_epoch: 2

data:
  train_list: "logs/staff001/gpt_train_list.txt"
  valid_list: "logs/staff001/gpt_valid_list.txt"

training:
  precision: "fp16"
  gradient_accumulation_steps: 4
  max_grad_norm: 1.0
```

#### 訓練列表格式

```
# logs/staff001/gpt_train_list.txt
audio_path|speaker_id|transcript
data/staff001/audio_001.wav|staff001|您好，歡迎來到我們的客服中心
data/staff001/audio_002.wav|staff001|請問有什麼可以幫助您的嗎
data/staff001/audio_003.wav|staff001|感謝您的來電，祝您有美好的一天
```

#### 執行 GPT 訓練

```bash
python GPT_SoVITS/s1_train.py \
    --config_path configs/s1longer.yaml \
    --train_list logs/staff001/gpt_train_list.txt \
    --valid_list logs/staff001/gpt_valid_list.txt \
    --output_dir logs/staff001/gpt \
    --pretrained_s1 pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt
```

### 2. SoVITS 模型微調 (第二階段)

#### 配置檔案設置

```json
{
  "train": {
    "log_interval": 200,
    "eval_interval": 1000,
    "seed": 1234,
    "epochs": 100,
    "learning_rate": 0.0002,
    "betas": [0.8, 0.99],
    "eps": 1e-9,
    "batch_size": 8,
    "fp16_run": true,
    "lr_decay": 0.999875,
    "segment_size": 17920,
    "init_lr_ratio": 1,
    "warmup_epochs": 0,
    "c_mel": 45,
    "c_kl": 1.0
  },
  "data": {
    "training_files": "logs/staff001/sovits_train_list.txt",
    "validation_files": "logs/staff001/sovits_valid_list.txt",
    "max_wav_value": 32768.0,
    "sampling_rate": 22050,
    "filter_length": 1024,
    "hop_length": 256,
    "win_length": 1024,
    "n_mel_channels": 80,
    "mel_fmin": 0.0,
    "mel_fmax": null
  }
}
```

#### 執行 SoVITS 訓練

```bash
python GPT_SoVITS/s2_train.py \
    --config_path configs/s2.json \
    --model_name staff001 \
    --pretrained_s2G pretrained_models/s2G488k.pth \
    --pretrained_s2D pretrained_models/s2D488k.pth
```

## 📈 模型品質評估

### 1. 客觀評估指標

```python
class ModelEvaluator:
    def evaluate_model(self, model_path, test_data):
        metrics = {}

        # 1. MOS 分數 (平均意見分數)
        metrics['mos_score'] = self.calculate_mos(model_path, test_data)

        # 2. 說話人相似度
        metrics['speaker_similarity'] = self.calculate_speaker_similarity(model_path, test_data)

        # 3. 語音自然度
        metrics['naturalness'] = self.calculate_naturalness(model_path, test_data)

        # 4. 語音清晰度
        metrics['intelligibility'] = self.calculate_intelligibility(model_path, test_data)

        # 5. 推理速度
        metrics['inference_speed'] = self.calculate_inference_speed(model_path)

        return metrics
```

### 2. 品質閾值標準

- **MOS 分數**: > 3.5 (滿分 5.0)
- **說話人相似度**: > 0.75
- **語音自然度**: > 0.70
- **語音清晰度**: > 0.80
- **推理速度**: < 2.0 RTF (Real Time Factor)

## 🚀 模型部署

### 1. 推理服務啟動

```python
# 啟動 GPT-SoVITS API 服務
def start_inference_service(staff_code, gpt_model, sovits_model, reference_audio):
    cmd = [
        "python", "api.py",
        "--gpt_model", gpt_model,
        "--sovits_model", sovits_model,
        "--reference_audio", reference_audio,
        "--port", f"900{hash(staff_code) % 100}",
        "--device", "cuda",
        "--half", "true"  # 使用半精度加速
    ]

    return subprocess.Popen(cmd)
```

### 2. API 調用範例

```python
import requests

def synthesize_speech(text, staff_code, emotion="neutral", speed=1.0):
    api_url = f"http://localhost:900{hash(staff_code) % 100}/synthesize"

    payload = {
        "text": text,
        "text_language": "zh",
        "ref_audio_path": f"reference/{staff_code}_ref.wav",
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
        return response.content  # 返回音頻數據
    else:
        raise RuntimeError(f"語音合成失敗: {response.text}")
```

## 🔧 故障排除

### 常見問題與解決方案

1. **CUDA 記憶體不足**

   - 減少 batch_size
   - 使用 gradient_accumulation_steps
   - 啟用 fp16 訓練

2. **訓練收斂慢**

   - 檢查學習率設置
   - 增加 warmup_epochs
   - 檢查數據品質

3. **語音品質差**

   - 增加訓練數據量
   - 提高原始音頻品質
   - 調整模型超參數

4. **推理速度慢**
   - 使用 TensorRT 優化
   - 啟用半精度推理
   - 使用 GPU 加速

## 📊 性能優化建議

### 1. 訓練優化

- 使用混合精度訓練 (fp16)
- 梯度累積減少記憶體使用
- 數據並行處理加速訓練

### 2. 推理優化

- 模型量化 (INT8)
- 動態批處理
- 快取機制減少重複計算

### 3. 部署優化

- 使用 Docker 容器化部署
- 負載均衡分散請求
- 監控系統追蹤性能

這份指南提供了完整的 GPT-SoVITS 微調流程，從環境準備到模型部署的每個步驟都有詳細說明，確保能夠成功訓練出高品質的個人化語音克隆模型。
