# Implementation Plan

- [x] 1. 準備階段：建立備份和基礎結構

  - 建立完整專案備份到 backups/pre-reorganization-[timestamp]/
  - 記錄當前 git commit hash 和專案狀態
  - 建立新目錄結構（config/, docs/, scripts/, tests/, assets/, data/, modules/, archive/）
  - 初始化 migration_log.json 記錄檔案移動
  - _Requirements: 10.2, 10.3_

- [x] 2. 生成檔案分類清單和分析報告

  - 掃描根目錄所有檔案，建立完整清單
  - 分析每個檔案的類型、用途和依賴關係
  - 生成檔案分類對照表（原路徑 → 新路徑）
  - 識別需要更新 import 語句的 Python 檔案
  - 識別需要歸檔的過時檔案
  - _Requirements: 1.4, 8.1, 10.1_

- [-] 3. 移動配置檔案

- [x] 3.1 建立 config/ 子目錄結構

  - 建立 config/requirements/, config/deployment/, config/api_specs/
  - 在每個子目錄建立 README.md 說明用途
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 3.2 移動依賴配置檔案

  - 移動 requirements.txt → config/requirements/base.txt
  - 移動 requirements-voice.txt → config/requirements/voice.txt
  - 移動 requirements-asr.txt → config/requirements/asr.txt
  - 移動 requirements_carbon_only.txt → config/requirements/carbon.txt
  - 移動 requirements_full.txt → config/requirements/full.txt
  - 移動 requirements_minimal.txt → config/requirements/minimal.txt
  - 更新 app.py 和相關文檔中的引用路徑
  - _Requirements: 5.1_

- [x] 3.3 移動部署配置檔案

  - 移動 render.yaml → config/deployment/
  - 移動 Dockerfile.voice-api → config/deployment/
  - 移動 nginx-voice.conf → config/deployment/
  - 更新部署文檔中的路徑引用
  - _Requirements: 5.2_

- [x] 3.4 移動 API 規格檔案

  - 移動 gpt-sovits-api.json → config/api_specs/
  - 移動 f5-tts API.json → config/api_specs/f5-tts-api.json
  - 移動 Gpt-Sovis-API.md → config/api_specs/
  - 移動 api_description.txt → config/api_specs/
  - _Requirements: 5.3_

- [x] 3.5 測試配置檔案移動

  - 驗證 requirements 檔案可正常安裝
  - 驗證部署配置檔案路徑正確
  - _Requirements: 10.4_

- [-] 4. 移動文檔檔案

- [x] 4.1 建立 docs/ 子目錄結構

  - 建立 docs/guides/, docs/technical/, docs/reports/, docs/status/
  - 建立 docs/technical/ 下的子目錄（architecture/, backend/, frontend/, voice/, asr/）
  - 建立 docs/status/ 下的子目錄（completed/, deployment/）
  - 在每個子目錄建立 README.md
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 4.2 移動操作指南文檔

  - 移動 開始使用\_README.md → docs/guides/quick_start.md
  - 移動 碳排放追蹤系統\_使用說明.md → docs/guides/carbon_tracking_usage.md
  - 移動 VOICE_CLONE_GUIDE.md → docs/guides/voice_clone_guide.md
  - 移動 build_android_app.md → docs/guides/android_app_build.md
  - 移動 deploy_to_render.md → docs/guides/deployment_guide.md
  - 移動 快速參考卡.md → docs/guides/
  - 移動 PWA 檢查清單.md → docs/guides/
  - 移動 部署檢查清單.md → docs/guides/
  - 移動 最終檢查清單.md → docs/guides/
  - 移動 🚀 快速啟動指南.md → docs/guides/
  - 移動 🚀APK 建置與上架完整指南.md → docs/guides/
  - _Requirements: 2.3_

- [x] 4.3 移動技術文檔

  - 移動 project-structure.md → docs/technical/architecture/
  - 移動 SYSTEM_ARCHITECTURE_DIAGRAM.svg → docs/technical/architecture/
  - 移動 BACKEND_TECHNICAL_DOCUMENTATION.md → docs/technical/backend/
  - 移動 FRONTEND_TECHNICAL_DOCUMENTATION.md → docs/technical/frontend/
  - 移動 ADVANCED_VOICE_SEPARATION_GUIDE.md → docs/technical/voice/
  - 移動 AUDIO_SEPARATION_GUIDE.md → docs/technical/voice/
  - 移動 VOICE_DATASET_VALIDATION_GUIDE.md → docs/technical/voice/
  - 移動 GPT_SOVITS_FINE_TUNING_GUIDE.md → docs/technical/voice/
  - 移動 VOICE_CLONE_SETUP.md → docs/technical/voice/
  - 移動 MODEL_STORAGE_DEPLOYMENT_GUIDE.md → docs/technical/voice/
  - 移動 MODEL_WEIGHTS_CONFIGURATION_GUIDE.md → docs/technical/voice/
  - 移動 VOLUME_BALANCE_SOLUTION.md → docs/technical/voice/
  - 移動 NATURAL_VS_ADVANCED_COMPARISON.md → docs/technical/voice/
  - 移動 setup_asr_environment.md → docs/technical/asr/
  - 移動 docs/funasr\_\*.md → docs/technical/asr/
  - _Requirements: 2.1_

