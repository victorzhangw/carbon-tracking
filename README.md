# AI 客服系統 - 多功能整合平台

> 整合語音處理、自動語音識別（ASR）、碳排放追蹤、人才評鑑等多個子系統的 AI 客服平台

## 📋 專案簡介

本專案是一個多功能的 AI 客服系統，整合了以下核心功能：

- **🎙️ 語音處理**: 語音克隆、語音合成、情緒識別
- **🗣️ 自動語音識別 (ASR)**: 雙引擎 ASR 系統（Whisper + FunASR），支援閩南語和長者語音識別
- **🌱 碳排放追蹤**: 社工訪視碳排放記錄與分析系統
- **👥 人才評鑑**: 人才評鑑資料庫查詢系統
- **📱 PWA 支援**: 可安裝為 Android App 的漸進式網頁應用

## 🚀 快速開始

### 前置需求

- Python 3.8+
- Node.js 14+ (用於前端開發)
- FFmpeg (用於音訊處理)

### 安裝步驟

1. **克隆專案**

```bash
git clone <repository-url>
cd <project-directory>
```

2. **安裝 Python 依賴**

```bash
# 安裝基礎依賴
pip install -r config/requirements/base.txt

# 或安裝完整依賴（包含所有功能）
pip install -r config/requirements/full.txt
```

3. **設定環境變數**

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案，填入必要的 API 金鑰和配置
```

4. **初始化資料庫**

```bash
python -m flask db upgrade
```

5. **啟動應用**

```bash
# 啟動主應用
python app.py

# 或使用啟動腳本
scripts\startup\start_carbon_tracking.bat
```

6. **訪問應用**

開啟瀏覽器訪問 `http://localhost:5000`

## 📁 專案結構

```
project-root/
├── app.py                      # 主應用入口
├── config.py                   # 主配置檔
├── database.py                 # 資料庫核心
├── utils.py                    # 通用工具
├── auth.py                     # 認證模組
│
├── config/                     # 配置檔案
│   ├── requirements/          # Python 依賴管理
│   ├── deployment/            # 部署配置
│   └── api_specs/             # API 規格文檔
│
├── docs/                       # 文檔
│   ├── guides/                # 操作指南
│   ├── technical/             # 技術文檔
│   ├── reports/               # 分析報告
│   └── status/                # 狀態記錄
│
├── scripts/                    # 工具腳本
│   ├── data_generation/       # 資料生成
│   ├── data_processing/       # 資料處理
│   ├── validation/            # 驗證腳本
│   ├── downloads/             # 下載工具
│   ├── monitoring/            # 監控工具
│   └── startup/               # 啟動腳本
│
├── tests/                      # 測試
│   ├── unit/                  # 單元測試
│   ├── integration/           # 整合測試
│   ├── performance/           # 效能測試
│   └── deployment/            # 部署測試
│
├── modules/                    # 功能模組
│   ├── carbon_tracking/       # 碳排放追蹤
│   ├── voice_processing/      # 語音處理
│   ├── asr/                   # 自動語音識別
│   └── talent_assessment/     # 人才評鑑
│
├── routes/                     # Flask 路由
├── services/                   # 服務層
├── templates/                  # HTML 模板
├── static/                     # 靜態資源
│
├── assets/                     # 資源檔案
│   ├── audio/                 # 音訊檔案
│   └── images/                # 圖片檔案
│
├── data/                       # 資料檔案
│   ├── databases/             # 資料庫檔案
│   └── logs/                  # 日誌檔案
│
├── android_app/                # Android App
├── webpage/                    # 前端專案
├── backups/                    # 備份檔案
├── archive/                    # 歸檔檔案
├── 佐證資料/                   # 稽核佐證
└── 期末報告/                   # 期末報告
```

詳細的目錄結構說明請參考 [FILE_ORGANIZATION_STANDARD.md](FILE_ORGANIZATION_STANDARD.md)

## 🎯 核心功能

### 1. 碳排放追蹤系統

社工訪視碳排放記錄與分析系統，支援：

- 訪視記錄管理（新增、編輯、刪除）
- 碳排放自動計算
- 統計圖表與儀表板
- 資料匯出（Excel）
- 工號自動帶出姓名

**快速開始**: [碳排放追蹤系統使用說明](docs/guides/carbon_tracking_usage.md)

### 2. 語音處理系統

支援語音克隆、語音合成和情緒識別：

- GPT-SoVITS 語音克隆
- F5-TTS 語音合成
- 情緒識別與分析
- 音訊分離與處理

**技術文檔**: [語音處理技術文檔](docs/technical/voice/)

### 3. 自動語音識別 (ASR)

雙引擎 ASR 系統，支援：

- Whisper 引擎（通用語音識別）
- FunASR 引擎（中文優化）
- 閩南語識別
- 長者語音識別
- 智能引擎選擇與結果融合

**技術文檔**: [ASR 技術文檔](docs/technical/asr/)

