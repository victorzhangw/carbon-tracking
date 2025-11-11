# FunASR 模型手動安裝完整指南

## 概述

本指南將幫助你手動下載並安裝 FunASR Paraformer 模型，解決自動下載失敗的問題。

---

## 方案 1: 使用 ModelScope CLI（最簡單）

### 步驟 1: 安裝 ModelScope

```bash
pip install modelscope
```

### 步驟 2: 創建下載腳本

創建文件 `download_funasr_model.py`:

```python
from modelscope.hub.snapshot_download import snapshot_download
import os

# 創建模型目錄
os.makedirs('models', exist_ok=True)

# 下載模型
print("開始下載 FunASR Paraformer 模型...")
print("這可能需要幾分鐘，請耐心等待...")

model_dir = snapshot_download(
    'iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    cache_dir='./models',
    revision='master'
)

print(f"\n✓ 模型已下載到: {model_dir}")
print("\n請記住這個路徑，稍後需要使用！")
```

### 步驟 3: 運行下載腳本

```bash
python download_funasr_model.py
```

### 步驟 4: 記錄模型路徑

下載完成後，腳本會顯示模型路徑，例如：

```
✓ 模型已下載到: ./models/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
```

### 步驟 5: 測試模型

```bash
# 設置環境變量指向本地模型
set FUNASR_MODEL_PATH=./models/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch

# 運行測試
python test_funasr_engine.py
```

---

## 方案 2: 從 ModelScope 網站手動下載

### 步驟 1: 訪問模型頁面

打開瀏覽器，訪問：

```
https://www.modelscope.cn/models/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
```

### 步驟 2: 下載文件

點擊「文件」標籤，下載以下關鍵文件到 `models/paraformer-zh/` 目錄：

**必需文件**:

- `am.mvn` - 聲學模型均值方差
- `config.yaml` - 模型配置
- `model.pb` 或 `model.pt` - 模型權重
- `tokens.txt` - 詞彙表

**可選文件**（提升功能）:

- `vad.pb` - 語音活動檢測
- `punc.pb` - 標點預測
- `README.md` - 說明文檔

### 步驟 3: 組織文件結構

確保文件結構如下：

```
models/
└── paraformer-zh/
    ├── am.mvn
    ├── config.yaml
    ├── model.pb (或 model.pt)
    ├── tokens.txt
    ├── vad.pb (可選)
    └── punc.pb (可選)
```

### 步驟 4: 測試模型

```bash
python test_funasr_engine.py
```

---

## 方案 3: 使用 Git LFS 克隆

### 步驟 1: 安裝 Git LFS

**Windows**:

1. 下載安裝器: https://git-lfs.github.com/
2. 運行安裝器
3. 打開命令提示符，運行: `git lfs install`

**Linux**:

```bash
sudo apt-get install git-lfs
git lfs install
```

### 步驟 2: 克隆模型倉庫

```bash
# 創建模型目錄
mkdir -p models
cd models

# 克隆模型（這會下載所有文件）
git clone https://www.modelscope.cn/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch.git paraformer-zh

cd ..
```

### 步驟 3: 驗證下載

```bash
# 檢查文件
dir models\paraformer-zh

# 應該看到 am.mvn, config.yaml, model.pb 等文件
```

### 步驟 4: 測試模型

```bash
python test_funasr_engine.py
```

---

## 方案 4: 使用代理下載

如果網絡受限，可以配置代理：

### Windows PowerShell:

```powershell
$env:HTTP_PROXY="http://your-proxy:port"
$env:HTTPS_PROXY="http://your-proxy:port"
python download_funasr_model.py
```

### Windows CMD:

```cmd
set HTTP_PROXY=http://your-proxy:port
set HTTPS_PROXY=http://your-proxy:port
python download_funasr_model.py
```

---

## 在代碼中使用本地模型

### 方法 1: 直接指定路徑

```python
from services.asr.funasr_engine import FunASREngine

# 使用本地模型
engine = FunASREngine(
    model_name="paraformer-zh",
    device="cuda",
    local_model_path="./models/paraformer-zh"  # 你的本地路徑
)
```

### 方法 2: 在 Coordinator 中使用

