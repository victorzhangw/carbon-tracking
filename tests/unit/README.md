# Unit Tests

## Purpose

此目錄包含所有單元測試，用於測試獨立的功能模組和類別。

## Contents

- `test_elderly_detector.py` - 長者語音檢測器測試
- `test_minnan_detector.py` - 閩南語檢測器測試

## Usage

執行所有單元測試：

```bash
pytest tests/unit/
```

執行特定測試檔案：

```bash
pytest tests/unit/test_elderly_detector.py
```

## Related Directories

- `services/asr/` - ASR 服務模組
- `tests/integration/` - 整合測試
