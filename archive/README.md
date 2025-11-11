# Archive Directory

## Purpose

本目錄用於存放已過時、重複或不再使用的專案檔案。歸檔的檔案不會被刪除，以便未來需要時可以查閱或恢復。

## Archiving Policy

### 何時歸檔檔案

檔案應該被歸檔的情況：

1. **過時的版本**: 當有新版本的檔案時，舊版本應該被歸檔
2. **重複的檔案**: 當存在功能相同但格式不同的檔案時（如 .md 和 .docx）
3. **備份檔案**: 帶有日期後綴或 "backup" 字樣的檔案
4. **實驗性檔案**: 測試或實驗用途的檔案，已不再使用
5. **已整合的檔案**: 內容已被整合到其他檔案中的文檔

### 歸檔流程

1. 確認檔案確實不再需要
2. 將檔案移動到對應的 archive/[YYYY-MM]/ 子目錄
3. 在該月份的 README.md 中記錄歸檔原因
4. 更新 migration_log.json（如適用）

## Directory Structure

```
archive/
├── README.md                    # 本檔案
└── YYYY-MM/                     # 按月份組織
    ├── README.md                # 該月份的歸檔記錄
    ├── old_requirements/        # 過時的依賴配置
    ├── old_docs/                # 過時的文檔
    ├── old_scripts/             # 過時的腳本
    └── old_configs/             # 過時的配置檔
```

## How to Restore Archived Files

如需恢復歸檔的檔案：

1. 查閱對應月份的 README.md，確認檔案的原始位置
2. 將檔案從 archive/ 複製回原位置
3. 檢查是否需要更新相關的引用或依賴

## Notes

- 歸檔的檔案不應該被其他檔案引用
- 定期檢查歸檔檔案，超過 2 年未使用的可考慮永久刪除
- 重要的歷史文檔應該保留，即使已過時