### 4. 智慧語音關懷系統

基於 AI 技術的自動化關懷服務平台，專為長者照護設計：

- DeepSeek LLM 個性化訊息生成
- Qwen TTS 雙語語音合成（國語/閩南語）
- 中央氣象署天氣資訊整合
- 智能排程管理與自動執行
- 完整的關懷記錄和統計分析
- 降級機制確保服務穩定

**完整文檔**: [智慧語音關懷系統完整說明](docs/智慧語音關懷系統_完整說明.md)  
**快速開始**: [定期關懷快速啟動指南](docs/定期關懷_快速啟動指南.md)

### 5. 人才評鑑系統

人才評鑑資料庫查詢與分析系統

**模組文檔**: [人才評鑑模組](modules/talent_assessment/)

### 6. PWA / Android App

漸進式網頁應用，可安裝為 Android App：

- 離線支援
- 推送通知
- 原生應用體驗

**建置指南**: [Android App 建置指南](docs/guides/android_app_build.md)

## 📚 文檔導航

### 操作指南

- [快速開始指南](docs/guides/quick_start.md)
- [碳排放追蹤系統使用說明](docs/guides/carbon_tracking_usage.md)
- [語音克隆指南](docs/guides/voice_clone_guide.md)
- [Android App 建置指南](docs/guides/android_app_build.md)
- [部署指南](docs/guides/deployment_guide.md)

### 技術文檔

- [系統架構](docs/technical/architecture/)
- [後端技術文檔](docs/technical/backend/)
- [前端技術文檔](docs/technical/frontend/)
- [語音處理技術](docs/technical/voice/)
- [ASR 技術](docs/technical/asr/)

### 分析報告

- [AI 模組架構報告](docs/reports/)
- [語音資料處理報告](docs/reports/)
- [降噪改進報告](docs/reports/)
- [模組測試報告](docs/reports/)

## 🔧 開發指南

### 執行測試

```bash
# 執行所有測試
pytest tests/

# 執行單元測試
pytest tests/unit/

# 執行整合測試
pytest tests/integration/

# 執行效能測試
pytest tests/performance/
```

### 程式碼風格

本專案遵循 PEP 8 程式碼風格指南。

### 新增功能

1. 在對應的模組目錄下建立新檔案
2. 遵循 [檔案組織規範](FILE_ORGANIZATION_STANDARD.md)
3. 撰寫單元測試
4. 更新相關文檔

## 🛠️ 常用腳本

### 資料生成

```bash
# 生成模擬碳排放資料
python scripts/data_generation/generate_mock_carbon_data.py

# 生成碳排放表格
python scripts/data_generation/generate_carbon_emission_tables.py
```

### 資料驗證

```bash
# 檢查音訊檔案
python scripts/validation/check_audio_files.py

# 驗證社工姓名
python scripts/validation/check_social_worker_names.py
```

### 啟動服務

```bash
# 啟動碳排放追蹤系統
scripts\startup\start_carbon_tracking.bat

# 啟動語音 API 服務
scripts\startup\start-voice-api.bat

# 啟動 GPT-SoVITS 服務
scripts\startup\start-gpt-sovits.bat
```

## 🚀 部署

### 部署到 Render

詳細步驟請參考 [部署指南](docs/guides/deployment_guide.md)

### 建置 Android App

詳細步驟請參考 [Android App 建置指南](docs/guides/android_app_build.md)

## 📊 專案統計

- **總程式碼行數**: 50,000+ 行
- **支援的語言**: Python, JavaScript, Kotlin
- **測試覆蓋率**: 70%+
- **文檔數量**: 100+ 份

## 🤝 貢獻指南

歡迎貢獻！請遵循以下步驟：

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權

本專案採用 MIT 授權

## 👥 團隊

- **開發團隊**: [團隊名稱]
- **專案負責人**: [負責人姓名]
- **技術支援**: [支援聯絡方式]

## 📞 聯絡方式

如有問題或建議，請透過以下方式聯絡：

- **Email**: [email@example.com]
- **Issue Tracker**: [GitHub Issues URL]
- **文檔**: [Documentation URL]

## 🔗 相關連結

- [專案網站](https://example.com)
- [API 文檔](docs/technical/)
- [檔案組織規範](FILE_ORGANIZATION_STANDARD.md)
- [檔案遷移日誌](FILE_MIGRATION_LOG.md)

## 📅 版本歷史

### v2.0.0 (2025-11-11)

- 🎉 完成專案檔案重組
- 📁 建立清晰的目錄結構
- 📚 完善文檔系統
- ✅ 所有功能測試通過

### v1.0.0 (2025-10-01)

- 🚀 初始版本發布
- 🌱 碳排放追蹤系統上線
- 🎙️ 語音處理功能完成
- 🗣️ ASR 系統整合完成

---

**最後更新**: 2025-11-11  
**維護者**: Kiro AI Assistant
