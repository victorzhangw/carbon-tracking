# 專案重組工具和記錄

## 目的

本目錄包含 2025-11 專案檔案重組過程中使用的工具腳本和生成的記錄檔案。

## 內容

### 重組工具腳本

- `prepare_reorganization.py` - 準備重組的主要腳本
- `generate_file_classification.py` - 生成檔案分類報告
- `test_config_migration.py` - 測試配置檔案遷移
- `test_resource_migration.py` - 測試資源檔案遷移
- `update_migration_log_archive.py` - 更新歸檔遷移日誌
- `update_migration_log_docs.py` - 更新文檔遷移日誌

### 記錄檔案

- `migration_log.json` - 完整的檔案遷移記錄（JSON 格式）
- `file_classification_report.json` - 檔案分類報告（JSON 格式）
- `FILE_CLASSIFICATION_REPORT.md` - 檔案分類報告（Markdown 格式）
- `doc_links_update_log.json` - 文檔連結更新記錄

## 歸檔原因

這些檔案是專案重組過程中的臨時工具和記錄，重組完成後不再需要在根目錄中保留。歸檔以便：

1. 保留重組過程的完整記錄
2. 未來需要時可以參考
3. 保持根目錄整潔

## 歸檔日期

2025-11-11

## 相關文檔

- 主要遷移記錄：`/FILE_MIGRATION_LOG.md`
- 組織規範：`/FILE_ORGANIZATION_STANDARD.md`
- 回滾腳本：`/scripts/rollback.py`
