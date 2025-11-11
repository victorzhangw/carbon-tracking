# Deployment Tests

## Purpose

此目錄包含所有部署測試，用於測試應用程式的部署配置和 PWA 功能。

## Contents

- `test_deployment.py` - 部署配置測試
- `test_pwa.html` - PWA 功能測試頁面

## Usage

執行所有部署測試：

```bash
pytest tests/deployment/
```

測試 PWA 功能：
在瀏覽器中開啟 `test_pwa.html` 進行手動測試。

## Related Directories

- `config/deployment/` - 部署配置檔案
- `static/` - 靜態資源（包含 PWA 檔案）
