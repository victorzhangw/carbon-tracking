# Requirements Document

## Introduction

本專案是一個多功能的 AI 客服系統，包含碳排放追蹤、語音處理、ASR（自動語音識別）、Android App 等多個子系統。隨著專案發展，根目錄累積了大量不同性質的檔案，包括源碼、文檔、測試腳本、部署配置、報告等，導致檔案結構混亂，難以維護和查找。需要建立一套清晰的檔案組織規範，將所有檔案依據功能、性質和格式重新分類，並記錄為未來的開發規範。

## Glossary

- **System**: 指本專案的檔案組織系統
- **Root Directory**: 專案根目錄
- **Source Code**: 可執行的 Python、JavaScript、Kotlin 等程式碼檔案
- **Documentation**: 說明文件，包括 .md、.txt、.docx 等格式
- **Configuration**: 配置檔案，包括 requirements.txt、.json、.yaml 等
- **Test Script**: 測試用的 Python 腳本，通常以 test\_ 開頭
- **Utility Script**: 工具腳本，用於資料處理、生成、檢查等一次性任務
- **Deployment Artifact**: 部署相關檔案，包括 Dockerfile、nginx 配置等
- **Report**: 正式報告文件，通常為 .md 或 .docx 格式
- **Asset**: 靜態資源，包括圖片、音訊、資料庫檔案等
- **Temporary File**: 臨時或過時的檔案，可能需要歸檔或刪除

## Requirements

### Requirement 1

**User Story:** 作為開發者，我希望所有源碼檔案按照功能模組分類存放，以便快速找到需要修改的程式碼

#### Acceptance Criteria

1. WHEN 開發者查看專案結構時，THE System SHALL 將所有 Python 源碼檔案（非測試、非工具腳本）組織在對應的功能目錄中（如 routes/、services/、database/ 等）
2. THE System SHALL 將所有前端相關源碼（HTML、CSS、JavaScript）存放在 templates/ 和 static/ 目錄中
3. THE System SHALL 將 Android App 相關的所有檔案（包括 Kotlin、Gradle、資源檔）保持在 android_app/ 目錄中
4. THE System SHALL 確保根目錄不包含任何功能性源碼檔案（app.py、config.py 等核心檔案除外）

### Requirement 2

**User Story:** 作為開發者，我希望所有文檔按照類型和用途分類，以便快速找到相關說明

#### Acceptance Criteria

1. THE System SHALL 將所有技術文檔（架構、API、指南）存放在 docs/ 目錄中
2. THE System SHALL 將所有正式報告（期末報告、分析報告）存放在 reports/ 或 期末報告/ 目錄中
3. THE System SHALL 將所有操作指南和快速開始文檔存放在 guides/ 目錄中
4. WHEN 文檔使用 emoji 開頭時，THE System SHALL 將其識別為狀態文檔或完成記錄，並存放在 docs/status/ 目錄中
5. THE System SHALL 將所有 README 類型的文檔保留在其對應的功能目錄中

### Requirement 3

**User Story:** 作為開發者，我希望所有測試腳本集中管理，以便執行測試和維護測試程式碼

#### Acceptance Criteria

1. THE System SHALL 將所有以 test\_ 開頭的 Python 檔案移動到 tests/ 目錄中
2. THE System SHALL 在 tests/ 目錄下按照測試類型建立子目錄（如 tests/unit/、tests/integration/、tests/performance/）
3. THE System SHALL 將測試相關的配置檔案（如 pytest.ini）存放在 tests/ 目錄中
4. THE System SHALL 確保測試腳本的命名清楚表明其測試的功能模組

### Requirement 4

**User Story:** 作為開發者，我希望所有工具腳本按照用途分類，以便找到資料處理或系統維護工具

#### Acceptance Criteria

1. THE System SHALL 將所有資料生成腳本（generate\_\*.py）存放在 scripts/data_generation/ 目錄中
2. THE System SHALL 將所有資料檢查和驗證腳本（check*\*.py、validate*\*.py）存放在 scripts/validation/ 目錄中
3. THE System SHALL 將所有資料更新和處理腳本（update*\*.py、process*\*.py）存放在 scripts/data_processing/ 目錄中
4. THE System SHALL 將所有下載腳本（download\_\*.py）存放在 scripts/downloads/ 目錄中
5. THE System SHALL 將所有批次檔（.bat）存放在 scripts/startup/ 目錄中

