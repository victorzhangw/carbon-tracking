# 專案重組團隊指南

## 📢 重要通知

專案檔案結構已於 **2025-11-11** 完成重大重組，根目錄檔案從 150+ 個減少到 12 個核心檔案。本指南將幫助您快速適應新結構。

## 🎯 為什麼要重組？

### 問題

- 根目錄檔案過多（150+ 個），難以找到需要的檔案
- 文檔、腳本、測試散落各處，缺乏組織
- 新成員難以理解專案結構
- 維護困難，容易產生混淆

### 解決方案

- 按功能和性質分類所有檔案
- 建立清晰的目錄結構
- 制定檔案組織規範
- 完整記錄所有變更

## 🗺️ 如何找到常用檔案

### 我的檔案去哪了？

#### 配置檔案

**之前**: `requirements.txt`, `render.yaml`, `Dockerfile.*`  
**現在**: `config/` 目錄

- Python 依賴 → `config/requirements/`
- 部署配置 → `config/deployment/`
- API 規格 → `config/api_specs/`

#### 文檔

**之前**: 散落在根目錄  
**現在**: `docs/` 目錄

- 操作指南 → `docs/guides/`
- 技術文檔 → `docs/technical/`
- 分析報告 → `docs/reports/`
- 狀態記錄 → `docs/status/`

#### 腳本

**之前**: 各種 `.py` 和 `.bat` 檔案在根目錄  
**現在**: `scripts/` 目錄

- 資料生成 → `scripts/data_generation/`
- 資料處理 → `scripts/data_processing/`
- 驗證腳本 → `scripts/validation/`
- 啟動腳本 → `scripts/startup/`

#### 測試

**之前**: `test_*.py` 在根目錄  
**現在**: `tests/` 目錄

- 單元測試 → `tests/unit/`
- 整合測試 → `tests/integration/`
- 效能測試 → `tests/performance/`

#### 資源檔案

**之前**: `mockvoice/`, `genvoice/`, `*.db` 在根目錄  
**現在**:

- 音訊 → `assets/audio/`
- 圖片 → `assets/images/`
- 資料庫 → `data/databases/`
- 日誌 → `data/logs/`

#### 功能模組

**之前**: 各種功能檔案在根目錄  
**現在**: `modules/` 目錄

- 碳排放追蹤 → `modules/carbon_tracking/`
- 語音處理 → `modules/voice_processing/`
- ASR → `modules/asr/`
- 人才評鑑 → `modules/talent_assessment/`

## 📋 快速參考表

| 檔案類型         | 舊位置 | 新位置                        |
| ---------------- | ------ | ----------------------------- |
| requirements.txt | 根目錄 | config/requirements/base.txt  |
| render.yaml      | 根目錄 | config/deployment/render.yaml |
| 操作指南         | 根目錄 | docs/guides/                  |
| 技術文檔         | 根目錄 | docs/technical/               |
| 分析報告         | 根目錄 | docs/reports/                 |
| 資料生成腳本     | 根目錄 | scripts/data_generation/      |
| 驗證腳本         | 根目錄 | scripts/validation/           |
| 啟動批次檔       | 根目錄 | scripts/startup/              |
| 測試檔案         | 根目錄 | tests/ (按類型分類)           |
| 音訊檔案         | 根目錄 | assets/audio/                 |
| 資料庫檔案       | 根目錄 | data/databases/               |
| 功能模組         | 根目錄 | modules/                      |

## 🔧 如何適應新結構

### 1. 更新您的工作流程

#### 安裝依賴

```bash
# 之前
pip install -r requirements.txt

# 現在
pip install -r config/requirements/base.txt
# 或根據需要選擇其他依賴檔案
pip install -r config/requirements/full.txt
```

#### 執行腳本

```bash
# 之前
python generate_mock_carbon_data.py

# 現在
python scripts/data_generation/generate_mock_carbon_data.py
```

#### 執行測試

```bash
# 之前
pytest test_asr_api.py

# 現在
pytest tests/integration/test_asr_api.py
```

#### 啟動應用

```bash
# 之前
start_carbon_tracking.bat

# 現在
scripts\startup\start_carbon_tracking.bat
```

### 2. 更新您的 IDE 設定

#### VS Code

- 更新 `launch.json` 中的路徑
- 更新 `settings.json` 中的 Python 路徑
- 重新索引專案

#### PyCharm

- 標記 `tests/` 為測試根目錄
- 標記 `scripts/` 為源碼根目錄
- 重新建立執行配置

### 3. 更新您的文檔連結

