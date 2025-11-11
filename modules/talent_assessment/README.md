# Talent Assessment Module

## Purpose

人才評鑑模組提供基於 LLM 的智能查詢生成和資料庫連接功能，用於人才評估和分析。

## Contents

- `talent_assessment_db_connector.py` - 資料庫連接器
- `talent_assessment_llm_query_generator.py` - LLM 查詢生成器
- `talent_assessment_query_validator.py` - 查詢驗證器

## Usage

### Database Connection

```python
from modules.talent_assessment.talent_assessment_db_connector import TalentAssessmentDB

# 初始化資料庫連接
db = TalentAssessmentDB()

# 執行查詢
results = db.execute_query("SELECT * FROM assessments")
```

### LLM Query Generation

```python
from modules.talent_assessment.talent_assessment_llm_query_generator import generate_query

# 使用自然語言生成 SQL 查詢
query = generate_query(
    natural_language="找出所有評分超過 80 分的候選人"
)

print(query)  # 生成的 SQL 查詢
```

### Query Validation

```python
from modules.talent_assessment.talent_assessment_query_validator import validate_query

# 驗證查詢安全性
is_valid, message = validate_query(
    query="SELECT * FROM assessments WHERE score > 80"
)

if is_valid:
    # 執行查詢
    pass
else:
    print(f"查詢驗證失敗: {message}")
```

## Features

- **LLM 驅動查詢**: 使用自然語言生成 SQL 查詢
- **查詢驗證**: 確保查詢安全性和正確性
- **資料庫抽象**: 簡化資料庫操作
- **人才評估**: 支援多維度人才評估

## Database Schema

人才評鑑資料庫包含以下主要資料表：

- `assessments` - 評估記錄
- `candidates` - 候選人資訊
- `criteria` - 評估標準
- `scores` - 評分記錄

詳細資料庫設計請參考 `期末報告/人才評鑑系統資料庫設計.md`

## Security

- SQL 注入防護
- 查詢白名單驗證
- 參數化查詢
- 權限控制

## Technical Documentation

詳細技術文檔請參考：

- `期末報告/人才評鑑系統/` - 人才評鑑系統文檔
- `scripts/validation/talent_assessment_query_validator.py` - 驗證腳本（已移動）
