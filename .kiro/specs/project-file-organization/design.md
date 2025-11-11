# Design Document - Project File Organization

## Overview

本設計文檔定義了專案檔案重組的完整方案，將現有的 150+ 個根目錄檔案重新組織到清晰的目錄結構中。設計遵循「按功能分類、按性質分組」的原則，確保開發者能快速找到所需檔案，同時保持各子系統的獨立性。

### Design Goals

1. **清晰性**: 每個目錄的用途一目了然
2. **可維護性**: 新檔案有明確的存放位置
3. **可擴展性**: 支援未來新增子系統
4. **向後相容**: 不破壞現有功能
5. **可追溯性**: 完整記錄所有變更

## Architecture

### High-Level Directory Structure

```
project-root/
├── app.py                          # 主應用入口（保留）
├── config.py                       # 主配置檔（保留）
├── database.py                     # 資料庫核心（保留）
├── utils.py                        # 通用工具（保留）
├── auth.py                         # 認證模組（保留）
├── .gitignore                      # Git 配置（保留）
├── README.md                       # 專案主說明（新建）
│
├── config/                         # 配置檔案目錄
│   ├── requirements/              # 依賴管理
│   ├── deployment/                # 部署配置
│   └── api_specs/                 # API 規格
│
├── docs/                          # 文檔目錄
│   ├── guides/                    # 操作指南
│   ├── technical/                 # 技術文檔
│   ├── reports/                   # 分析報告
│   └── status/                    # 狀態記錄
│
├── scripts/                       # 工具腳本
│   ├── data_generation/          # 資料生成
│   ├── data_processing/          # 資料處理
│   ├── validation/               # 驗證腳本
│   ├── downloads/                # 下載工具
│   └── startup/                  # 啟動腳本
│
├── tests/                         # 測試目錄
│   ├── unit/                     # 單元測試
│   ├── integration/              # 整合測試
```

│ └── performance/ # 效能測試
│
├── assets/ # 靜態資源
│ ├── audio/ # 音訊檔案
│ └── images/ # 圖片檔案
│
├── data/ # 資料檔案
│ ├── databases/ # 資料庫檔案
│ └── logs/ # 日誌檔案
│
├── modules/ # 功能模組
│ ├── carbon_tracking/ # 碳排放追蹤
│ ├── voice_processing/ # 語音處理
│ ├── asr/ # 自動語音識別
│ └── talent_assessment/ # 人才評鑑
│
├── routes/ # Flask 路由（現有）
├── services/ # 服務層（現有）
├── templates/ # HTML 模板（現有）
├── static/ # 靜態資源（現有）
├── android_app/ # Android App（現有）
├── webpage/ # 前端專案（現有）
│
├── backups/ # 備份檔案（現有）
├── temp/ # 臨時檔案（現有）
├── archive/ # 歸檔檔案（新建）
│
├── 佐證資料/ # 稽核佐證（現有）
└── 期末報告/ # 期末報告（現有）

```

## Components and Interfaces

### 1. Configuration Management (config/)

**Purpose**: 集中管理所有配置檔案

**Structure**:
```

config/
├── requirements/
│ ├── base.txt # 基礎依賴
│ ├── voice.txt # 語音處理依賴
│ ├── asr.txt # ASR 依賴
│ ├── carbon.txt # 碳追蹤依賴
│ ├── full.txt # 完整依賴
│ └── minimal.txt # 最小依賴
├── deployment/
│ ├── render.yaml # Render 部署
│ ├── Dockerfile.voice-api # Docker 配置
│ └── nginx-voice.conf # Nginx 配置
└── api_specs/
├── gpt-sovits-api.json # GPT-SoVITS API
├── f5-tts-api.json # F5-TTS API
└── api_description.txt # API 說明

```

**Files to Move**:
- requirements*.txt → config/requirements/
- render.yaml, Dockerfile.*, nginx*.conf → config/deployment/
- *-api.json, api_description.txt → config/api_specs/

### 2. Documentation (docs/)

**Purpose**: 組織所有文檔，按類型分類

**Structure**:
```

