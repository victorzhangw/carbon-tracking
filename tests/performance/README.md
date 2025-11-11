# Performance Tests

## Purpose

此目錄包含所有效能測試，用於測試系統的效能和回應時間。

## Contents

- `test_asr_performance.py` - ASR 系統效能測試
- `test_asr_setup.py` - ASR 設定和初始化測試

## Usage

執行所有效能測試：

```bash
pytest tests/performance/
```

執行特定測試檔案：

```bash
pytest tests/performance/test_asr_performance.py
```

## Related Directories

- `services/asr/` - ASR 服務模組
- `tests/integration/` - 整合測試
