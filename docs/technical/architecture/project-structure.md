# 專案目錄結構

以下是完整的專案目錄結構，經過重構後更有組織性和可維護性：

```
Flask-AICares/
│
├── app.py                     # 主應用入口
├── config.py                  # 配置相關
├── database.py                # 數據庫操作
├── utils.py                   # 工具函數
├── requirements.txt           # 依賴包列表
├── __init__.py                # 套件標記文件
│
├── routes/                    # 路由模塊
│   ├── __init__.py           # 套件標記文件
│   ├── main.py               # 主要路由
│   ├── staff.py              # 客服專員相關路由
│   └── audio.py              # 音頻相關路由
│
├── services/                  # 服務模塊
│   ├── __init__.py           # 套件標記文件
│   ├── speech.py             # 語音轉文字相關
│   ├── ai.py                 # AI 分析和回應
│   └── tts.py                # 語音合成相關
│
├── templates/                 # HTML 模板
│   └── index.html            # 主頁模板
│
├── static/                    # 靜態資源
│   ├── css/                  # CSS 檔案
│   ├── js/                   # JavaScript 檔案
│   └── audio/                # 生成的音頻檔案
│
├── mockvoice/                 # 模擬聲音檔案存儲
├── genvoice/                  # 生成的聲音檔案存儲
└── audio_uploads/             # 上傳的音頻檔案存儲
    ├── staff_code1/          # 按照客服專員代號組織
    ├── staff_code2/
    └── ...
```

## 模塊說明

1. **主應用入口 (app.py)**
   - 初始化 Flask 應用
   - 註冊藍圖
   - 應用程序啟動點

2. **配置模塊 (config.py)**
   - 儲存配置常量
   - 目錄初始化函數
   - 檔案類型檢查函數

3. **數據庫模塊 (database.py)**
   - 資料庫初始化
   - 客服專員資料操作
   - 音頻記錄資料操作
   - 通用查詢輔助函數

4. **工具模塊 (utils.py)**
   - 檔案大小格式化
   - JSON 文本修復
   - 檔案處理輔助函數

5. **路由模塊 (routes/)**
   - **main.py**: 首頁、處理上傳音頻、TTS 等主要功能
   - **staff.py**: 客服專員 CRUD 操作
   - **audio.py**: 音頻記錄 CRUD 操作

6. **服務模塊 (services/)**
   - **speech.py**: 語音轉文字功能
   - **ai.py**: AI 分析和回應
   - **tts.py**: 語音合成功能
