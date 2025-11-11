# File Classification and Migration Report

**Generated:** 2025-11-11T09:36:41.537824
**Total Files Analyzed:** 161

## Summary

- **Keep in Root:** 7 files
- **To Move:** 150 files
- **To Archive:** 4 files

### Files by Category

- **archive:** 1 files
- **config:** 15 files
- **data:** 8 files
- **docs:** 73 files
- **modules:** 10 files
- **scripts:** 35 files
- **tests:** 12 files
- **unknown:** 7 files

## File Classification Details

| Original Path | Category | Subcategory | New Path | Reason |
|--------------|----------|-------------|----------|--------|
| validate_vue_component.js | archive | old_scripts | archive/2025-11/old_scripts/validate_vue_component.js | 📦 Archive: Old or obsolete script |
| Dockerfile.voice-api | config | deployment | config/deployment/Dockerfile.voice-api | ➡️ Move: Docker deployment configuration |
| f5-tts API.json | config | api_specs | config/api_specs/f5-tts-api.json | ➡️ Move: API specification |
| file_classification_report.json | config | other |  | ➡️ Move:  |
| gpt-sovits-api.json | config | api_specs | config/api_specs/gpt-sovits-api.json | ➡️ Move: API specification |
| nginx-voice.conf | config | deployment | config/deployment/nginx-voice.conf | ➡️ Move: Deployment configuration |
| render.yaml | config | deployment | config/deployment/render.yaml | ➡️ Move: Deployment configuration |
| requirements-asr.txt | config | requirements | config/requirements/asr.txt | ➡️ Move: Dependency configuration |
| requirements-voice.txt | config | requirements | config/requirements/voice.txt | ➡️ Move: Dependency configuration |
| requirements.txt | config | requirements | config/requirements/base.txt | ➡️ Move: Dependency configuration |
| requirements_250521.txt | config | requirements | archive/2025-11/old_requirements/requirements_250521.txt | 📦 Archive: Old or backup requirements file |
| requirements_audio_separation.txt | config | requirements | archive/2025-11/old_requirements/requirements_audio_separation.txt | 📦 Archive: Old or backup requirements file |
| requirements_backup.txt | config | requirements | archive/2025-11/old_requirements/requirements_backup.txt | 📦 Archive: Old or backup requirements file |
| requirements_carbon_only.txt | config | requirements | config/requirements/carbon.txt | ➡️ Move: Dependency configuration |
| requirements_full.txt | config | requirements | config/requirements/full.txt | ➡️ Move: Dependency configuration |
| requirements_minimal.txt | config | requirements | config/requirements/minimal.txt | ➡️ Move: Dependency configuration |
| carbon_tracking.db | data | databases | data/databases/carbon_tracking.db | ➡️ Move: Database file |
| carbon_tracking_backup_20251110_072639.db | data | backups | backups/databases/carbon_tracking_backup_20251110_072639.db | ➡️ Move: Database backup file |
| carbon_tracking_backup_20251110_072934.db | data | backups | backups/databases/carbon_tracking_backup_20251110_072934.db | ➡️ Move: Database backup file |
| carbon_tracking_backup_20251110_073307.db | data | backups | backups/databases/carbon_tracking_backup_20251110_073307.db | ➡️ Move: Database backup file |
| customer_service.db | data | databases | data/databases/customer_service.db | ➡️ Move: Database file |
| voice_dataset_validation.log | data | logs | data/logs/voice_dataset_validation.log | ➡️ Move: Log file |
| 碳排放減少效益分析_佐證表格.xlsx | data | reports | data/reports/碳排放減少效益分析_佐證表格.xlsx | ➡️ Move: Data report file |
| 社工交通工具使用調查報告.xlsx | data | reports | data/reports/社工交通工具使用調查報告.xlsx | ➡️ Move: Data report file |
| .agent.md | docs | other | docs/.agent.md | ➡️ Move: General documentation |
| ADVANCED_VOICE_SEPARATION_GUIDE.md | docs | technical/voice | docs/technical/voice/ADVANCED_VOICE_SEPARATION_GUIDE.md | ➡️ Move: Voice processing technical guide |
| AI_CORE_MODULES_ARCHITECTURE_REPORT.md | docs | reports | docs/reports/AI_CORE_MODULES_ARCHITECTURE_REPORT.md | ➡️ Move: Analysis or technical report |
| AUDIO_SEPARATION_GUIDE.md | docs | technical/voice | docs/technical/voice/AUDIO_SEPARATION_GUIDE.md | ➡️ Move: Voice processing technical guide |
| Android_App功能相容性分析.md | docs | guides | docs/guides/Android_App功能相容性分析.md | ➡️ Move: Android/PWA guide |
| BACKEND_TECHNICAL_DOCUMENTATION.md | docs | technical/backend | docs/technical/backend/BACKEND_TECHNICAL_DOCUMENTATION.md | ➡️ Move: Backend technical documentation |
| CLEANUP_SUMMARY.md | docs | other | docs/CLEANUP_SUMMARY.md | ➡️ Move: General documentation |
| ELDERLY_VOICE_DATASET_VALIDATION_REPORT.md | docs | reports | docs/reports/ELDERLY_VOICE_DATASET_VALIDATION_REPORT.md | ➡️ Move: Analysis or technical report |
| FILE_CLASSIFICATION_REPORT.md | docs | reports | docs/reports/FILE_CLASSIFICATION_REPORT.md | ➡️ Move: Analysis or technical report |
| FILE_ORGANIZATION_STANDARD.md | docs | other | docs/FILE_ORGANIZATION_STANDARD.md | ➡️ Move: General documentation |
| FRONTEND_TECHNICAL_DOCUMENTATION.md | docs | technical/frontend | docs/technical/frontend/FRONTEND_TECHNICAL_DOCUMENTATION.md | ➡️ Move: Frontend technical documentation |
| GPT_SOVITS_FINE_TUNING_GUIDE.md | docs | technical/voice | docs/technical/voice/GPT_SOVITS_FINE_TUNING_GUIDE.md | ➡️ Move: Voice processing technical guide |
| Gpt-Sovis-API.docx | docs | other | docs/Gpt-Sovis-API.docx | ➡️ Move: General documentation |
| Gpt-Sovis-API.md | docs | other | docs/Gpt-Sovis-API.md | ➡️ Move: General documentation |
| MODEL_STORAGE_DEPLOYMENT_GUIDE.md | docs | technical/voice | docs/technical/voice/MODEL_STORAGE_DEPLOYMENT_GUIDE.md | ➡️ Move: Voice processing technical guide |
| MODEL_WEIGHTS_CONFIGURATION_GUIDE.md | docs | technical/voice | docs/technical/voice/MODEL_WEIGHTS_CONFIGURATION_GUIDE.md | ➡️ Move: Voice processing technical guide |
| MODULE_TESTING_REPORT.md | docs | reports | docs/reports/MODULE_TESTING_REPORT.md | ➡️ Move: Analysis or technical report |
| NATURAL_VS_ADVANCED_COMPARISON.md | docs | other | docs/NATURAL_VS_ADVANCED_COMPARISON.md | ➡️ Move: General documentation |
| NOISE_REDUCTION_IMPROVEMENT_REPORT.md | docs | reports | docs/reports/NOISE_REDUCTION_IMPROVEMENT_REPORT.md | ➡️ Move: Analysis or technical report |
| PWA檢查清單.md | docs | guides | docs/guides/PWA檢查清單.md | ➡️ Move: User guide or checklist |
| PYTHON_313_COMPATIBILITY_FIX.md | docs | other | docs/PYTHON_313_COMPATIBILITY_FIX.md | ➡️ Move: General documentation |
| Render部署問題排查.md | docs | guides | docs/guides/Render部署問題排查.md | ➡️ Move: Deployment guide |
| SYSTEM_ARCHITECTURE_DIAGRAM.svg | docs | technical/architecture | docs/technical/architecture/SYSTEM_ARCHITECTURE_DIAGRAM.svg | ➡️ Move: Architecture documentation |
| UI優化完成說明.md | docs | technical | docs/technical/UI優化完成說明.md | ➡️ Move: Technical analysis document |
| VOICE_CLONE_GUIDE.md | docs | technical/voice | docs/technical/voice/VOICE_CLONE_GUIDE.md | ➡️ Move: Voice processing technical guide |
| VOICE_CLONE_SETUP.md | docs | technical/voice | docs/technical/voice/VOICE_CLONE_SETUP.md | ➡️ Move: Voice processing technical guide |
| VOICE_DATASET_VALIDATION_GUIDE.md | docs | technical/voice | docs/technical/voice/VOICE_DATASET_VALIDATION_GUIDE.md | ➡️ Move: Voice processing technical guide |
| VOICE_DATA_PROCESSING_AND_AI_MODULES_REPORT.md | docs | reports | docs/reports/VOICE_DATA_PROCESSING_AND_AI_MODULES_REPORT.md | ➡️ Move: Analysis or technical report |
| VOLUME_BALANCE_SOLUTION.md | docs | other | docs/VOLUME_BALANCE_SOLUTION.md | ➡️ Move: General documentation |
| api_description.txt | docs | other | docs/api_description.txt | ➡️ Move: General documentation |
| build_android_app.md | docs | guides | docs/guides/build_android_app.md | ➡️ Move: Deployment guide |
| deploy_to_render.md | docs | guides | docs/guides/deploy_to_render.md | ➡️ Move: Deployment guide |
| emotion_color_guide.md | docs | guides | docs/guides/emotion_color_guide.md | ➡️ Move: User guide or checklist |
| project-structure.md | docs | technical/architecture | docs/technical/architecture/project-structure.md | ➡️ Move: Architecture documentation |
| setup_asr_environment.md | docs | technical/asr | docs/technical/asr/setup_asr_environment.md | ➡️ Move: ASR technical guide |
| ✅PWA_Android_App完成.md | docs | status/completed | docs/status/completed/✅PWA_Android_App完成.md | ➡️ Move: Completion status document |
| ✅優化完成_立即測試.md | docs | status/completed | docs/status/completed/✅優化完成_立即測試.md | ➡️ Move: Completion status document |
| ✅完成報告_所有佐證資料已就緒.md | docs | status/completed | docs/status/completed/✅完成報告_所有佐證資料已就緒.md | ➡️ Move: Completion status document |
| ✅工號自動帶出姓名功能完成.md | docs | status/completed | docs/status/completed/✅工號自動帶出姓名功能完成.md | ➡️ Move: Completion status document |
| ✅搜尋與篩選功能完成.md | docs | status/completed | docs/status/completed/✅搜尋與篩選功能完成.md | ➡️ Move: Completion status document |
| ✅碳排放追蹤系統_建置完成.md | docs | status/completed | docs/status/completed/✅碳排放追蹤系統_建置完成.md | ➡️ Move: Completion status document |
| ✅記錄編輯刪除功能完成.md | docs | status/completed | docs/status/completed/✅記錄編輯刪除功能完成.md | ➡️ Move: Completion status document |
| ✅資料匯出功能完成.md | docs | status/completed | docs/status/completed/✅資料匯出功能完成.md | ➡️ Move: Completion status document |
| 優化後模型成效比較報告.md | docs | reports | docs/reports/優化後模型成效比較報告.md | ➡️ Move: Analysis or technical report |
| 完成清單_稽核佐證資料.md | docs | other | docs/完成清單_稽核佐證資料.md | ➡️ Move: General documentation |
| 專案技術分析報告.md | docs | reports | docs/reports/專案技術分析報告.md | ➡️ Move: Analysis or technical report |
| 專業系統驗證及ASR改進整合報告.md | docs | reports | docs/reports/專業系統驗證及ASR改進整合報告.md | ➡️ Move: Analysis or technical report |
| 快速參考卡.md | docs | guides | docs/guides/快速參考卡.md | ➡️ Move: User guide or checklist |
| 推廣成果摘要報告.md | docs | reports | docs/reports/推廣成果摘要報告.md | ➡️ Move: Analysis or technical report |
| 最終檢查清單.md | docs | guides | docs/guides/最終檢查清單.md | ➡️ Move: User guide or checklist |
| 碳排放減少效益分析.md | docs | technical | docs/technical/碳排放減少效益分析.md | ➡️ Move: Technical analysis document |
| 碳排放追蹤系統_使用說明.md | docs | guides | docs/guides/碳排放追蹤系統_使用說明.md | ➡️ Move: User guide or checklist |
| 系統改進建議.md | docs | technical | docs/technical/系統改進建議.md | ➡️ Move: Technical analysis document |
| 給VB3-1 優化後模型成效比較報告.docx | docs | reports | docs/reports/給VB3-1 優化後模型成效比較報告.docx | ➡️ Move: Analysis or technical report |
| 給VB3-2 【菁宸】專業系統驗證及ASR改進整合報告.docx | docs | reports | docs/reports/給VB3-2 【菁宸】專業系統驗證及ASR改進整合報告.docx | ➡️ Move: Analysis or technical report |
| 給VC2-2 推廣成果摘要報告.docx | docs | reports | docs/reports/給VC2-2 推廣成果摘要報告.docx | ➡️ Move: Analysis or technical report |
| 給VC2-3 碳排放減少效益分析.docx | docs | technical | docs/technical/給VC2-3 碳排放減少效益分析.docx | ➡️ Move: Technical analysis document |
| 部署架構優化方案.md | docs | technical/architecture | docs/technical/architecture/部署架構優化方案.md | ➡️ Move: Architecture documentation |
| 部署模式說明.md | docs | guides | docs/guides/部署模式說明.md | ➡️ Move: Deployment guide |
| 部署檢查清單.md | docs | guides | docs/guides/部署檢查清單.md | ➡️ Move: User guide or checklist |
| 開始使用_README.md | docs | other | docs/開始使用_README.md | ➡️ Move: General documentation |
| 🌿淡化綠色主題+分頁功能完成.md | docs | status/completed | docs/status/completed/🌿淡化綠色主題+分頁功能完成.md | ➡️ Move: Completion status document |
| 🌿環保綠色主題優化完成.md | docs | status/completed | docs/status/completed/🌿環保綠色主題優化完成.md | ➡️ Move: Completion status document |
| 🎉PWA轉換完成_快速開始.md | docs | status/completed | docs/status/completed/🎉PWA轉換完成_快速開始.md | ➡️ Move: Completion status document |
| 🎉部署完成_下一步行動.md | docs | status/deployment | docs/status/deployment/🎉部署完成_下一步行動.md | ➡️ Move: Deployment status document |
| 🎉部署成功_開始建置APK.md | docs | status/deployment | docs/status/deployment/🎉部署成功_開始建置APK.md | ➡️ Move: Deployment status document |
| 🎊PWA完整方案_全部完成.md | docs | status/completed | docs/status/completed/🎊PWA完整方案_全部完成.md | ➡️ Move: Completion status document |
| 🎊完整方案_PWA+Android全部完成.md | docs | status/completed | docs/status/completed/🎊完整方案_PWA+Android全部完成.md | ➡️ Move: Completion status document |
| 📱Android_App建置完成.md | docs | status/completed | docs/status/completed/📱Android_App建置完成.md | ➡️ Move: Completion status document |
| 📱轉換為Android_App指南.md | docs | status/completed | docs/status/completed/📱轉換為Android_App指南.md | ➡️ Move: Completion status document |
| 🔧修復完成_等待部署.md | docs | status/deployment | docs/status/deployment/🔧修復完成_等待部署.md | ➡️ Move: Deployment status document |
| 🚀APK建置與上架完整指南.md | docs | status/completed | docs/status/completed/🚀APK建置與上架完整指南.md | ➡️ Move: Completion status document |
| 🚀快速啟動指南.md | docs | status/completed | docs/status/completed/🚀快速啟動指南.md | ➡️ Move: Completion status document |
| database_carbon_tracking.py | modules | carbon_tracking | modules/carbon_tracking/database_carbon_tracking.py | ➡️ Move: Carbon tracking module |
| database_emotion_extension.py | modules | voice_processing | modules/voice_processing/database_emotion_extension.py | ➡️ Move: Voice processing module |
| simple_voice_api.py | modules | voice_processing | modules/voice_processing/simple_voice_api.py | ➡️ Move: Voice processing module |
| talent_assessment_db_connector.py | modules | talent_assessment | modules/talent_assessment/talent_assessment_db_connector.py | ➡️ Move: Talent assessment module |
| talent_assessment_llm_query_generator.py | modules | talent_assessment | modules/talent_assessment/talent_assessment_llm_query_generator.py | ➡️ Move: Talent assessment module |
| talent_assessment_query_validator.py | modules | talent_assessment | modules/talent_assessment/talent_assessment_query_validator.py | ➡️ Move: Talent assessment module |
| voice_clone_service.py | modules | voice_processing | modules/voice_processing/voice_clone_service.py | ➡️ Move: Voice processing module |
| voice_config.py | modules | voice_processing | modules/voice_processing/voice_config.py | ➡️ Move: Voice processing module |
| voice_dataset_validation_system.py | modules | voice_processing | modules/voice_processing/voice_dataset_validation_system.py | ➡️ Move: Voice processing module |
| voice_synthesis_service.py | modules | voice_processing | modules/voice_processing/voice_synthesis_service.py | ➡️ Move: Voice processing module |
| add_more_social_workers.py | scripts | data_processing | scripts/data_processing/add_more_social_workers.py | ➡️ Move: Data processing script |
| advanced_voice_separation.py | scripts | data_processing | scripts/data_processing/advanced_voice_separation.py | ➡️ Move: Voice separation processing script |
| audio_voice_separation.py | scripts | data_processing | scripts/data_processing/audio_voice_separation.py | ➡️ Move: Voice separation processing script |
| batch_validation_processor.py | scripts | validation | scripts/validation/batch_validation_processor.py | ➡️ Move: Validation script |
| check_audio_files.py | scripts | validation | scripts/validation/check_audio_files.py | ➡️ Move: Check/validation script |
| check_emotion_methods.py | scripts | validation | scripts/validation/check_emotion_methods.py | ➡️ Move: Check/validation script |
| check_social_worker_names.py | scripts | validation | scripts/validation/check_social_worker_names.py | ➡️ Move: Check/validation script |
| dataset_validation_dashboard.py | scripts | validation | scripts/validation/dataset_validation_dashboard.py | ➡️ Move: Validation dashboard script |
| debug_voice_models.py | scripts | monitoring | scripts/monitoring/debug_voice_models.py | ➡️ Move: Monitoring/debugging script |
| download_epa_document.py | scripts | downloads | scripts/downloads/download_epa_document.py | ➡️ Move: Download script |
| download_funasr_model.py | scripts | downloads | scripts/downloads/download_funasr_model.py | ➡️ Move: Download script |
| final_tag_validation.py | scripts | validation | scripts/validation/final_tag_validation.py | ➡️ Move: Validation script |
| generate_carbon_dashboard_images.py | scripts | data_generation | scripts/data_generation/generate_carbon_dashboard_images.py | ➡️ Move: Data generation script |
| generate_carbon_emission_tables.py | scripts | data_generation | scripts/data_generation/generate_carbon_emission_tables.py | ➡️ Move: Data generation script |
| generate_epa_document_images.py | scripts | data_generation | scripts/data_generation/generate_epa_document_images.py | ➡️ Move: Data generation script |
| generate_file_classification.py | scripts | data_generation | scripts/data_generation/generate_file_classification.py | ➡️ Move: Data generation script |
| generate_mock_carbon_data.py | scripts | data_generation | scripts/data_generation/generate_mock_carbon_data.py | ➡️ Move: Data generation script |
| generate_pwa_icons.py | scripts | data_generation | scripts/data_generation/generate_pwa_icons.py | ➡️ Move: Data generation script |
| install-gpt-sovits.bat | scripts | startup | scripts/startup/install-gpt-sovits.bat | ➡️ Move: Startup/setup script |
| monitor_deployment.py | scripts | monitoring | scripts/monitoring/monitor_deployment.py | ➡️ Move: Monitoring/debugging script |
| natural_voice_separation.py | scripts | data_processing | scripts/data_processing/natural_voice_separation.py | ➡️ Move: Voice separation processing script |
| optimized_natural_voice_separation.py | scripts | data_processing | scripts/data_processing/optimized_natural_voice_separation.py | ➡️ Move: Voice separation processing script |
| prepare_reorganization.py | scripts | other | scripts/prepare_reorganization.py | ➡️ Move: Project reorganization script |
| process_03041966_audio.py | scripts | data_processing | scripts/data_processing/process_03041966_audio.py | ➡️ Move: Audio/voice processing script |
| process_advanced_03041966.py | scripts | data_processing | scripts/data_processing/process_advanced_03041966.py | ➡️ Move: Data processing script |
| process_natural_03041966.py | scripts | data_processing | scripts/data_processing/process_natural_03041966.py | ➡️ Move: Data processing script |
| setup-voice-system.bat | scripts | startup | scripts/startup/setup-voice-system.bat | ➡️ Move: Startup/setup script |
| show_all_workers_stats.py | scripts | monitoring | scripts/monitoring/show_all_workers_stats.py | ➡️ Move: Monitoring/debugging script |
| start-gpt-sovits.bat | scripts | startup | scripts/startup/start-gpt-sovits.bat | ➡️ Move: Startup/setup script |
| start-voice-api.bat | scripts | startup | scripts/startup/start-voice-api.bat | ➡️ Move: Startup/setup script |
| start-voice-clone-service.bat | scripts | startup | scripts/startup/start-voice-clone-service.bat | ➡️ Move: Startup/setup script |
| start_carbon_tracking.bat | scripts | startup | scripts/startup/start_carbon_tracking.bat | ➡️ Move: Startup/setup script |
| update_names_extended.py | scripts | data_processing | scripts/data_processing/update_names_extended.py | ➡️ Move: Data processing script |
| update_social_worker_names.py | scripts | data_processing | scripts/data_processing/update_social_worker_names.py | ➡️ Move: Data processing script |
| volume_balanced_voice_separation.py | scripts | data_processing | scripts/data_processing/volume_balanced_voice_separation.py | ➡️ Move: Voice separation processing script |
| test_asr_api.py | tests | integration | tests/integration/test_asr_api.py | ➡️ Move: Integration test |
| test_asr_coordinator.py | tests | integration | tests/integration/test_asr_coordinator.py | ➡️ Move: Integration test |
| test_asr_performance.py | tests | performance | tests/performance/test_asr_performance.py | ➡️ Move: Performance test |
| test_asr_setup.py | tests | performance | tests/performance/test_asr_setup.py | ➡️ Move: Performance test |
| test_carbon_system.py | tests | integration | tests/integration/test_carbon_system.py | ➡️ Move: Integration test |
| test_deployment.py | tests | deployment | tests/deployment/test_deployment.py | ➡️ Move: Deployment test |
| test_elderly_detector.py | tests | unit | tests/unit/test_elderly_detector.py | ➡️ Move: Unit test for specific component |
| test_funasr_engine.py | tests | integration | tests/integration/test_funasr_engine.py | ➡️ Move: Integration test |
| test_minimal_app.py | tests | integration | tests/integration/test_minimal_app.py | ➡️ Move: Integration test |
| test_minnan_detector.py | tests | unit | tests/unit/test_minnan_detector.py | ➡️ Move: Unit test for specific component |
| test_pwa.html | tests | deployment | tests/deployment/test_pwa.html | ➡️ Move: PWA deployment test |
| test_pwa_features.bat | tests | deployment | tests/deployment/test_pwa_features.bat | ➡️ Move: PWA deployment test |
| .gitignore | unknown |  | .gitignore | ✅ Keep in root: Core application file |
| app.py | unknown |  | app.py | ✅ Keep in root: Core application file |
| auth.py | unknown |  | auth.py | ✅ Keep in root: Core application file |
| config.py | unknown |  | config.py | ✅ Keep in root: Core application file |
| database.py | unknown |  | database.py | ✅ Keep in root: Core application file |
| migration_log.json | unknown |  | migration_log.json | ✅ Keep in root: Core application file |
| utils.py | unknown |  | utils.py | ✅ Keep in root: Core application file |

