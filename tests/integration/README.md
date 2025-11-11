# Integration Tests

## Purpose

此目錄包含所有整合測試，用於測試多個模組之間的協作和系統整合。

## Contents

- `test_asr_coordinator.py` - ASR 協調器整合測試
- `test_funasr_engine.py` - FunASR 引擎整合測試
- `test_asr_api.py` - ASR API 端點測試
- `test_carbon_system.py` - 碳排放追蹤系統測試
- `test_minimal_app.py` - 最小應用程式測試

## Usage

執行所有整合測試：

```bash
pytest tests/integration/
```

執行特定測試檔案：

```bash
pytest tests/integration/test_asr_coordinator.py
```

## Related Directories

- `routes/` - Flask 路由
- `services/` - 服務層
- `tests/unit/` - 單元測試