docs/
├── guides/
│ ├── quick_start.md # 快速開始
│ ├── carbon_tracking_usage.md # 碳追蹤使用
│ ├── voice_clone_guide.md # 語音克隆指南
│ ├── android_app_build.md # Android 建置
│ └── deployment_guide.md # 部署指南
├── technical/
│ ├── architecture/
│ │ ├── system_architecture.md
│ │ └── system_architecture.svg
│ ├── backend/
│ │ └── backend_technical.md
│ ├── frontend/
│ │ └── frontend_technical.md
│ ├── voice/
│ │ ├── voice_separation_guide.md
│ │ ├── voice_dataset_validation.md
│ │ └── gpt_sovits_fine_tuning.md
│ └── asr/
│ ├── funasr_setup.md
│ └── funasr_manual_install.md
├── reports/
│ ├── ai_modules_architecture.md
│ ├── voice_data_processing.md
│ ├── noise_reduction_improvement.md
│ ├── module_testing.md
│ └── cleanup_summary.md
└── status/
├── completed/
│ ├── carbon_tracking_completed.md
│ ├── pwa_android_completed.md
│ └── ui_optimization_completed.md
└── deployment/
├── deployment_completed.md
└── deployment_issues.md

```

```

**Files to Move**:

Status Documents (emoji 開頭):

- ✅\*.md → docs/status/completed/
- 🎉*.md, 🎊*.md → docs/status/completed/
- 🔧\*.md → docs/status/deployment/
- 🌿\*.md → docs/status/completed/
- 📱\*.md → docs/status/completed/
- 🚀\*.md → docs/guides/

Technical Guides:

- \*\_GUIDE.md → docs/technical/voice/
- \*\_SETUP.md → docs/technical/voice/
- setup_asr_environment.md → docs/technical/asr/
- build_android_app.md → docs/guides/
- deploy_to_render.md → docs/guides/

Reports:

- \*\_REPORT.md → docs/reports/
- \*\_DOCUMENTATION.md → docs/technical/
- project-structure.md → docs/technical/architecture/

Usage Guides:

- 開始使用\_README.md → docs/guides/quick_start.md
- 碳排放追蹤系統\_使用說明.md → docs/guides/carbon_tracking_usage.md
- 快速參考卡.md → docs/guides/
- PWA 檢查清單.md → docs/guides/
- 部署檢查清單.md → docs/guides/
- 最終檢查清單.md → docs/guides/

### 3. Scripts (scripts/)

**Purpose**: 組織所有工具腳本，按用途分類

**Structure**:

```
scripts/
├── data_generation/
│   ├── generate_mock_carbon_data.py
│   ├── generate_carbon_emission_tables.py
│   ├── generate_carbon_dashboard_images.py
│   ├── generate_epa_document_images.py
│   └── generate_pwa_icons.py
├── data_processing/
│   ├── update_social_worker_names.py
│   ├── update_names_extended.py
│   ├── add_more_social_workers.py
│   ├── process_03041966_audio.py
│   ├── process_advanced_03041966.py
│   ├── process_natural_03041966.py
│   ├── advanced_voice_separation.py
│   ├── audio_voice_separation.py
│   ├── natural_voice_separation.py
│   ├── optimized_natural_voice_separation.py
│   └── volume_balanced_voice_separation.py
├── validation/
│   ├── check_audio_files.py
│   ├── check_emotion_methods.py
│   ├── check_social_worker_names.py
│   ├── final_tag_validation.py
│   ├── batch_validation_processor.py
│   ├── voice_dataset_validation_system.py
│   ├── dataset_validation_dashboard.py
│   └── talent_assessment_query_validator.py
├── downloads/
│   ├── download_epa_document.py
│   └── download_funasr_model.py
├── monitoring/
│   ├── monitor_deployment.py
│   ├── show_all_workers_stats.py
│   └── debug_voice_models.py
└── startup/
    ├── start_carbon_tracking.bat
    ├── start-gpt-sovits.bat
    ├── start-voice-api.bat
    ├── start-voice-clone-service.bat
    ├── setup-voice-system.bat
    ├── install-gpt-sovits.bat
    └── test_pwa_features.bat
```

**Files to Move**:

- generate\_\*.py → scripts/data_generation/
- update*\*.py, add*\_.py, process\_\_.py → scripts/data_processing/
- \*\_voice_separation.py → scripts/data_processing/
- check\__.py, _\_validation\*.py → scripts/validation/
- download\_\*.py → scripts/downloads/
- monitor*\*.py, show*\_.py, debug\_\_.py → scripts/monitoring/
- \*.bat → scripts/startup/

### 4. Tests (tests/)

**Purpose**: 集中管理所有測試腳本