## Python Files Requiring Import Updates

**Total:** 46 files

| File | New Path | Dependencies |
|------|----------|--------------|
| add_more_social_workers.py | scripts/data_processing/add_more_social_workers.py | random, sqlite3, datetime |
| advanced_voice_separation.py | scripts/data_processing/advanced_voice_separation.py | numpy, soundfile, noisereduce, scipy, sys (+10 more) |
| audio_voice_separation.py | scripts/data_processing/audio_voice_separation.py | numpy, soundfile, noisereduce, scipy, sys (+5 more) |
| batch_validation_processor.py | scripts/validation/batch_validation_processor.py | typing, hashlib, tqdm, voice_dataset_validation_system, pandas (+8 more) |
| check_audio_files.py | scripts/validation/check_audio_files.py | config, sqlite3, database, os |
| check_emotion_methods.py | scripts/validation/check_emotion_methods.py | re |
| check_social_worker_names.py | scripts/validation/check_social_worker_names.py | sqlite3 |
| database_carbon_tracking.py | modules/carbon_tracking/database_carbon_tracking.py | datetime, pathlib, sqlite3 |
| database_emotion_extension.py | modules/voice_processing/database_emotion_extension.py | config, sqlite3 |
| dataset_validation_dashboard.py | scripts/validation/dataset_validation_dashboard.py | streamlit, sqlite3, voice_dataset_validation_system, pandas, datetime (+3 more) |
| debug_voice_models.py | scripts/monitoring/debug_voice_models.py | config, sqlite3, database |
| download_epa_document.py | scripts/downloads/download_epa_document.py | pathlib, requests, json |
| download_funasr_model.py | scripts/downloads/download_funasr_model.py | sys, os |
| final_tag_validation.py | scripts/validation/final_tag_validation.py | re |
| generate_carbon_dashboard_images.py | scripts/data_generation/generate_carbon_dashboard_images.py | numpy, datetime, pathlib, matplotlib.patches, matplotlib |
| generate_carbon_emission_tables.py | scripts/data_generation/generate_carbon_emission_tables.py | datetime, openpyxl, openpyxl.utils, openpyxl.styles |
| generate_epa_document_images.py | scripts/data_generation/generate_epa_document_images.py | pathlib, PIL |
| generate_file_classification.py | scripts/data_generation/generate_file_classification.py | typing, re, datetime, pathlib, json (+1 more) |
| generate_mock_carbon_data.py | scripts/data_generation/generate_mock_carbon_data.py | random, database_carbon_tracking, datetime |
| generate_pwa_icons.py | scripts/data_generation/generate_pwa_icons.py | PIL, os |
| monitor_deployment.py | scripts/monitoring/monitor_deployment.py | datetime, time, requests |
| natural_voice_separation.py | scripts/data_processing/natural_voice_separation.py | numpy, soundfile, noisereduce, scipy, sys (+9 more) |
| optimized_natural_voice_separation.py | scripts/data_processing/optimized_natural_voice_separation.py | numpy, soundfile, noisereduce, scipy, sys (+4 more) |
| prepare_reorganization.py | scripts/prepare_reorganization.py | datetime, json, subprocess, shutil, os |
| process_03041966_audio.py | scripts/data_processing/process_03041966_audio.py | sys, audio_voice_separation, os |
| process_advanced_03041966.py | scripts/data_processing/process_advanced_03041966.py | sys, advanced_voice_separation, os |
| process_natural_03041966.py | scripts/data_processing/process_natural_03041966.py | sys, natural_voice_separation, os |
| show_all_workers_stats.py | scripts/monitoring/show_all_workers_stats.py | sqlite3 |
| simple_voice_api.py | modules/voice_processing/simple_voice_api.py | numpy, soundfile, sys, tempfile, logging (+4 more) |
| talent_assessment_llm_query_generator.py | modules/talent_assessment/talent_assessment_llm_query_generator.py | openai, re, talent_assessment_query_validator, json, typing |
| talent_assessment_query_validator.py | modules/talent_assessment/talent_assessment_query_validator.py | re, typing |
| test_asr_api.py | tests/integration/test_asr_api.py | os, requests, json |
| test_asr_coordinator.py | tests/integration/test_asr_coordinator.py | numpy, services.asr.coordinator, soundfile, asyncio |
| test_asr_performance.py | tests/performance/test_asr_performance.py | numpy, soundfile, time, services.asr.coordinator, io (+1 more) |
| test_asr_setup.py | tests/performance/test_asr_setup.py | sys, importlib |
| test_deployment.py | tests/deployment/test_deployment.py | requests, json |
| test_elderly_detector.py | tests/unit/test_elderly_detector.py | numpy, services.asr.elderly_detector, logging |
| test_funasr_engine.py | tests/integration/test_funasr_engine.py | numpy, services.asr.funasr_engine, logging, asyncio |
| test_minimal_app.py | tests/integration/test_minimal_app.py | sys |
| test_minnan_detector.py | tests/unit/test_minnan_detector.py | numpy, services.asr.minnan_detector, logging |
| update_names_extended.py | scripts/data_processing/update_names_extended.py | random, sqlite3 |
| update_social_worker_names.py | scripts/data_processing/update_social_worker_names.py | random, sqlite3 |
| voice_clone_service.py | modules/voice_processing/voice_clone_service.py | numpy, typing, soundfile, requests, sys (+12 more) |
| voice_dataset_validation_system.py | modules/voice_processing/voice_dataset_validation_system.py | numpy, hashlib, typing, sqlite3, pandas (+7 more) |
| voice_synthesis_service.py | modules/voice_processing/voice_synthesis_service.py | requests, logging, io, json, base64 (+2 more) |
| volume_balanced_voice_separation.py | scripts/data_processing/volume_balanced_voice_separation.py | numpy, soundfile, noisereduce, scipy, sys (+7 more) |

