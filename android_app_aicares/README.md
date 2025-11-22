# AI 客服語音克隆系統 - Android APP

> 完整的 AI 客服系統 Android 應用程式，包含語音識別、語音合成、情緒識別等功能

## 📱 應用程式資訊

- **應用程式名稱：** AI 客服系統
- **套件名稱：** com.aicares.app
- **版本：** 1.0.0
- **最低 Android 版本：** 7.0 (API 24)
- **目標 Android 版本：** 14 (API 34)

## 🌐 伺服器配置

- **開發環境：** http://192.168.1.102:5000
- **生產環境：** 待部署

## ✨ 功能模組

### AI 功能

- 🎤 ASR 語音識別
- 🔊 TTS 文字轉語音
- 🎭 語音克隆
- 💬 語音對話
- 😊 情緒識別

### 管理功能

- 👥 員工管理
- 🎵 音訊處理
- 🌱 碳排放追蹤

### 系統功能

- 🔐 JWT 認證系統
- 🏠 主頁面導航

## 🚀 快速開始

### 方法 1：使用批次檔（最快）

```bash
雙擊執行：🎯立即建置.bat
```

### 方法 2：使用 Android Studio

1. 開啟 Android Studio
2. File → Open → 選擇此資料夾
3. 等待 Gradle 同步完成
4. Build → Build APK

### 方法 3：使用命令列

```bash
gradlew clean
gradlew assembleDebug
```

## 📦 APK 輸出位置

```
app/build/outputs/apk/debug/app-debug.apk
```

## 📱 安裝方式

### USB 連接

1. 開啟手機的「開發者選項」和「USB 偵錯」
2. 連接 USB 線
3. 在 Android Studio 點擊 Run

### 直接安裝

1. 將 APK 傳到手機
2. 點擊 APK 檔案
3. 允許「安裝未知來源」
4. 完成安裝

## 🔐 權限說明

- **INTERNET** - 連接後端伺服器（必要）
- **ACCESS_NETWORK_STATE** - 檢查網路狀態（必要）
- **RECORD_AUDIO** - 語音輸入功能（語音功能必要）
- **MODIFY_AUDIO_SETTINGS** - 調整音訊設定（語音功能必要）
- **WRITE/READ_EXTERNAL_STORAGE** - 快取音訊檔案（選用）

## 📚 說明文件

- [🎉 完成！開始使用](🎉完成！開始使用.md) - 快速入門指南
- [✅ 最終配置完成](✅最終配置完成.md) - 配置說明
- [✅ 圖示已創建](✅圖示已創建.md) - 圖示更換指南
- [🚀 快速建置指南](🚀快速建置指南.md) - 詳細建置步驟
- [⚙️ 配置說明](⚙️配置說明.md) - 配置選項
- [🔍 問題排查指南](🔍問題排查指南.md) - 問題解決方案
- [📋 兩個 APP 的差異](📋兩個APP的差異.md) - 與碳排放 APP 的對比

## 🎨 主題設計

- **主色調：** 紫色 (#667eea)
- **深色主色：** #764ba2
- **強調色：** #f093fb
- **風格：** 現代科技感

## 🔧 技術架構

- **前端：** WebView（載入 Flask 網頁）
- **後端：** Flask + Python
- **通訊：** HTTP/HTTPS
- **語言：** Kotlin

## 📊 專案結構

```
android_app_aicares/
├── app/
│   ├── src/main/
│   │   ├── java/com/aicares/app/
│   │   │   ├── MainActivity.kt          # 主活動
│   │   │   └── SplashActivity.kt        # 啟動畫面
│   │   ├── res/
│   │   │   ├── drawable/                # 圖示資源
│   │   │   ├── layout/                  # 佈局文件
│   │   │   ├── values/                  # 字串、顏色、主題
│   │   │   └── xml/                     # 配置文件
│   │   └── AndroidManifest.xml          # 應用程式清單
│   ├── build.gradle                     # APP 建置配置
│   └── proguard-rules.pro              # 混淆規則
├── gradle/                              # Gradle Wrapper
├── build.gradle                         # 專案建置配置
├── settings.gradle                      # 專案設定
├── gradle.properties                    # Gradle 屬性
└── 說明文件/                            # 各種說明文件
```

## 🆚 與碳排放 APP 的差異

| 項目   | 碳排放 APP             | AI 客服 APP         |
| ------ | ---------------------- | ------------------- |
| 目錄   | android_app            | android_app_aicares |
| 套件名 | com.carbontracking.app | com.aicares.app     |
| 功能   | 碳排放追蹤             | 完整 AI 功能        |
| 伺服器 | 雲端部署               | 本地開發            |
| 主題色 | 綠色                   | 紫色                |
| 權限   | 基本                   | 基本 + 語音         |

兩個 APP 可以同時安裝在同一支手機上！

## ✅ 測試清單

- [ ] APP 能正常啟動
- [ ] 顯示 Splash 畫面
- [ ] 能連接到伺服器
- [ ] 能看到網頁內容
- [ ] 導航功能正常
- [ ] 返回鍵正常
- [ ] 下拉重新整理正常
- [ ] 權限請求正常
- [ ] 語音功能正常（如果有）

## 🐛 常見問題

### 無法連接伺服器

- 確認伺服器正在運行
- 確認手機和電腦在同一 WiFi
- 檢查防火牆設定

### Gradle 同步失敗

- 檢查網路連線
- 清除快取：File → Invalidate Caches / Restart

### 建置失敗

- 查看錯誤訊息
- 參考「問題排查指南」

## 📞 技術支援

如有問題，請參考：

1. 說明文件（上方列表）
2. 問題排查指南
3. Android Studio 的 Logcat

## 📝 版本歷史

### v1.0.0 (2024-11-12)

- ✅ 初始版本
- ✅ 完整的 AI 功能模組
- ✅ WebView 整合
- ✅ 權限管理
- ✅ Splash 畫面

## 📄 授權

此專案為內部使用。

## 🎉 開始使用

現在就開始建置你的 AI 客服系統 Android APP 吧！

```bash
# 立即建置
雙擊執行：🎯立即建置.bat
```

祝你使用愉快！🚀