- [x] 4.4 移動分析報告文檔

  - 移動 AI_CORE_MODULES_ARCHITECTURE_REPORT.md → docs/reports/
  - 移動 VOICE_DATA_PROCESSING_AND_AI_MODULES_REPORT.md → docs/reports/
  - 移動 NOISE_REDUCTION_IMPROVEMENT_REPORT.md → docs/reports/
  - 移動 MODULE_TESTING_REPORT.md → docs/reports/
  - 移動 ELDERLY_VOICE_DATASET_VALIDATION_REPORT.md → docs/reports/
  - 移動 CLEANUP_SUMMARY.md → docs/reports/
  - 移動 優化後模型成效比較報告.md → docs/reports/
  - 移動 專業系統驗證及 ASR 改進整合報告.md → docs/reports/
  - 移動 推廣成果摘要報告.md → docs/reports/
  - 移動 碳排放減少效益分析.md → docs/reports/
  - 移動 專案技術分析報告.md → docs/reports/
  - _Requirements: 2.2_

- [x] 4.5 移動狀態記錄文檔

  - 移動 ✅ 碳排放追蹤系統\_建置完成.md → docs/status/completed/
  - 移動 ✅ 工號自動帶出姓名功能完成.md → docs/status/completed/
  - 移動 ✅ 搜尋與篩選功能完成.md → docs/status/completed/
  - 移動 ✅ 記錄編輯刪除功能完成.md → docs/status/completed/
  - 移動 ✅ 資料匯出功能完成.md → docs/status/completed/
  - 移動 ✅ 優化完成\_立即測試.md → docs/status/completed/
  - 移動 ✅PWA_Android_App 完成.md → docs/status/completed/
  - 移動 ✅ 完成報告\_所有佐證資料已就緒.md → docs/status/completed/
  - 移動 🎉 部署成功\_開始建置 APK.md → docs/status/deployment/
  - 移動 🎉 部署完成\_下一步行動.md → docs/status/deployment/
  - 移動 🎉PWA 轉換完成\_快速開始.md → docs/status/completed/
  - 移動 🎊 完整方案\_PWA+Android 全部完成.md → docs/status/completed/
  - 移動 🎊PWA 完整方案\_全部完成.md → docs/status/completed/
  - 移動 🔧 修復完成\_等待部署.md → docs/status/deployment/
  - 移動 🌿 淡化綠色主題+分頁功能完成.md → docs/status/completed/
  - 移動 🌿 環保綠色主題優化完成.md → docs/status/completed/
  - 移動 📱 轉換為 Android_App 指南.md → docs/status/completed/
  - 移動 📱Android_App 建置完成.md → docs/status/completed/
  - 移動 UI 優化完成說明.md → docs/status/completed/
  - 移動 完成清單\_稽核佐證資料.md → docs/status/completed/
  - _Requirements: 2.4_

- [x] 4.6 移動其他文檔

  - 移動 系統改進建議.md → docs/
  - 移動 部署架構優化方案.md → docs/technical/architecture/
  - 移動 部署模式說明.md → docs/technical/architecture/
  - 移動 Render 部署問題排查.md → docs/status/deployment/
  - 移動 Android_App 功能相容性分析.md → docs/technical/
  - 移動 PYTHON_313_COMPATIBILITY_FIX.md → docs/technical/
  - 移動 emotion_color_guide.md → docs/technical/voice/
  - _Requirements: 2.1, 2.2_

- [x] 4.7 更新文檔內部連結

  - 掃描所有 .md 檔案中的相對連結
  - 更新指向已移動檔案的連結
  - 驗證所有連結有效
  - _Requirements: 10.1_

- [x] 5. 移動腳本檔案