### Requirement 5

**User Story:** 作為開發者，我希望所有配置檔案集中管理，以便快速調整系統設定

#### Acceptance Criteria

1. THE System SHALL 將所有 requirements\*.txt 檔案存放在 config/requirements/ 目錄中
2. THE System SHALL 將所有部署配置檔（render.yaml、Dockerfile、nginx.conf）存放在 config/deployment/ 目錄中
3. THE System SHALL 將所有 API 規格檔（.json、.yaml）存放在 config/api_specs/ 目錄中
4. THE System SHALL 保留根目錄的主要配置檔（如 config.py、.gitignore）
5. THE System SHALL 將環境相關的配置檔（.env、local.properties）保留在根目錄或對應的子專案目錄中

### Requirement 6

**User Story:** 作為開發者，我希望所有靜態資源和資料檔案按照類型組織，以便管理專案資產

#### Acceptance Criteria

1. THE System SHALL 將所有音訊檔案存放在 assets/audio/ 目錄中，並按照用途建立子目錄（如 mockvoice/、genvoice/、uploads/）
2. THE System SHALL 將所有圖片檔案存放在 assets/images/ 目錄中
3. THE System SHALL 將所有資料庫檔案（.db）存放在 data/databases/ 目錄中
4. THE System SHALL 將所有備份檔案存放在 backups/ 目錄中，並按照日期或版本組織
5. THE System SHALL 將所有臨時檔案存放在 temp/ 目錄中

### Requirement 7

**User Story:** 作為開發者，我希望有一份清晰的檔案組織規範文檔，以便未來開發時遵循統一標準

#### Acceptance Criteria

1. THE System SHALL 建立一份 FILE_ORGANIZATION_STANDARD.md 文檔，說明所有目錄的用途和檔案分類規則
2. THE System SHALL 在規範文檔中包含目錄結構樹狀圖
3. THE System SHALL 在規範文檔中說明每種檔案類型的命名規範
4. THE System SHALL 在規範文檔中提供檔案移動的對照表，記錄所有檔案的原始位置和新位置
5. THE System SHALL 在規範文檔中說明哪些檔案應該保留在根目錄

### Requirement 8

**User Story:** 作為開發者，我希望過時或重複的檔案被識別並歸檔，以保持專案整潔

#### Acceptance Criteria

1. WHEN 發現多個功能相似的文檔時，THE System SHALL 識別最新或最完整的版本，並將其他版本移至 archive/ 目錄
2. THE System SHALL 將所有帶有日期後綴的備份檔案（如 _*backup*_.db）移至 backups/ 目錄
3. THE System SHALL 識別所有狀態記錄文檔（emoji 開頭的 .md 檔案），並評估是否需要歸檔
4. THE System SHALL 建立 archive/README.md 說明歸檔檔案的原因和日期
5. THE System SHALL 確保歸檔的檔案不影響系統正常運作

### Requirement 9

**User Story:** 作為開發者，我希望專案結構支援多個子系統的獨立開發，同時保持整體一致性

#### Acceptance Criteria

1. THE System SHALL 為每個主要子系統（碳排放追蹤、語音處理、ASR、人才評鑑）建立獨立的功能目錄
2. WHEN 子系統有專屬的文檔、測試或配置時，THE System SHALL 將這些檔案組織在該子系統目錄下
3. THE System SHALL 確保共用的程式碼（如 database.py、utils.py）存放在根目錄或 common/ 目錄中
4. THE System SHALL 在每個子系統目錄中包含 README.md 說明該子系統的功能和使用方式
5. THE System SHALL 確保子系統之間的依賴關係清晰可追溯

### Requirement 10

**User Story:** 作為專案維護者，我希望檔案重組過程不會破壞現有功能，並且可以追溯變更

#### Acceptance Criteria

1. WHEN 移動檔案時，THE System SHALL 更新所有相關的 import 語句和路徑引用
2. THE System SHALL 在移動檔案前建立完整的專案備份
3. THE System SHALL 建立檔案移動日誌（FILE_MIGRATION_LOG.md），記錄每個檔案的原始路徑和新路徑
4. THE System SHALL 在移動完成後執行基本測試，確保核心功能正常運作
5. THE System SHALL 提供回滾腳本，以便在出現問題時恢復原始結構
