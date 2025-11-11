# Carbon Tracking Module

## Purpose

碳排放追蹤模組提供社工訪視碳排放計算和管理功能。

## Contents

- `database_carbon_tracking.py` - 碳排放資料庫操作模組

## Related Components

- **Routes**: `routes/carbon_tracking.py` - Flask 路由處理
- **Templates**: `templates/carbon_tracking/` - 前端頁面模板
- **Database**: `data/databases/carbon_tracking.db` - 碳排放資料庫

## Usage

```python
from modules.carbon_tracking.database_carbon_tracking import (
    init_carbon_db,
    add_visit_record,
    get_all_visits
)

# 初始化資料庫
init_carbon_db()

# 新增訪視記錄
add_visit_record(
    worker_id="SW001",
    worker_name="張社工",
    transport_mode="機車",
    distance=10.5,
    visit_date="2025-11-11"
)

# 查詢所有訪視記錄
visits = get_all_visits()
```

## Features

- 訪視記錄管理（新增、編輯、刪除）
- 碳排放自動計算
- 統計報表生成
- 資料匯出功能
- 工號自動帶出姓名

## Database Schema

詳見 `database_carbon_tracking.py` 中的資料表定義。