- [x] 5.1 建立 scripts/ 子目錄結構

  - 建立 scripts/data_generation/, scripts/data_processing/, scripts/validation/
  - 建立 scripts/downloads/, scripts/monitoring/, scripts/startup/
  - 在每個子目錄建立 README.md
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 5.2 移動資料生成腳本

  - 移動 generate_mock_carbon_data.py → scripts/data_generation/
  - 移動 generate_carbon_emission_tables.py → scripts/data_generation/
  - 移動 generate_carbon_dashboard_images.py → scripts/data_generation/
  - 移動 generate_epa_document_images.py → scripts/data_generation/
  - 移動 generate_pwa_icons.py → scripts/data_generation/
  - _Requirements: 4.1_

- [x] 5.3 移動資料處理腳本

  - 移動 update_social_worker_names.py → scripts/data_processing/
  - 移動 update_names_extended.py → scripts/data_processing/
  - 移動 add_more_social_workers.py → scripts/data_processing/
  - 移動 process_03041966_audio.py → scripts/data_processing/
  - 移動 process_advanced_03041966.py → scripts/data_processing/
  - 移動 process_natural_03041966.py → scripts/data_processing/
  - 移動 advanced_voice_separation.py → scripts/data_processing/
  - 移動 audio_voice_separation.py → scripts/data_processing/
  - 移動 natural_voice_separation.py → scripts/data_processing/
  - 移動 optimized_natural_voice_separation.py → scripts/data_processing/
  - 移動 volume_balanced_voice_separation.py → scripts/data_processing/
  - _Requirements: 4.3_

- [x] 5.4 移動驗證腳本

  - 移動 check_audio_files.py → scripts/validation/
  - 移動 check_emotion_methods.py → scripts/validation/
  - 移動 check_social_worker_names.py → scripts/validation/
  - 移動 final_tag_validation.py → scripts/validation/
  - 移動 batch_validation_processor.py → scripts/validation/
  - 移動 voice_dataset_validation_system.py → scripts/validation/
  - 移動 dataset_validation_dashboard.py → scripts/validation/
  - _Requirements: 4.2_

- [x] 5.5 移動下載和監控腳本

  - 移動 download_epa_document.py → scripts/downloads/
  - 移動 download_funasr_model.py → scripts/downloads/
  - 移動 monitor_deployment.py → scripts/monitoring/
  - 移動 show_all_workers_stats.py → scripts/monitoring/
  - 移動 debug_voice_models.py → scripts/monitoring/
  - _Requirements: 4.4_

- [x] 5.6 移動啟動腳本

  - 移動 start_carbon_tracking.bat → scripts/startup/
  - 移動 start-gpt-sovits.bat → scripts/startup/
  - 移動 start-voice-api.bat → scripts/startup/
  - 移動 start-voice-clone-service.bat → scripts/startup/
  - 移動 setup-voice-system.bat → scripts/startup/
  - 移動 install-gpt-sovits.bat → scripts/startup/
  - 移動 test_pwa_features.bat → scripts/startup/
  - 更新批次檔中的路徑引用
  - _Requirements: 4.5_

- [x] 5.7 測試腳本執行

  - 測試資料生成腳本可正常執行
  - 測試驗證腳本可正常執行
  - 測試啟動腳本可正常啟動應用
  - _Requirements: 10.4_

- [ ] 6. 移動測試檔案

- [x] 6.1 建立 tests/ 子目錄結構

  - 建立 tests/unit/, tests/integration/, tests/performance/, tests/deployment/
  - 在每個子目錄建立 README.md 和 **init**.py
  - _Requirements: 3.2_

- [x] 6.2 移動單元測試

  - 移動 test_elderly_detector.py → tests/unit/
  - 移動 test_minnan_detector.py → tests/unit/
  - _Requirements: 3.1, 3.4_

- [x] 6.3 移動整合測試

  - 移動 test_asr_coordinator.py → tests/integration/
  - 移動 test_funasr_engine.py → tests/integration/
  - 移動 test_asr_api.py → tests/integration/
  - 移動 test_carbon_system.py → tests/integration/
  - 移動 test_minimal_app.py → tests/integration/
  - _Requirements: 3.1, 3.4_

- [x] 6.4 移動效能測試

  - 移動 test_asr_performance.py → tests/performance/
  - 移動 test_asr_setup.py → tests/performance/
  - _Requirements: 3.1, 3.4_

- [x] 6.5 移動部署測試

  - 移動 test_deployment.py → tests/deployment/
  - 移動 test_pwa.html → tests/deployment/
  - _Requirements: 3.1, 3.4_