```python
from services.asr.coordinator import ASRCoordinator

coordinator = ASRCoordinator(
    whisper_model_size="base",
    enable_funasr=True,
    funasr_model_path="./models/paraformer-zh",  # 本地模型路徑
    device="cuda"
)
```

### 方法 3: 使用環境變量

創建 `.env` 文件：

```
FUNASR_MODEL_PATH=./models/paraformer-zh
```

在代碼中讀取：

```python
import os
from dotenv import load_dotenv

load_dotenv()
model_path = os.getenv('FUNASR_MODEL_PATH')

engine = FunASREngine(
    device="cuda",
    local_model_path=model_path
)
```

---

## 驗證安裝

### 快速測試

```bash
python test_funasr_engine.py
```

### 預期輸出

```
============================================================
FunASR 引擎測試
============================================================

1. 初始化 FunASR 引擎...
   找到本地模型: ./models/paraformer-zh
INFO:services.asr.funasr_engine:載入本地 FunASR 模型: ./models/paraformer-zh
INFO:services.asr.funasr_engine:  嘗試載入完整模型（含 VAD 和標點）...
INFO:services.asr.funasr_engine:  ✓ 完整模型載入成功
INFO:services.asr.funasr_engine:✓ FunASR 模型已載入到 cuda
✓ 引擎初始化成功

2. 模型信息:
   engine: funasr
   model_name: paraformer-zh
   device: cuda
   cuda_available: True
   model_loaded: True
   ...

✓ FunASR 引擎測試完成
```

---

## 常見問題排查

### Q1: 下載速度很慢

**解決方案**:

- 使用代理或 VPN
- 選擇網絡較好的時段下載
- 使用方案 2 手動下載單個文件

### Q2: 提示 "模型路徑不存在"

**檢查**:

```bash
# 確認路徑是否正確
dir models\paraformer-zh

# 確認必需文件是否存在
dir models\paraformer-zh\am.mvn
dir models\paraformer-zh\config.yaml
```

### Q3: 模型載入失敗

**可能原因**:

1. 文件下載不完整 - 重新下載
2. 文件損壞 - 刪除後重新下載
3. 權限問題 - 以管理員身份運行

### Q4: CUDA 記憶體不足

**解決方案**:

```python
# 使用 CPU 模式
engine = FunASREngine(
    device="cpu",
    local_model_path="./models/paraformer-zh"
)
```

### Q5: 找不到某些文件

**最小配置**:
只需要這些文件即可運行：

- `am.mvn`
- `config.yaml`
- `model.pb` 或 `model.pt`
- `tokens.txt`

VAD 和標點模型是可選的。

---

## 模型文件說明

| 文件名      | 大小   | 說明                        | 必需    |
| ----------- | ------ | --------------------------- | ------- |
| am.mvn      | ~11KB  | 聲學模型均值方差            | ✅ 是   |
| config.yaml | ~2KB   | 模型配置文件                | ✅ 是   |
| model.pb    | ~220MB | 模型權重（Protocol Buffer） | ✅ 是   |
| tokens.txt  | ~100KB | 詞彙表                      | ✅ 是   |
| vad.pb      | ~1MB   | 語音活動檢測模型            | ⭕ 可選 |
| punc.pb     | ~50MB  | 標點預測模型                | ⭕ 可選 |

**總大小**: 約 270-320 MB

---

## 下一步

模型安裝成功後：

1. **運行完整測試**:

   ```bash
   python test_funasr_engine.py
   ```

2. **測試雙引擎協作**:

   ```bash
   python test_asr_coordinator.py
   ```

3. **繼續開發任務**:
   - 任務 4.2: 實現 FunASR 閩南語優化
   - 任務 4.3: 實現 FunASR 性能優化

---

## 技術支持

如果遇到問題：

1. 查看日誌輸出
2. 檢查 `.kiro/specs/p0-dual-engine-asr/funasr_status.md`
3. 參考 FunASR 官方文檔: https://github.com/alibaba-damo-academy/FunASR
4. 在項目 Issues 中提問

---

**文檔版本**: v1.0  
**最後更新**: 2025-10-29  
**適用於**: FunASR 0.8.x+, Python 3.8+