## Archive Candidates

**Total:** 4 files

| File | New Path | Reason |
|------|----------|--------|
| requirements_250521.txt | archive/2025-11/old_requirements/requirements_250521.txt | Old or backup requirements file |
| requirements_audio_separation.txt | archive/2025-11/old_requirements/requirements_audio_separation.txt | Old or backup requirements file |
| requirements_backup.txt | archive/2025-11/old_requirements/requirements_backup.txt | Old or backup requirements file |
| validate_vue_component.js | archive/2025-11/old_scripts/validate_vue_component.js | Old or obsolete script |

## Migration Mapping

Complete mapping of original paths to new paths for migration scripts:

```json
{
  ".agent.md": "docs/.agent.md",
  "add_more_social_workers.py": "scripts/data_processing/add_more_social_workers.py",
  "advanced_voice_separation.py": "scripts/data_processing/advanced_voice_separation.py",
  "ADVANCED_VOICE_SEPARATION_GUIDE.md": "docs/technical/voice/ADVANCED_VOICE_SEPARATION_GUIDE.md",
  "AI_CORE_MODULES_ARCHITECTURE_REPORT.md": "docs/reports/AI_CORE_MODULES_ARCHITECTURE_REPORT.md",
  "Android_App功能相容性分析.md": "docs/guides/Android_App功能相容性分析.md",
  "api_description.txt": "docs/api_description.txt",
  "AUDIO_SEPARATION_GUIDE.md": "docs/technical/voice/AUDIO_SEPARATION_GUIDE.md",
  "audio_voice_separation.py": "scripts/data_processing/audio_voice_separation.py",
  "BACKEND_TECHNICAL_DOCUMENTATION.md": "docs/technical/backend/BACKEND_TECHNICAL_DOCUMENTATION.md",
  "batch_validation_processor.py": "scripts/validation/batch_validation_processor.py",
  "build_android_app.md": "docs/guides/build_android_app.md",
  "carbon_tracking.db": "data/databases/carbon_tracking.db",
  "carbon_tracking_backup_20251110_072639.db": "backups/databases/carbon_tracking_backup_20251110_072639.db",
  "carbon_tracking_backup_20251110_072934.db": "backups/databases/carbon_tracking_backup_20251110_072934.db",
  "carbon_tracking_backup_20251110_073307.db": "backups/databases/carbon_tracking_backup_20251110_073307.db",
  "check_audio_files.py": "scripts/validation/check_audio_files.py",
  "check_emotion_methods.py": "scripts/validation/check_emotion_methods.py",
  "check_social_worker_names.py": "scripts/validation/check_social_worker_names.py",
  "CLEANUP_SUMMARY.md": "docs/CLEANUP_SUMMARY.md",
  "customer_service.db": "data/databases/customer_service.db",
  "database_carbon_tracking.py": "modules/carbon_tracking/database_carbon_tracking.py",
  "database_emotion_extension.py": "modules/voice_processing/database_emotion_extension.py",
  "dataset_validation_dashboard.py": "scripts/validation/dataset_validation_dashboard.py",
  "debug_voice_models.py": "scripts/monitoring/debug_voice_models.py",
  "deploy_to_render.md": "docs/guides/deploy_to_render.md",
  "Dockerfile.voice-api": "config/deployment/Dockerfile.voice-api",
  "download_epa_document.py": "scripts/downloads/download_epa_document.py",
  "download_funasr_model.py": "scripts/downloads/download_funasr_model.py",
  "ELDERLY_VOICE_DATASET_VALIDATION_REPORT.md": "docs/reports/ELDERLY_VOICE_DATASET_VALIDATION_REPORT.md",
  "emotion_color_guide.md": "docs/guides/emotion_color_guide.md",
  "f5-tts API.json": "config/api_specs/f5-tts-api.json",
  "file_classification_report.json": "",
  "FILE_CLASSIFICATION_REPORT.md": "docs/reports/FILE_CLASSIFICATION_REPORT.md",
  "FILE_ORGANIZATION_STANDARD.md": "docs/FILE_ORGANIZATION_STANDARD.md",
  "final_tag_validation.py": "scripts/validation/final_tag_validation.py",
  "FRONTEND_TECHNICAL_DOCUMENTATION.md": "docs/technical/frontend/FRONTEND_TECHNICAL_DOCUMENTATION.md",
  "generate_carbon_dashboard_images.py": "scripts/data_generation/generate_carbon_dashboard_images.py",
  "generate_carbon_emission_tables.py": "scripts/data_generation/generate_carbon_emission_tables.py",
  "generate_epa_document_images.py": "scripts/data_generation/generate_epa_document_images.py",
  "generate_file_classification.py": "scripts/data_generation/generate_file_classification.py",
  "generate_mock_carbon_data.py": "scripts/data_generation/generate_mock_carbon_data.py",
  "generate_pwa_icons.py": "scripts/data_generation/generate_pwa_icons.py",
  "Gpt-Sovis-API.docx": "docs/Gpt-Sovis-API.docx",
  "Gpt-Sovis-API.md": "docs/Gpt-Sovis-API.md",
  "gpt-sovits-api.json": "config/api_specs/gpt-sovits-api.json",
  "GPT_SOVITS_FINE_TUNING_GUIDE.md": "docs/technical/voice/GPT_SOVITS_FINE_TUNING_GUIDE.md",
  "install-gpt-sovits.bat": "scripts/startup/install-gpt-sovits.bat",
  "MODEL_STORAGE_DEPLOYMENT_GUIDE.md": "docs/technical/voice/MODEL_STORAGE_DEPLOYMENT_GUIDE.md",
  "MODEL_WEIGHTS_CONFIGURATION_GUIDE.md": "docs/technical/voice/MODEL_WEIGHTS_CONFIGURATION_GUIDE.md",
  "MODULE_TESTING_REPORT.md": "docs/reports/MODULE_TESTING_REPORT.md",
  "monitor_deployment.py": "scripts/monitoring/monitor_deployment.py",
  "natural_voice_separation.py": "scripts/data_processing/natural_voice_separation.py",
  "NATURAL_VS_ADVANCED_COMPARISON.md": "docs/NATURAL_VS_ADVANCED_COMPARISON.md",
  "nginx-voice.conf": "config/deployment/nginx-voice.conf",
  "NOISE_REDUCTION_IMPROVEMENT_REPORT.md": "docs/reports/NOISE_REDUCTION_IMPROVEMENT_REPORT.md",
  "optimized_natural_voice_separation.py": "scripts/data_processing/optimized_natural_voice_separation.py",
  "prepare_reorganization.py": "scripts/prepare_reorganization.py",
  "process_03041966_audio.py": "scripts/data_processing/process_03041966_audio.py",
  "process_advanced_03041966.py": "scripts/data_processing/process_advanced_03041966.py",
  "process_natural_03041966.py": "scripts/data_processing/process_natural_03041966.py",
  "project-structure.md": "docs/technical/architecture/project-structure.md",
  "PWA檢查清單.md": "docs/guides/PWA檢查清單.md",
  "PYTHON_313_COMPATIBILITY_FIX.md": "docs/PYTHON_313_COMPATIBILITY_FIX.md",
  "render.yaml": "config/deployment/render.yaml",
  "Render部署問題排查.md": "docs/guides/Render部署問題排查.md",
  "requirements-asr.txt": "config/requirements/asr.txt",
  "requirements-voice.txt": "config/requirements/voice.txt",
  "requirements.txt": "config/requirements/base.txt",
  "requirements_250521.txt": "archive/2025-11/old_requirements/requirements_250521.txt",
  "requirements_audio_separation.txt": "archive/2025-11/old_requirements/requirements_audio_separation.txt",
  "requirements_backup.txt": "archive/2025-11/old_requirements/requirements_backup.txt",
  "requirements_carbon_only.txt": "config/requirements/carbon.txt",
  "requirements_full.txt": "config/requirements/full.txt",
  "requirements_minimal.txt": "config/requirements/minimal.txt",
  "setup-voice-system.bat": "scripts/startup/setup-voice-system.bat",
  "setup_asr_environment.md": "docs/technical/asr/setup_asr_environment.md",
  "show_all_workers_stats.py": "scripts/monitoring/show_all_workers_stats.py",
  "simple_voice_api.py": "modules/voice_processing/simple_voice_api.py",
  "start-gpt-sovits.bat": "scripts/startup/start-gpt-sovits.bat",
  "start-voice-api.bat": "scripts/startup/start-voice-api.bat",
  "start-voice-clone-service.bat": "scripts/startup/start-voice-clone-service.bat",
  "start_carbon_tracking.bat": "scripts/startup/start_carbon_tracking.bat",
  "SYSTEM_ARCHITECTURE_DIAGRAM.svg": "docs/technical/architecture/SYSTEM_ARCHITECTURE_DIAGRAM.svg",
  "talent_assessment_db_connector.py": "modules/talent_assessment/talent_assessment_db_connector.py",
  "talent_assessment_llm_query_generator.py": "modules/talent_assessment/talent_assessment_llm_query_generator.py",
  "talent_assessment_query_validator.py": "modules/talent_assessment/talent_assessment_query_validator.py",
  "test_asr_api.py": "tests/integration/test_asr_api.py",
  "test_asr_coordinator.py": "tests/integration/test_asr_coordinator.py",
  "test_asr_performance.py": "tests/performance/test_asr_performance.py",
  "test_asr_setup.py": "tests/performance/test_asr_setup.py",
  "test_carbon_system.py": "tests/integration/test_carbon_system.py",
  "test_deployment.py": "tests/deployment/test_deployment.py",
  "test_elderly_detector.py": "tests/unit/test_elderly_detector.py",
  "test_funasr_engine.py": "tests/integration/test_funasr_engine.py",
  "test_minimal_app.py": "tests/integration/test_minimal_app.py",
  "test_minnan_detector.py": "tests/unit/test_minnan_detector.py",
  "test_pwa.html": "tests/deployment/test_pwa.html",
  "test_pwa_features.bat": "tests/deployment/test_pwa_features.bat",
  "UI優化完成說明.md": "docs/technical/UI優化完成說明.md",
  "update_names_extended.py": "scripts/data_processing/update_names_extended.py",
  "update_social_worker_names.py": "scripts/data_processing/update_social_worker_names.py",
  "validate_vue_component.js": "archive/2025-11/old_scripts/validate_vue_component.js",
  "VOICE_CLONE_GUIDE.md": "docs/technical/voice/VOICE_CLONE_GUIDE.md",
  "voice_clone_service.py": "modules/voice_processing/voice_clone_service.py",
  "VOICE_CLONE_SETUP.md": "docs/technical/voice/VOICE_CLONE_SETUP.md",
  "voice_config.py": "modules/voice_processing/voice_config.py",
  "voice_dataset_validation.log": "data/logs/voice_dataset_validation.log",
  "VOICE_DATASET_VALIDATION_GUIDE.md": "docs/technical/voice/VOICE_DATASET_VALIDATION_GUIDE.md",
  "voice_dataset_validation_system.py": "modules/voice_processing/voice_dataset_validation_system.py",
  "VOICE_DATA_PROCESSING_AND_AI_MODULES_REPORT.md": "docs/reports/VOICE_DATA_PROCESSING_AND_AI_MODULES_REPORT.md",
  "voice_synthesis_service.py": "modules/voice_processing/voice_synthesis_service.py",
  "volume_balanced_voice_separation.py": "scripts/data_processing/volume_balanced_voice_separation.py",
  "VOLUME_BALANCE_SOLUTION.md": "docs/VOLUME_BALANCE_SOLUTION.md",
  "✅PWA_Android_App完成.md": "docs/status/completed/✅PWA_Android_App完成.md",
  "✅優化完成_立即測試.md": "docs/status/completed/✅優化完成_立即測試.md",
  "✅完成報告_所有佐證資料已就緒.md": "docs/status/completed/✅完成報告_所有佐證資料已就緒.md",
  "✅工號自動帶出姓名功能完成.md": "docs/status/completed/✅工號自動帶出姓名功能完成.md",
  "✅搜尋與篩選功能完成.md": "docs/status/completed/✅搜尋與篩選功能完成.md",
  "✅碳排放追蹤系統_建置完成.md": "docs/status/completed/✅碳排放追蹤系統_建置完成.md",
  "✅記錄編輯刪除功能完成.md": "docs/status/completed/✅記錄編輯刪除功能完成.md",
  "✅資料匯出功能完成.md": "docs/status/completed/✅資料匯出功能完成.md",
  "優化後模型成效比較報告.md": "docs/reports/優化後模型成效比較報告.md",
  "完成清單_稽核佐證資料.md": "docs/完成清單_稽核佐證資料.md",
  "專案技術分析報告.md": "docs/reports/專案技術分析報告.md",
  "專業系統驗證及ASR改進整合報告.md": "docs/reports/專業系統驗證及ASR改進整合報告.md",
  "快速參考卡.md": "docs/guides/快速參考卡.md",
  "推廣成果摘要報告.md": "docs/reports/推廣成果摘要報告.md",
  "最終檢查清單.md": "docs/guides/最終檢查清單.md",
  "碳排放減少效益分析.md": "docs/technical/碳排放減少效益分析.md",
  "碳排放減少效益分析_佐證表格.xlsx": "data/reports/碳排放減少效益分析_佐證表格.xlsx",
  "碳排放追蹤系統_使用說明.md": "docs/guides/碳排放追蹤系統_使用說明.md",
  "社工交通工具使用調查報告.xlsx": "data/reports/社工交通工具使用調查報告.xlsx",
  "系統改進建議.md": "docs/technical/系統改進建議.md",
  "給VB3-1 優化後模型成效比較報告.docx": "docs/reports/給VB3-1 優化後模型成效比較報告.docx",
  "給VB3-2 【菁宸】專業系統驗證及ASR改進整合報告.docx": "docs/reports/給VB3-2 【菁宸】專業系統驗證及ASR改進整合報告.docx",
  "給VC2-2 推廣成果摘要報告.docx": "docs/reports/給VC2-2 推廣成果摘要報告.docx",
  "給VC2-3 碳排放減少效益分析.docx": "docs/technical/給VC2-3 碳排放減少效益分析.docx",
  "部署架構優化方案.md": "docs/technical/architecture/部署架構優化方案.md",
  "部署模式說明.md": "docs/guides/部署模式說明.md",
  "部署檢查清單.md": "docs/guides/部署檢查清單.md",
  "開始使用_README.md": "docs/開始使用_README.md",
  "🌿淡化綠色主題+分頁功能完成.md": "docs/status/completed/🌿淡化綠色主題+分頁功能完成.md",
  "🌿環保綠色主題優化完成.md": "docs/status/completed/🌿環保綠色主題優化完成.md",
  "🎉PWA轉換完成_快速開始.md": "docs/status/completed/🎉PWA轉換完成_快速開始.md",
  "🎉部署完成_下一步行動.md": "docs/status/deployment/🎉部署完成_下一步行動.md",
  "🎉部署成功_開始建置APK.md": "docs/status/deployment/🎉部署成功_開始建置APK.md",
  "🎊PWA完整方案_全部完成.md": "docs/status/completed/🎊PWA完整方案_全部完成.md",
  "🎊完整方案_PWA+Android全部完成.md": "docs/status/completed/🎊完整方案_PWA+Android全部完成.md",
  "📱Android_App建置完成.md": "docs/status/completed/📱Android_App建置完成.md",
  "📱轉換為Android_App指南.md": "docs/status/completed/📱轉換為Android_App指南.md",
  "🔧修復完成_等待部署.md": "docs/status/deployment/🔧修復完成_等待部署.md",
  "🚀APK建置與上架完整指南.md": "docs/status/completed/🚀APK建置與上架完整指南.md",
  "🚀快速啟動指南.md": "docs/status/completed/🚀快速啟動指南.md"
}
```

---

**Note:** This report should be reviewed before executing any file migrations.
Verify that all classifications are correct and paths are appropriate.