- [x] 6.6 更新測試檔案的 import 語句

  - 掃描所有測試檔案的 import 語句
  - 更新指向已移動模組的路徑
  - 執行測試確認無錯誤
  - _Requirements: 10.1, 10.4_

-

- [x] 7. 移動資源和資料檔案

- [x] 7.1 建立 assets/ 和 data/ 目錄結構

  - 建立 assets/audio/, assets/images/
  - 建立 data/databases/, data/logs/
  - 在每個目錄建立 README.md
  - _Requirements: 6.1, 6.3_

- [x] 7.2 移動音訊資源

  - 移動 mockvoice/ → assets/audio/mockvoice/
  - 移動 genvoice/ → assets/audio/genvoice/
  - 移動 audio_uploads/ → assets/audio/uploads/
  - 移動 TTS/ → assets/audio/tts/
  - 移動 voice_output/ → assets/audio/voice_output/
  - 更新程式碼中的音訊路徑引用
  - _Requirements: 6.1_

- [x] 7.3 移動圖片資源

  - 複製 static/icons/ → assets/images/icons/
  - 保留 static/icons/ 的符號連結或更新引用
  - _Requirements: 6.2_

- [x] 7.4 移動資料庫檔案

  - 移動 carbon_tracking.db → data/databases/
  - 移動 customer_service.db → data/databases/
  - 移動 carbon*tracking_backup*\*.db → backups/databases/
  - 更新 database.py 和 database_carbon_tracking.py 中的路徑
  - _Requirements: 6.3, 6.4_

- [x] 7.5 移動日誌檔案

  - 移動 voice_dataset_validation.log → data/logs/
  - 更新日誌配置中的路徑
  - _Requirements: 6.3_

- [x] 7.6 測試資源和資料存取

  - 驗證音訊檔案可正常載入
  - 驗證資料庫連接正常
  - 驗證靜態資源載入正常
  - _Requirements: 10.4_

- [x] 8. 組織功能模組

- [x] 8.1 建立 modules/ 目錄結構

  - 建立 modules/carbon_tracking/, modules/voice_processing/
  - 建立 modules/asr/, modules/talent_assessment/
  - 在每個子目錄建立 README.md
  - _Requirements: 9.1, 9.4_

- [x] 8.2 組織碳排放追蹤模組

  - 移動 database_carbon_tracking.py → modules/carbon_tracking/
  - 在 modules/carbon_tracking/README.md 中說明模組功能
  - 在 README 中參考 routes/carbon_tracking.py 和 templates/carbon_tracking/
  - 更新相關 import 語句
  - _Requirements: 9.1, 9.2, 9.4_

- [x] 8.3 組織語音處理模組

  - 移動 voice_clone_service.py → modules/voice_processing/
  - 移動 voice_synthesis_service.py → modules/voice_processing/
  - 移動 simple_voice_api.py → modules/voice_processing/
  - 移動 voice_config.py → modules/voice_processing/
  - 移動 database_emotion_extension.py → modules/voice_processing/
  - 在 modules/voice_processing/README.md 中說明模組功能
  - 更新相關 import 語句
  - _Requirements: 9.1, 9.2, 9.4_

- [x] 8.4 組織人才評鑑模組

  - 移動 talent_assessment_db_connector.py → modules/talent_assessment/
  - 移動 talent_assessment_llm_query_generator.py → modules/talent_assessment/
  - 移動 talent_assessment_query_validator.py → modules/talent_assessment/
  - 在 modules/talent_assessment/README.md 中說明模組功能
  - 更新相關 import 語句
  - _Requirements: 9.1, 9.2, 9.4_

- [x] 8.5 建立 ASR 模組參考

  - 在 modules/asr/README.md 中說明 ASR 功能
  - 參考 services/asr/ 目錄和相關文檔
  - 說明 ASR 模組的使用方式
  - _Requirements: 9.1, 9.4_

- [x] 8.6 測試模組功能

  - 測試碳排放追蹤功能正常
  - 測試語音處理功能正常
  - 測試人才評鑑功能正常
  - 測試 ASR 功能正常
  - _Requirements: 10.4_

-

- [x] 9. 歸檔過時檔案

- [x] 9.1 建立 archive/ 目錄結構

  - 建立 archive/2025-11/
  - 建立 archive/2025-11/old_requirements/
  - 建立 archive/2025-11/old_docs/
  - 建立 archive/2025-11/old_scripts/
  - 建立 archive/README.md 說明歸檔政策
  - _Requirements: 8.4_