如果您有個人筆記或文檔引用專案檔案：

- 使用 `FILE_MIGRATION_LOG.md` 查找檔案新位置
- 更新所有相對路徑
- 使用絕對路徑從專案根目錄開始

## ❓ 常見問題

### Q1: 我的程式碼會受影響嗎？

**A**: 核心應用程式碼（`app.py`, `routes/`, `services/` 等）位置未變，import 語句已更新。應用程式可以正常運行。

### Q2: 我需要重新 clone 專案嗎？

**A**: 不需要。只需 `git pull` 最新變更即可。

### Q3: 如果我找不到某個檔案怎麼辦？

**A**:

1. 查看 `FILE_MIGRATION_LOG.md` 找到檔案新位置
2. 使用 IDE 的全域搜尋功能
3. 查閱 `FILE_ORGANIZATION_STANDARD.md` 了解分類規則

### Q4: 我要新增檔案時應該放在哪裡？

**A**:

1. 查閱 `FILE_ORGANIZATION_STANDARD.md` 確定檔案類型
2. 根據功能和性質選擇對應目錄
3. 參考該目錄的 `README.md`
4. 不確定時詢問團隊

### Q5: 舊的檔案還能找回嗎？

**A**: 可以。

- 查看 `backups/pre-reorganization-*/` 備份
- 使用 `scripts/rollback.py` 回滾（不建議）
- 查看 Git 歷史記錄

### Q6: 部署會受影響嗎？

**A**: 不會。部署配置已更新，路徑引用已修正。測試確認所有功能正常。

### Q7: 我的分支會有衝突嗎？

**A**: 可能會。建議：

1. 先合併主分支到您的分支
2. 解決路徑相關的衝突
3. 參考 `FILE_MIGRATION_LOG.md` 更新路徑

### Q8: 為什麼有些檔案被歸檔了？

**A**: 過時或重複的檔案被移至 `archive/2025-11/`。查看 `archive/2025-11/README.md` 了解原因。

## 📚 重要文檔

### 必讀

- **FILE_ORGANIZATION_STANDARD.md** - 檔案組織規範（新增檔案前必讀）
- **FILE_MIGRATION_LOG.md** - 完整的檔案遷移記錄
- **PROJECT_REORGANIZATION_SNAPSHOT.md** - 重組狀態快照

### 參考

- **README.md** - 專案主說明（已更新）
- **docs/guides/quick_start.md** - 快速開始指南
- **scripts/rollback.py** - 緊急回滾腳本

## 🎓 最佳實踐

### 新增檔案時

1. ✅ 先查閱組織規範
2. ✅ 放在正確的目錄
3. ✅ 更新該目錄的 README（如需要）
4. ✅ 使用清晰的檔案名稱
5. ❌ 不要隨意放在根目錄

### 修改檔案時

1. ✅ 確認檔案位置正確
2. ✅ 更新相關文檔
3. ✅ 測試路徑引用
4. ❌ 不要移動檔案而不更新引用

### Code Review 時

1. ✅ 檢查新檔案位置是否正確
2. ✅ 檢查路徑引用是否更新
3. ✅ 確認符合組織規範
4. ✅ 提醒團隊成員遵循規範

## 🆘 需要幫助？

### 遇到問題時

1. 查閱本指南的常見問題
2. 查看 `FILE_ORGANIZATION_STANDARD.md`
3. 查看 `FILE_MIGRATION_LOG.md`
4. 詢問團隊成員
5. 提交 Issue 或聯繫專案負責人

### 回饋建議

如果您發現：

- 檔案放置不當
- 組織規範需要改進
- 文檔需要更新
- 有更好的組織方式

請隨時提出建議！

## 📅 時間表

- **2025-11-11**: 重組完成
- **2025-11-12**: 團隊適應期開始
- **2025-11-18**: 檢查點 - 確認團隊適應情況
- **2025-11-25**: 第一次定期檢查

## ✅ 檢查清單

完成以下項目以確保您已適應新結構：

- [ ] 閱讀本指南
- [ ] 閱讀 `FILE_ORGANIZATION_STANDARD.md`
- [ ] 更新本地專案（git pull）
- [ ] 測試應用程式啟動
- [ ] 更新 IDE 設定
- [ ] 更新個人筆記中的路徑
- [ ] 了解如何找到常用檔案
- [ ] 知道新增檔案時應該放在哪裡
- [ ] 知道遇到問題時如何尋求幫助

---

**感謝您的配合！** 這次重組將大幅提升我們的開發效率和專案可維護性。如有任何問題，請隨時聯繫團隊。
