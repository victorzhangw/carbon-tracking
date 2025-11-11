# FunASR 模型安裝指南

## 問題描述

FunASR 模型自動下載可能因網絡問題失敗，錯誤信息：

```
File am.mvn download incomplete, content_length: None
TypeError: 'NoneType' object is not callable
```

## 解決方案

### 方案 1: 手動下載模型（推薦）

#### 步驟 1: 創建模型目錄

```bash
mkdir -p models/paraformer-zh
```

#### 步驟 2: 從 ModelScope 下載

訪問 ModelScope 模型頁面：
https://www.modelscope.cn/models/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch

或使用 git clone：

```bash
cd models
git clone https://www.modelscope.cn/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch.git paraformer-zh
```

#### 步驟 3: 修改代碼使用本地模型

在 `services/asr/funasr_engine.py` 中：

```python
self.model = AutoModel(
    model="./models/paraformer-zh",  # 使用本地路徑
    device=self.device
)
```

### 方案 2: 使用 HuggingFace 模型

#### 步驟 1: 安裝 HuggingFace Hub

```bash
pip install huggingface_hub
```

#### 步驟 2: 修改代碼

```python
from funasr import AutoModel

self.model = AutoModel(
    model="damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    hub="hf",  # 使用 HuggingFace
    device=self.device
)
```

### 方案 3: 配置網絡代理

#### Windows (PowerShell)

```powershell
$env:HTTP_PROXY="http://proxy-server:port"
$env:HTTPS_PROXY="http://proxy-server:port"
```

#### Windows (CMD)

```cmd
set HTTP_PROXY=http://proxy-server:port
set HTTPS_PROXY=http://proxy-server:port
```

#### Linux/Mac

```bash
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port
```

然後重新運行：

```bash
python test_funasr_engine.py
```

### 方案 4: 使用 ModelScope CLI

#### 步驟 1: 安裝 ModelScope CLI

```bash
pip install modelscope
```

#### 步驟 2: 下載模型

```python
from modelscope.hub.snapshot_download import snapshot_download

model_dir = snapshot_download(
    'iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    cache_dir='./models'
)
print(f"模型已下載到: {model_dir}")
```

#### 步驟 3: 使用下載的模型

```python
self.model = AutoModel(
    model=model_dir,
    device=self.device
)
```

## 驗證安裝

運行測試腳本驗證：

```bash
python test_funasr_engine.py
```

成功輸出應包含：

```
✓ 引擎初始化成功
✓ 完整模型載入成功
✓ FunASR 引擎測試完成
```

## 模型文件結構

成功下載後，模型目錄應包含：

```
models/paraformer-zh/
├── am.mvn
├── config.yaml
├── model.pb
├── tokens.txt
└── ...
```

## 常見問題

### Q1: 下載速度很慢

A: 使用代理或選擇其他下載源（HuggingFace）

### Q2: 磁盤空間不足

A: Paraformer 模型約 1-2GB，確保有足夠空間

### Q3: 模型版本不匹配

A: 確保 FunASR 版本與模型版本兼容：

```bash
pip install funasr --upgrade
```

### Q4: CUDA 記憶體不足

A: 使用 CPU 模式：

```python
engine = FunASREngine(device="cpu")
```

## 替代方案

如果 FunASR 持續無法使用，可以考慮：

1. **僅使用 Whisper**: 系統已實現降級策略
2. **使用其他中文 ASR**: 如 WeNet、Kaldi
3. **使用雲端 API**: 如阿里雲、騰訊雲 ASR 服務

## 技術支持

- FunASR GitHub: https://github.com/alibaba-damo-academy/FunASR
- ModelScope: https://www.modelscope.cn
- 項目 Issues: 在項目倉庫提交問題

---

**文檔版本**: v1.0  
**最後更新**: 2025-10-29  
**適用於**: FunASR 0.8.x+