- [x] 9.2 識別並歸檔過時檔案

  - 移動 requirements_250521.txt → archive/2025-11/old_requirements/
  - 移動 requirements_backup.txt → archive/2025-11/old_requirements/
  - 移動 requirements_audio_separation.txt → archive/2025-11/old_requirements/
  - 移動 validate_vue_component.js → archive/2025-11/old_scripts/
  - 評估 Gpt-Sovis-API.docx 是否需要歸檔（已有 .md 版本）
  - 評估 給 VB3-_.docx, 給 VC2-_.docx 是否需要歸檔（已有對應 .md 報告）
  - _Requirements: 8.1, 8.2_

- [x] 9.3 建立歸檔說明文檔

  - 在 archive/2025-11/README.md 中記錄每個檔案的歸檔原因
  - 記錄歸檔日期和決策依據
  - 說明如何恢復歸檔檔案
  - _Requirements: 8.4_

- [ ] 10. 建立規範文檔和遷移記錄

- [x] 10.1 建立檔案組織規範文檔

  - 建立 FILE_ORGANIZATION_STANDARD.md
  - 說明所有目錄的用途和檔案分類規則
  - 包含完整的目錄結構樹狀圖
  - 說明每種檔案類型的命名規範
  - 說明哪些檔案應該保留在根目錄
  - 提供新檔案的存放決策流程圖
  - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [x] 10.2 建立檔案遷移日誌

  - 建立 FILE_MIGRATION_LOG.md
  - 記錄所有檔案的原始位置和新位置
  - 記錄遷移日期和執行者
  - 記錄每個檔案的遷移原因
  - 包含統計資訊（移動檔案數、歸檔檔案數等）
  - _Requirements: 7.4, 10.3_

- [x] 10.3 更新主 README.md

  - 建立或更新專案根目錄的 README.md
  - 說明專案結構和主要目錄
  - 提供快速開始指南的連結
  - 說明如何找到各類文檔和腳本
  - 包含專案架構圖
  - _Requirements: 7.1, 7.2_

- [x] 10.4 建立回滾腳本

  - 建立 scripts/rollback.py
  - 實作根據 migration_log.json 還原檔案的功能
  - 提供命令列介面選擇還原範圍
  - 測試回滾功能
  - _Requirements: 10.5_

-

- [x] 11. 執行完整測試和驗證

- [x] 11.1 執行自動化測試

  - 執行所有單元測試
  - 執行所有整合測試
  - 記錄測試結果
  - 修復任何失敗的測試
  - _Requirements: 10.4_

- [x] 11.2 手動測試核心功能

  - 測試 app.py 正常啟動
  - 測試碳排放追蹤系統所有頁面
  - 測試語音處理功能（如果可用）
  - 測試 ASR 功能（如果可用）
  - 記錄測試結果
  - _Requirements: 10.4_

- [x] 11.3 驗證文檔和連結

  - 檢查所有文檔的內部連結
  - 驗證文檔中的程式碼範例
  - 確認所有 README 檔案完整
  - 修復任何失效的連結
  - _Requirements: 10.1_

- [x] 11.4 驗證配置和路徑

  - 檢查所有配置檔案的路徑引用
  - 驗證靜態資源路徑正確
  - 驗證資料庫路徑正確
  - 驗證日誌路徑正確
  - _Requirements: 10.1, 10.4_

- [x] 11.5 建立驗證報告

  - 記錄所有測試結果
  - 列出已修復的問題
  - 列出已知的限制或注意事項
  - 確認所有成功標準達成
  - _Requirements: 10.4_

- [-] 12. 最終清理和文檔化

- [x] 12.1 清理根目錄

  - 確認根目錄只保留必要檔案
  - 移除任何遺漏的臨時檔案
  - 驗證根目錄檔案數量減少 80% 以上
  - _Requirements: 1.4_

- [x] 12.2 更新 .gitignore

  - 更新 .gitignore 以反映新的目錄結構
  - 確保臨時檔案和備份不被追蹤
  - _Requirements: 5.4_

- [x] 12.3 建立專案狀態快照

  - 記錄重組後的專案統計資訊
  - 建立新的目錄結構圖
  - 記錄所有主要變更
  - _Requirements: 10.3_

- [x] 12.4 準備團隊溝通文檔

  - 建立重組變更摘要
  - 說明如何適應新結構
  - 提供常見問題解答
  - 說明如何找到常用檔案
  - _Requirements: 7.1, 7.2_

- [-] 12.5 建立 Git commit

  - 提交所有變更到版本控制
  - 撰寫詳細的 commit message
  - 標記為重要的結構變更
  - _Requirements: 10.3_
