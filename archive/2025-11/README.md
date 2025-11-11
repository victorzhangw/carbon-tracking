# Archive - November 2025

## Overview

本目錄包含在 2025 年 11 月專案檔案重組過程中歸檔的過時檔案。這些檔案已不再使用，但保留以供未來參考。

## Archiving Date

- **歸檔日期**: 2025-11-11
- **執行者**: 專案檔案重組任務 (Task 9)
- **相關任務**: `.kiro/specs/project-file-organization/tasks.md` - Task 9

## Archived Files

### Old Requirements (old_requirements/)

過時的依賴配置檔案，已被新的配置系統取代（位於 `config/requirements/`）。

#### requirements_250521.txt

- **歸檔原因**: 過時的 requirements 檔案，日期為 2021 年 5 月
- **替代方案**: 使用 `config/requirements/base.txt` 和其他模組化的 requirements 檔案
- **決策依據**: 檔案名稱包含舊日期，內容已過時且不完整
- **恢復方式**: 如需查看歷史依賴，可參考此檔案，但不建議使用

#### requirements_backup.txt

- **歸檔原因**: 備份的 requirements 檔案
- **替代方案**: 使用 `config/requirements/` 下的模組化配置
- **決策依據**: 檔案名稱標示為 backup，且內容與當前需求不符
- **恢復方式**: 如需恢復，複製到專案根目錄並重新命名

#### requirements_audio_separation.txt

- **歸檔原因**: 音訊分離專用的依賴配置
- **替代方案**: 相關依賴已整合到 `config/requirements/voice.txt`
- **決策依據**: 功能已整合到主要的語音處理模組中
- **恢復方式**: 如需單獨的音訊分離環境，可參考此檔案

### Old Scripts (old_scripts/)

不再使用的腳本檔案。

#### validate_vue_component.js

- **歸檔原因**: 單一用途的 Vue 組件驗證腳本，已不再需要
- **替代方案**: 使用前端專案的標準測試工具
- **決策依據**:
  - 僅針對單一組件 `VoiceInteractionContainer.vue`
  - 功能過於特定，不具通用性
  - 前端專案有更完善的測試機制
- **恢復方式**: 如需恢復，複製到 `scripts/validation/` 並更新目標路徑

### Old Documentation (old_docs/)

重複或過時的文檔檔案。

#### Gpt-Sovis-API.docx

- **歸檔原因**: 重複的文檔，已有 Markdown 版本
- **替代方案**: 使用 `config/api_specs/Gpt-Sovis-API.md`
- **決策依據**:
  - Markdown 格式更適合版本控制
  - 內容相同，保留一份即可
  - Markdown 版本更易於維護和查看
- **恢復方式**: 如需 Word 格式，可從 Markdown 轉換

#### 給 VB3-1 優化後模型成效比較報告.docx

- **歸檔原因**: 重複的報告文檔
- **替代方案**: 使用 `docs/reports/優化後模型成效比較報告.md`
- **決策依據**:
  - 期末報告目錄中有完整版本
  - Markdown 版本內容更完整且持續更新
  - Word 格式不便於版本控制
- **恢復方式**: 如需 Word 格式，參考 `期末報告/01_優化後模型成效比較報告/`

#### 給 VB3-2 【菁宸】專業系統驗證及 ASR 改進整合報告.docx

- **歸檔原因**: 重複的報告文檔
- **替代方案**: 使用 `docs/reports/專業系統驗證及ASR改進整合報告.md`
- **決策依據**:
  - 期末報告目錄中有完整版本
  - Markdown 版本內容更完整
  - 檔案名稱包含特定人名，不適合作為正式文檔
- **恢復方式**: 如需 Word 格式，參考 `期末報告/02_專業系統驗證及ASR改進整合報告/`

#### 給 VC2-2 推廣成果摘要報告.docx

- **歸檔原因**: 重複的報告文檔
- **替代方案**: 使用 `docs/reports/推廣成果摘要報告.md`
- **決策依據**:
  - 期末報告目錄中有完整版本
  - Markdown 版本更易於維護
- **恢復方式**: 如需 Word 格式，參考 `期末報告/03_推廣成果摘要報告/`

#### 給 VC2-3 碳排放減少效益分析.docx

- **歸檔原因**: 重複的報告文檔
- **替代方案**: 使用 `docs/reports/碳排放減少效益分析.md`
- **決策依據**:
  - 期末報告目錄中有完整版本
  - Markdown 版本內容更完整且持續更新
- **恢復方式**: 如需 Word 格式，參考 `期末報告/04_碳排放減少效益分析報告/`

## Statistics

- **總歸檔檔案數**: 9
- **Requirements 檔案**: 3
- **腳本檔案**: 1
- **文檔檔案**: 5 (1 API 文檔 + 4 報告)

## Decision Criteria

檔案被歸檔的主要原因：

1. **過時版本**: 檔案名稱或內容顯示為舊版本
2. **重複內容**: 存在更新或更完整的版本
3. **格式問題**: Word 格式不適合版本控制，已有 Markdown 版本
4. **功能整合**: 功能已整合到其他模組中
5. **特定用途**: 過於特定的工具，不具通用性

## How to Restore

如需恢復歸檔的檔案：

1. **查看檔案**: 直接在 `archive/2025-11/` 目錄中查看
2. **複製檔案**: 將檔案複製到原始位置或新位置
3. **更新引用**: 如果檔案被其他檔案引用，需要更新路徑
4. **檢查依賴**: 確認檔案的依賴關係是否仍然有效

## Related Documentation

- **檔案組織規範**: `FILE_ORGANIZATION_STANDARD.md`
- **遷移日誌**: `migration_log.json`
- **專案任務**: `.kiro/specs/project-file-organization/tasks.md`

## Notes

- 歸檔的檔案不會被刪除，可隨時查閱
- 建議定期檢查歸檔檔案，超過 2 年未使用的可考慮永久刪除
- 如有疑問，請參考 `migration_log.json` 中的詳細記錄
