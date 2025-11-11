# P0-1 ASR 開發環境設置指南

## 環境需求

### 硬體需求

- **CPU**: Intel i5 或以上（推薦 i7/i9）
- **RAM**: 最少 16GB（推薦 32GB）
- **GPU**: NVIDIA GPU with CUDA support（推薦 RTX 3060 或以上）
  - VRAM: 最少 6GB（推薦 12GB+）
- **儲存**: 最少 50GB 可用空間

### 軟體需求

- **作業系統**: Windows 10/11, Linux, macOS
- **Python**: 3.8 - 3.11（推薦 3.10）
- **CUDA**: 11.8 或 12.1（如果使用 GPU）
- **cuDNN**: 對應 CUDA 版本

---

## 安裝步驟

### 1. 檢查 Python 版本

```bash
python --version
# 應該顯示 Python 3.8.x 到 3.11.x
```

### 2. 創建虛擬環境（推薦）

```bash
# 使用 venv
python -m venv venv-asr

# 啟動虛擬環境
# Windows:
venv-asr\Scripts\activate
# Linux/macOS:
source venv-asr/bin/activate
```

### 3. 升級 pip

```bash
python -m pip install --upgrade pip
```

### 4. 安裝 PyTorch（根據您的系統）

#### 有 NVIDIA GPU（推薦）

```bash
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### 僅 CPU

```bash
pip install torch torchvision torchaudio
```

### 5. 驗證 PyTorch 安裝

```python
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"
```

預期輸出：

```
PyTorch: 2.1.0+cu118
CUDA available: True
CUDA version: 11.8
```

### 6. 安裝 ASR 依賴

```bash
pip install -r requirements-asr.txt
```

### 7. 下載預訓練模型

#### Whisper 模型

```python
# 執行以下 Python 腳本下載 Whisper 模型
python -c "import whisper; whisper.load_model('large-v3')"
```

模型會下載到：

- Windows: `C:\Users\<username>\.cache\whisper\`
- Linux/macOS: `~/.cache/whisper/`

#### FunASR 模型

```python
# 執行以下 Python 腳本下載 FunASR 模型
python -c "from funasr import AutoModel; AutoModel(model='paraformer-zh')"
```

模型會下載到：

- `~/.cache/modelscope/`

### 8. 驗證安裝

創建測試腳本 `test_asr_setup.py`:

```python
import torch
import whisper
from funasr import AutoModel
import librosa
import numpy as np

print("=== ASR 環境驗證 ===\n")

# 1. PyTorch
print(f"✓ PyTorch: {torch.__version__}")
print(f"✓ CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✓ CUDA version: {torch.version.cuda}")
    print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

# 2. Whisper
print("\n--- Whisper ---")
try:
    model = whisper.load_model("base")  # 使用小模型測試
    print("✓ Whisper 模型載入成功")
    del model
except Exception as e:
    print(f"✗ Whisper 錯誤: {e}")

# 3. FunASR
print("\n--- FunASR ---")
try:
    model = AutoModel(model="paraformer-zh")
    print("✓ FunASR 模型載入成功")
    del model
except Exception as e:
    print(f"✗ FunASR 錯誤: {e}")

# 4. Librosa
print("\n--- Librosa ---")
try:
    # 創建測試音頻
    sr = 16000
    duration = 1
    t = np.linspace(0, duration, sr * duration)
    audio = np.sin(2 * np.pi * 440 * t)  # 440Hz 正弦波

    # 測試特徵提取
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    print(f"✓ Librosa 工作正常 (MFCC shape: {mfccs.shape})")
except Exception as e:
    print(f"✗ Librosa 錯誤: {e}")

print("\n=== 驗證完成 ===")
```

執行測試：

```bash
python test_asr_setup.py
```

---

## 常見問題

### Q1: CUDA 不可用

**問題**: `torch.cuda.is_available()` 返回 `False`

**解決方案**:

1. 確認已安裝 NVIDIA 驅動程式
2. 確認安裝了對應版本的 CUDA Toolkit
3. 重新安裝 PyTorch GPU 版本

### Q2: Whisper 模型下載失敗

**問題**: 網路連接問題導致模型下載失敗

**解決方案**:

1. 使用代理或 VPN
2. 手動下載模型文件並放置到快取目錄
3. 使用國內鏡像源

### Q3: FunASR 模型下載慢

**問題**: ModelScope 下載速度慢

**解決方案**:

```bash
# 設置 ModelScope 鏡像
export MODELSCOPE_CACHE=~/.cache/modelscope
```

### Q4: 記憶體不足

**問題**: 載入大模型時記憶體不足

**解決方案**:

1. 使用較小的模型（如 Whisper base 而非 large）
2. 減少批次大小
3. 使用模型量化

### Q5: ImportError

**問題**: 缺少某些依賴

**解決方案**:

```bash
pip install --upgrade -r requirements-asr.txt
```

---

## 模型大小參考

### Whisper 模型

| 模型     | 參數量 | 大小  | VRAM 需求 |
| -------- | ------ | ----- | --------- |
| tiny     | 39M    | 150MB | ~1GB      |
| base     | 74M    | 290MB | ~1GB      |
| small    | 244M   | 950MB | ~2GB      |
| medium   | 769M   | 3GB   | ~5GB      |
| large-v3 | 1550M  | 6GB   | ~10GB     |

### FunASR 模型

| 模型          | 大小   | VRAM 需求 |
| ------------- | ------ | --------- |
| paraformer-zh | ~220MB | ~2GB      |

---

## 開發工具推薦

### IDE

- **VS Code** + Python 擴展
- **PyCharm Professional**

### 調試工具

- **Jupyter Notebook** - 互動式開發
- **TensorBoard** - 模型訓練可視化

### 性能分析

- **nvidia-smi** - GPU 監控
- **htop** - CPU/記憶體監控

---

## 下一步

環境設置完成後，您可以：

1. 執行 `test_asr_setup.py` 驗證環境
2. 開始實現任務 2.1（ASR Coordinator 基礎框架）
3. 查看設計文檔 `.kiro/specs/p0-dual-engine-asr/design.md`

---

**設置完成！** 🎉

如有問題，請參考：

- Whisper 文檔: https://github.com/openai/whisper
- FunASR 文檔: https://github.com/alibaba-damo-academy/FunASR
- PyTorch 文檔: https://pytorch.org/docs/
