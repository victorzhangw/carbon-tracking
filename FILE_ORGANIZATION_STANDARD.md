# 專案檔案組織規範

> 本文檔定義了專案的檔案組織標準，所有開發者在新增或移動檔案時都應遵循此規範。

## 📋 目錄結構總覽

```
project-root/
├── app.py                          # 主應用入口
├── config.py                       # 主配置檔
├── database.py                     # 資料庫核心
├── utils.py                        # 通用工具
├── auth.py                         # 認證模組
├── README.md                       # 專案說明
├── .gitignore                      # Git 配置
│
├── config/                         # 📦 配置檔案
│   ├── requirements/              # 依賴管理
│   ├── deployment/                # 部署配置
│   └── api_specs/                 # API 規格
│
├── docs/                          # 📚 文檔
│   ├── guides/                    # 操作指南
│   ├── technical/                 # 技術文檔
│   ├── reports/                   # 分析報告
│   └── status/                    # 狀態記錄
│
├── scripts/                       # 🔧 工具腳本
│   ├── data_generation/          # 資料生成
│   ├── data_processing/          # 資料處理
│   ├── validation/               # 驗證腳本
│   ├── downloads/                # 下載工具
│   ├── monitoring/               # 監控工具
│   └── startup/                  # 啟動腳本
│
├── tests/                         # 🧪 測試
│   ├── unit/                     # 單元測試
│   ├── integration/              # 整合測試
│   ├── performance/              # 效能測試
│   └── deployment/               # 部署測試
│
├── assets/                        # 🎨 靜態資源
│   ├── audio/                    # 音訊檔案
│   └── images/                   # 圖片檔案
│
├── data/                          # 💾 資料檔案
│   ├── databases/                # 資料庫檔案
│   └── logs/                     # 日誌檔案
│
├── modules/                       # 🧩 功能模組
│   ├── carbon_tracking/          # 碳排放追蹤
│   ├── voice_processing/         # 語音處理
│   ├── asr/                      # 自動語音識別
│   └── talent_assessment/        # 人才評鑑
│
├── routes/                        # 🛣️ Flask 路由
├── services/                      # ⚙️ 服務層
├── templates/                     # 🎨 HTML 模板
├── static/                        # 📁 靜態資源（Web）
│
├── android_app/                   # 📱 Android App
├── webpage/                       # 🌐 前端專案
│
├── backups/                       # 💾 備份檔案
├── temp/                          # 🗑️ 臨時檔案
├── archive/                       # 📦 歸檔檔案
│
├── 佐證資料/                      # 📊 稽核佐證
└── 期末報告/                      # 📄 期末報告
```

## 📝 檔案分類規則

### 1. 配置檔案 (config/)

**用途**: 集中管理所有配置檔案

| 檔案類型    | 存放位置               | 範例                                         |
| ----------- | ---------------------- | -------------------------------------------- |
| Python 依賴 | `config/requirements/` | `base.txt`, `voice.txt`, `asr.txt`           |
| 部署配置    | `config/deployment/`   | `render.yaml`, `Dockerfile.*`, `nginx*.conf` |
| API 規格    | `config/api_specs/`    | `*-api.json`, `api_description.txt`          |

**命名規範**:

- 依賴檔案: `{功能名稱}.txt` (如 `voice.txt`, `carbon.txt`)
- 部署檔案: 保持原有命名
- API 規格: `{服務名稱}-api.{json|yaml}`

### 2. 文檔 (docs/)

**用途**: 組織所有文檔，按類型分類

| 文檔類型 | 存放位置                               | 範例                                          |
| -------- | -------------------------------------- | --------------------------------------------- |
| 操作指南 | `docs/guides/`                         | `quick_start.md`, `deployment_guide.md`       |
| 技術文檔 | `docs/technical/{子類別}/`             | `architecture/`, `backend/`, `voice/`, `asr/` |
| 分析報告 | `docs/reports/`                        | `*_REPORT.md`, `*分析報告.md`                 |
| 狀態記錄 | `docs/status/{completed\|deployment}/` | `✅*.md`, `🎉*.md`                            |

**命名規範**:

- 英文文檔: 使用 snake_case (如 `quick_start.md`)
- 中文文檔: 使用描述性名稱 (如 `碳排放追蹤系統使用說明.md`)
- 狀態文檔: 可保留 emoji 前綴