**Structure**:

```
tests/
├── unit/
│   ├── test_elderly_detector.py
│   ├── test_minnan_detector.py
│   └── test_emotion_methods.py
├── integration/
│   ├── test_asr_coordinator.py
│   ├── test_funasr_engine.py
│   ├── test_asr_api.py
│   ├── test_carbon_system.py
│   └── test_minimal_app.py
├── performance/
│   ├── test_asr_performance.py
│   └── test_asr_setup.py
└── deployment/
    ├── test_deployment.py
    └── test_pwa.html
```

**Files to Move**:

- test\_\*.py → tests/ (按類型分類)
- test_pwa.html → tests/deployment/

### 5. Assets (assets/)

**Purpose**: 管理所有靜態資源檔案

**Structure**:

```
assets/
├── audio/
│   ├── mockvoice/                # 模擬語音
│   ├── genvoice/                 # 生成語音
│   ├── uploads/                  # 上傳音訊
│   ├── tts/                      # TTS 輸出
│   └── voice_output/             # 語音輸出
└── images/
    ├── icons/                    # 圖示檔案
    └── screenshots/              # 系統截圖
```

**Files to Move**:

- mockvoice/ → assets/audio/mockvoice/
- genvoice/ → assets/audio/genvoice/
- audio_uploads/ → assets/audio/uploads/
- TTS/ → assets/audio/tts/
- voice_output/ → assets/audio/voice_output/
- static/icons/ → assets/images/icons/ (保留 static/icons 的符號連結)

### 6. Data (data/)

**Purpose**: 管理資料庫和日誌檔案

**Structure**:

```
data/
├── databases/
│   ├── carbon_tracking.db
│   ├── customer_service.db
│   └── README.md
└── logs/
    ├── voice_dataset_validation.log
    └── README.md
```

**Files to Move**:

- \*.db (非備份) → data/databases/
- \*.log → data/logs/
- carbon*tracking_backup*\*.db → backups/databases/

### 7. Modules (modules/)

**Purpose**: 組織功能模組，支援子系統獨立開發

**Structure**:

```
modules/
├── carbon_tracking/
│   ├── README.md
│   ├── database_carbon_tracking.py
│   └── routes/ → ../../routes/carbon_tracking.py (參考)
├── voice_processing/
│   ├── README.md
│   ├── voice_clone_service.py
│   ├── voice_synthesis_service.py
│   ├── simple_voice_api.py
│   └── voice_config.py
├── asr/
│   ├── README.md
│   └── services/ → ../../services/asr/ (參考)
└── talent_assessment/
    ├── README.md
    ├── talent_assessment_db_connector.py
    ├── talent_assessment_llm_query_generator.py
    └── talent_assessment_query_validator.py
```

**Files to Move**:

- database_carbon_tracking.py → modules/carbon_tracking/
- voice\_\*.py → modules/voice_processing/
- talent*assessment*\*.py → modules/talent_assessment/
- database_emotion_extension.py → modules/voice_processing/

### 8. Archive (archive/)

**Purpose**: 歸檔過時或重複的檔案

**Structure**:

```
archive/
├── 2025-11/
│   ├── README.md                 # 說明歸檔原因
│   ├── old_requirements/
│   ├── old_docs/
│   └── old_scripts/
└── README.md
```

**Candidates for Archiving**:

- requirements_250521.txt (舊版依賴)
- requirements_backup.txt (備份檔)
- emotion_color_guide.md (可能過時)
- validate_vue_component.js (單一檔案，可能測試用)
- Gpt-Sovis-API.docx (有 .md 版本)
- 給 VB3-_.docx, 給 VC2-_.docx (已有對應 .md 報告)

## Data Models

### File Metadata Structure

每個移動的檔案都會記錄以下資訊：

```python
{
    "original_path": "test_asr_api.py",
    "new_path": "tests/integration/test_asr_api.py",
    "category": "test",
    "subcategory": "integration",
    "moved_at": "2025-11-11T12:00:00",
    "reason": "Consolidate all test files",
    "dependencies": ["routes/asr.py", "services/asr/coordinator.py"]
}
```

### Directory Metadata

每個新目錄都會包含 README.md：

```markdown
# [Directory Name]

## Purpose

[目錄用途說明]

## Contents

[內容說明]

## Usage

[使用方式]

## Related Directories

[相關目錄]
```

## Error Handling

### Migration Safety Measures

