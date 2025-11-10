# FunASR 快速開始指南

## 🚀 快速安裝（3 步驟）

### 步驟 1: 安裝 ModelScope

```bash
pip install modelscope
```

### 步驟 2: 下載模型

```bash
python download_funasr_model.py
```

等待下載完成（約 5-10 分鐘，取決於網速）

### 步驟 3: 測試

```bash
python test_funasr_engine.py
```

看到 `✓ FunASR 引擎測試完成` 就成功了！

---

## 📝 使用方法

### 方法 1: 自動檢測本地模型

```python
from services.asr.funasr_engine import FunASREngine

# 如果 models/paraformer-zh 存在，會自動使用
engine = FunASREngine(device="cuda")
```

### 方法 2: 明確指定路徑

```python
engine = FunASREngine(
    device="cuda",
    local_model_path="./models/paraformer-zh"
)
```

### 方法 3: 在 Coordinator 中使用

```python
from services.asr.coordinator import ASRCoordinator

coordinator = ASRCoordinator(
    whisper_model_size="base",
    enable_funasr=True,
    funasr_model_path="./models/paraformer-zh",
    device="cuda"
)

# 使用雙引擎識別
result = await coordinator.recognize(audio_data)
```

---

## ❓ 常見問題

### Q: 下載失敗怎麼辦？

**A**: 嘗試以下方法：

1. **配置代理**:

   ```bash
   set HTTP_PROXY=http://proxy:port
   set HTTPS_PROXY=http://proxy:port
   python download_funasr_model.py
   ```

2. **手動下載**: 參考 `docs/funasr_manual_install.md`

3. **使用 Whisper 單引擎**: 系統已支援降級，不影響使用

### Q: 如何確認模型已安裝？

**A**: 檢查目錄：

```bash
dir models\paraformer-zh
```

應該看到：

- am.mvn
- config.yaml
- model.pb (或 model.pt)
- tokens.txt

### Q: GPU 記憶體不足？

**A**: 使用 CPU 模式：

```python
engine = FunASREngine(device="cpu")
```

---

## 📚 更多資源

- **完整安裝指南**: `docs/funasr_manual_install.md`
- **實現狀態**: `.kiro/specs/p0-dual-engine-asr/funasr_status.md`
- **API 文檔**: `.kiro/specs/p0-dual-engine-asr/API_DOCUMENTATION.md`

---

## ✅ 驗證清單

- [ ] ModelScope 已安裝
- [ ] 模型已下載到 `models/paraformer-zh`
- [ ] 測試腳本運行成功
- [ ] 可以進行語音識別

完成後，你就可以使用 FunASR 引擎了！🎉
