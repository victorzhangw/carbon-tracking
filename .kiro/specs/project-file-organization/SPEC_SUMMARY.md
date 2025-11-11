# 專案檔案組織規範 - Spec 總結

## 📋 Spec 概覽

**Spec 名稱**: Project File Organization (專案檔案組織)  
**建立日期**: 2025-11-11  
**狀態**: 規劃完成，待執行

## 🎯 目標

將專案根目錄的 150+ 個檔案重新組織到清晰的目錄結構中，建立一套可持續的檔案組織規範，提升專案的可維護性和可讀性。

## 📊 現狀分析

### 當前問題

- 根目錄包含 150+ 個檔案，難以查找和管理
- 檔案類型混雜：源碼、文檔、測試、配置、資源等
- 缺乏統一的檔案組織標準
- 多個子系統（碳排放追蹤、語音處理、ASR、Android App）的檔案混在一起
- 存在大量狀態記錄文檔（emoji 開頭的 .md 檔案）
- 有過時或重複的檔案需要歸檔

### 專案組成

- **核心系統**: Flask Web 應用（碳排放追蹤為主）
- **子系統**:
  - 碳排放追蹤系統
  - 語音處理系統（語音克隆、合成）
  - ASR 系統（雙引擎：Whisper + FunASR）
  - 人才評鑑系統
  - Android App
  - 前端專案（Vue.js）

## 🏗️ 設計方案

### 新目錄結構

```
project-root/
├── config/          # 配置檔案（requirements, deployment, api_specs）
├── docs/            # 文檔（guides, technical, reports, status）
├── scripts/         # 工具腳本（按用途分類）
├── tests/           # 測試（unit, integration, performance, deployment）
├── assets/          # 靜態資源（audio, images）
├── data/            # 資料檔案（databases, logs）
├── modules/         # 功能模組（carbon_tracking, voice_processing, asr, talent_assessment）
├── archive/         # 歸檔檔案
└── [現有目錄]       # routes/, services/, templates/, static/, android_app/, webpage/ 等
```

### 核心原則

1. **按功能分類**: 相同功能的檔案放在一起
2. **按性質分組**: 配置、文檔、腳本、測試等分開存放
3. **支援子系統**: 每個子系統有獨立的模組目錄
4. **保持簡潔**: 根目錄只保留核心檔案
5. **可追溯性**: 完整記錄所有變更

## 📝 主要文檔

### 1. Requirements (需求文檔)

- 位置: `.kiro/specs/project-file-organization/requirements.md`
- 內容: 10 個主要需求，涵蓋檔案分類、文檔組織、測試管理等
- 格式: EARS + INCOSE 標準

### 2. Design (設計文檔)

- 位置: `.kiro/specs/project-file-organization/design.md`
- 內容:
  - 完整的目錄結構設計
  - 8 個主要組件的詳細說明
  - 檔案移動對照表
  - 安全遷移機制
  - 錯誤處理策略
  - 測試策略
  - 8 個實施階段

### 3. Tasks (任務清單)

- 位置: `.kiro/specs/project-file-organization/tasks.md`
- 內容: 12 個主要任務，60+ 個子任務
- 所有任務都是必需的（包括測試任務）

### 4. FILE_ORGANIZATION_STANDARD.md (組織規範)

- 位置: 專案根目錄
- 內容:
  - 完整的目錄結構說明
  - 檔案分類規則表格
  - 命名規範
  - 決策流程圖
  - 最佳實踐
  - 常見問題解答

## 🔢 統計資訊

### 檔案分類統計（預估）

| 類別     | 數量    | 目標位置 |
| -------- | ------- | -------- |
| 配置檔案 | 15+     | config/  |
| 文檔檔案 | 60+     | docs/    |
| 腳本檔案 | 30+     | scripts/ |
| 測試檔案 | 15+     | tests/   |
| 資源檔案 | 5+ 目錄 | assets/  |
| 資料檔案 | 5+      | data/    |
| 模組檔案 | 10+     | modules/ |
| 歸檔檔案 | 5+      | archive/ |

### 預期成果

- ✅ 根目錄檔案數量減少 **80%+**
- ✅ 所有檔案都有明確的分類
- ✅ 建立完整的組織規範文檔
- ✅ 所有變更都有記錄
- ✅ 提供回滾機制

## 🚀 執行計劃

### 12 個主要任務

1. **準備階段**: 建立備份和基礎結構
2. **生成分類清單**: 分析所有檔案並建立對照表
3. **移動配置檔案**: requirements, deployment, api_specs
4. **移動文檔檔案**: guides, technical, reports, status
5. **移動腳本檔案**: 按用途分類到 scripts/
6. **移動測試檔案**: 按類型分類到 tests/
7. **移動資源和資料**: assets/, data/
8. **組織功能模組**: modules/
9. **歸檔過時檔案**: archive/
10. **建立規範文檔**: FILE_ORGANIZATION_STANDARD.md 等
11. **執行完整測試**: 確保功能正常
12. **最終清理**: 更新文檔、建立 commit

### 安全措施

1. **完整備份**: 移動前建立專案備份
2. **增量遷移**: 按類別逐步移動，每步驗證
3. **依賴追蹤**: 掃描並更新所有 import 語句
4. **測試驗證**: 每個階段完成後執行測試
5. **回滾機制**: 提供 rollback.py 腳本

## 📈 預期效益

### 短期效益

- 根目錄整潔，易於導航
- 檔案查找時間大幅減少
- 新成員更容易理解專案結構

### 長期效益

- 統一的檔案組織標準
- 更好的可維護性
- 支援多子系統獨立開發
- 減少檔案管理的認知負擔

## 🎯 成功標準

- [x] 需求文檔完成並獲得批准
- [x] 設計文檔完成並獲得批准
- [x] 任務清單完成並獲得批准
- [x] 組織規範文檔建立
- [ ] 所有檔案成功移動到新位置
- [ ] 所有測試通過
- [ ] 應用程式正常運行
- [ ] 文檔連結全部有效
- [ ] 團隊成員理解新結構

## 📚 相關文檔

- [Requirements](requirements.md)
- [Design](design.md)
- [Tasks](tasks.md)
- [FILE_ORGANIZATION_STANDARD.md](../../../FILE_ORGANIZATION_STANDARD.md)

## 🔄 下一步

1. **開始執行任務**: 從任務 1 開始，逐步完成所有任務
2. **定期檢查點**: 每完成一個主要任務，進行檢查和驗證
3. **團隊溝通**: 完成後向團隊說明新結構
4. **持續改進**: 根據使用反饋調整規範

---

**建立者**: Kiro AI  
**建立日期**: 2025-11-11  
**最後更新**: 2025-11-11