**決策流程**:

```
新文檔 → 是操作指南? → Yes → docs/guides/
       ↓ No
       → 是技術文檔? → Yes → docs/technical/{子類別}/
       ↓ No
       → 是分析報告? → Yes → docs/reports/
       ↓ No
       → 是狀態記錄? → Yes → docs/status/
```

### 3. 腳本 (scripts/)

**用途**: 組織所有工具腳本，按用途分類

| 腳本類型 | 存放位置                   | 範例                                             |
| -------- | -------------------------- | ------------------------------------------------ |
| 資料生成 | `scripts/data_generation/` | `generate_*.py`                                  |
| 資料處理 | `scripts/data_processing/` | `update_*.py`, `process_*.py`, `*_separation.py` |
| 驗證腳本 | `scripts/validation/`      | `check_*.py`, `*_validation*.py`                 |
| 下載工具 | `scripts/downloads/`       | `download_*.py`                                  |
| 監控工具 | `scripts/monitoring/`      | `monitor_*.py`, `show_*.py`, `debug_*.py`        |
| 啟動腳本 | `scripts/startup/`         | `start_*.bat`, `setup_*.bat`                     |

**命名規範**:

- Python 腳本: `{動詞}_{名詞}.py` (如 `generate_mock_data.py`)
- 批次檔: `{動詞}-{名詞}.bat` (如 `start-voice-api.bat`)

### 4. 測試 (tests/)

**用途**: 集中管理所有測試腳本

| 測試類型 | 存放位置             | 範例                       |
| -------- | -------------------- | -------------------------- |
| 單元測試 | `tests/unit/`        | `test_elderly_detector.py` |
| 整合測試 | `tests/integration/` | `test_asr_coordinator.py`  |
| 效能測試 | `tests/performance/` | `test_asr_performance.py`  |
| 部署測試 | `tests/deployment/`  | `test_deployment.py`       |

**命名規範**:

- 所有測試檔案必須以 `test_` 開頭
- 格式: `test_{模組名稱}.py`

### 5. 資源 (assets/)

**用途**: 管理所有靜態資源檔案

| 資源類型 | 存放位置                 | 說明                                  |
| -------- | ------------------------ | ------------------------------------- |
| 音訊檔案 | `assets/audio/{子類別}/` | mockvoice/, genvoice/, uploads/, tts/ |
| 圖片檔案 | `assets/images/`         | 圖示、截圖等                          |

### 6. 資料 (data/)

**用途**: 管理資料庫和日誌檔案

| 資料類型 | 存放位置          | 範例            |
| -------- | ----------------- | --------------- |
| 資料庫   | `data/databases/` | `*.db` (非備份) |
| 日誌     | `data/logs/`      | `*.log`         |

**注意**: 備份資料庫檔案應存放在 `backups/databases/`

### 7. 功能模組 (modules/)

**用途**: 組織功能模組，支援子系統獨立開發

| 模組       | 存放位置                     | 說明             |
| ---------- | ---------------------------- | ---------------- |
| 碳排放追蹤 | `modules/carbon_tracking/`   | 碳排放相關功能   |
| 語音處理   | `modules/voice_processing/`  | 語音克隆、合成等 |
| ASR        | `modules/asr/`               | 自動語音識別     |
| 人才評鑑   | `modules/talent_assessment/` | 人才評鑑系統     |

**規範**:

- 每個模組目錄必須包含 `README.md`
- 模組內的檔案應該高度相關
- 跨模組的共用程式碼應放在根目錄或 `services/`

### 8. 歸檔 (archive/)

**用途**: 歸檔過時或重複的檔案

**結構**:

```
archive/
├── {年份}-{月份}/
│   ├── README.md              # 說明歸檔原因
│   ├── old_requirements/
│   ├── old_docs/
│   └── old_scripts/
```

**歸檔標準**:

- 有更新版本的舊檔案
- 不再使用的功能相關檔案
- 重複的文檔（保留最完整的版本）
- 帶有日期後綴的備份檔案

## 🚫 根目錄檔案限制

**允許保留在根目錄的檔案**:

- `app.py` - 主應用入口
- `config.py` - 主配置檔
- `database.py` - 資料庫核心
- `utils.py` - 通用工具
- `auth.py` - 認證模組
- `README.md` - 專案說明
- `.gitignore` - Git 配置
- `.env` - 環境變數（不提交到 Git）
- `requirements.txt` - 主依賴檔案（符號連結到 config/requirements/base.txt）

**不應該出現在根目錄的檔案**:

- 測試腳本 (`test_*.py`)
- 工具腳本 (`generate_*.py`, `check_*.py`, `update_*.py` 等)
- 文檔檔案 (`*.md` 除了 README.md)
- 配置檔案 (`*.yaml`, `*.json`, `Dockerfile.*` 等)
- 資料檔案 (`*.db`, `*.log`)
- 資源檔案 (`*.wav`, `*.mp3`, `*.png` 等)

## 🔄 新增檔案決策流程

```mermaid
graph TD
    A[新增檔案] --> B{檔案類型?}
    B -->|源碼| C{功能類型?}
    B -->|文檔| D{文檔類型?}
    B -->|腳本| E{腳本用途?}
    B -->|測試| F{測試類型?}
    B -->|資源| G{資源類型?}
    B -->|資料| H{資料類型?}

    C -->|路由| I[routes/]
    C -->|服務| J[services/]
    C -->|模組| K[modules/{模組名}/]

    D -->|指南| L[docs/guides/]
    D -->|技術| M[docs/technical/]
    D -->|報告| N[docs/reports/]
    D -->|狀態| O[docs/status/]

    E -->|生成| P[scripts/data_generation/]
    E -->|處理| Q[scripts/data_processing/]
    E -->|驗證| R[scripts/validation/]
    E -->|其他| S[scripts/{類別}/]

    F -->|單元| T[tests/unit/]
    F -->|整合| U[tests/integration/]
    F -->|效能| V[tests/performance/]

    G -->|音訊| W[assets/audio/]
    G -->|圖片| X[assets/images/]

    H -->|資料庫| Y[data/databases/]
    H -->|日誌| Z[data/logs/]
```

## 📌 最佳實踐

### 1. 檔案命名

- 使用描述性名稱，清楚表達檔案用途
- Python 檔案使用 snake_case
- 文檔檔案可使用中文或英文，保持一致性
- 避免使用特殊字符（emoji 除外，用於狀態文檔）

### 2. 目錄組織

- 每個目錄應包含 `README.md` 說明用途
- 相關檔案應放在同一目錄
- 避免目錄層級過深（最多 3-4 層）

### 3. 依賴管理

- 主依賴檔案: `config/requirements/base.txt`
- 功能特定依賴: `config/requirements/{功能}.txt`
- 完整依賴: `config/requirements/full.txt`

### 4. 文檔維護

- 更新檔案位置時，同步更新相關文檔的連結
- 定期檢查文檔的時效性
- 過時文檔應移至 `archive/`

### 5. 測試組織

- 測試檔案應與被測試的模組對應
- 測試檔案名稱: `test_{模組名稱}.py`
- 每個測試目錄應包含 `__init__.py`

## 🔍 常見問題

### Q: 如何決定檔案應該放在哪裡？

A: 參考上方的「新增檔案決策流程」圖，或查看「檔案分類規則」表格。

### Q: 如果檔案同時符合多個類別怎麼辦？

A: 選擇最主要的用途。例如，一個生成測試資料的腳本應該放在 `scripts/data_generation/` 而不是 `tests/`。

### Q: 可以在子目錄中再建立子目錄嗎？

A: 可以，但建議不超過 3-4 層。如果需要更深的層級，考慮重新設計目錄結構。

### Q: 如何處理臨時檔案？

A: 臨時檔案應放在 `temp/` 目錄，並確保 `.gitignore` 中已排除此目錄。

### Q: 備份檔案應該放在哪裡？

A: 所有備份檔案應放在 `backups/` 目錄，並按照日期或版本組織。

## 📅 維護記錄

| 日期       | 版本 | 變更說明                       |
| ---------- | ---- | ------------------------------ |
| 2025-11-11 | 1.0  | 初始版本，定義專案檔案組織規範 |

---

**注意**: 本規範是專案的重要文檔，所有開發者都應該遵循。如需修改規範，請先與團隊討論並更新此文檔。