1. **Pre-Migration Backup**

   - 建立完整專案備份到 `backups/pre-reorganization-[timestamp]/`
   - 記錄當前 git commit hash

2. **Dependency Validation**

   - 掃描所有 Python 檔案的 import 語句
   - 建立依賴關係圖
   - 識別需要更新的路徑引用

3. **Incremental Migration**

   - 按類別逐步移動檔案
   - 每個類別完成後執行測試
   - 確認無錯誤後再進行下一類別

4. **Rollback Mechanism**
   - 提供 rollback.py 腳本
   - 可根據 migration_log.json 還原所有變更
   - 保留原始檔案的 git 歷史

### Error Detection

1. **Import Path Errors**

   - 移動後執行 `python -m py_compile` 檢查語法
   - 執行基本測試確認 import 正常

2. **Missing Files**

   - 比對移動前後的檔案清單
   - 確保沒有檔案遺失

3. **Broken References**
   - 檢查 HTML 模板中的靜態資源路徑
   - 檢查配置檔中的檔案路徑
   - 檢查文檔中的相對連結

## Testing Strategy

### Phase 1: Pre-Migration Testing

1. 執行現有所有測試，記錄基準結果
2. 記錄當前專案狀態（檔案清單、git status）

### Phase 2: Migration Testing

1. 每移動一個類別後，執行相關測試
2. 檢查 import 語句是否正常
3. 驗證應用程式啟動無誤

### Phase 3: Post-Migration Testing

1. 執行完整測試套件
2. 手動測試核心功能：
   - 碳排放追蹤系統
   - 語音處理功能
   - ASR 功能
3. 檢查文檔連結是否正常
4. 驗證部署配置是否正確

### Test Checklist

```markdown
- [ ] app.py 正常啟動
- [ ] 碳排放追蹤頁面可訪問
- [ ] 所有 API 端點正常回應
- [ ] 測試腳本可正常執行
- [ ] 文檔連結無 404
- [ ] 靜態資源載入正常
- [ ] 資料庫連接正常
- [ ] 配置檔案讀取正常
```

## Implementation Phases

### Phase 1: Preparation (準備階段)

1. 建立完整備份
2. 建立新目錄結構
3. 生成檔案分類清單
4. 建立 migration_log.json

### Phase 2: Configuration Files (配置檔案)

1. 移動 requirements\*.txt
2. 移動部署配置檔
3. 移動 API 規格檔
4. 更新相關引用

### Phase 3: Documentation (文檔)

1. 移動技術文檔
2. 移動操作指南
3. 移動狀態記錄
4. 移動報告檔案
5. 更新文檔內部連結

### Phase 4: Scripts (腳本)

1. 移動工具腳本
2. 移動測試腳本
3. 更新腳本中的路徑引用
4. 測試腳本執行

### Phase 5: Assets & Data (資源與資料)

1. 移動音訊檔案
2. 移動資料庫檔案
3. 移動日誌檔案
4. 更新路徑配置

### Phase 6: Modules (模組)

1. 移動功能模組檔案
2. 更新 import 語句
3. 測試模組功能
4. 建立模組 README

### Phase 7: Archiving (歸檔)

1. 識別過時檔案
2. 移動到 archive/
3. 建立歸檔說明

### Phase 8: Documentation & Validation (文檔與驗證)

1. 建立 FILE_ORGANIZATION_STANDARD.md
2. 建立 FILE_MIGRATION_LOG.md
3. 更新主 README.md
4. 執行完整測試
5. 建立 rollback 腳本

## Rollback Plan

如果重組過程出現問題，可以使用以下步驟回滾：

1. **使用 Git 回滾**

   ```bash
   git reset --hard [commit-hash]
   ```

2. **使用備份還原**

   ```bash
   python scripts/rollback.py --backup backups/pre-reorganization-[timestamp]
   ```

3. **手動還原**
   - 參考 FILE_MIGRATION_LOG.md
   - 逐一還原檔案位置

## Success Criteria

重組成功的標準：

1. ✅ 所有檔案都有明確的分類和位置
2. ✅ 根目錄檔案數量減少 80% 以上
3. ✅ 所有測試通過
4. ✅ 應用程式正常啟動和運行
5. ✅ 文檔連結全部有效
6. ✅ 有完整的遷移記錄
7. ✅ 有清晰的組織規範文檔
8. ✅ 團隊成員理解新結構
