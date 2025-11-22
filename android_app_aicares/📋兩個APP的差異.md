# 📋 兩個 Android APP 的差異說明

## 🎯 專案概覽

現在有兩個獨立的 Android APP 專案：

### 1️⃣ 碳排放追蹤 APP

**目錄：** `android_app/`

### 2️⃣ AI 客服系統 APP

**目錄：** `android_app_aicares/`

---

## 📊 功能對比

| 功能             | 碳排放追蹤 APP                               | AI 客服系統 APP            |
| ---------------- | -------------------------------------------- | -------------------------- |
| **主要用途**     | 社工訪視碳排放記錄                           | 完整 AI 客服功能           |
| **套件名稱**     | com.carbontracking.app                       | com.aicares.app            |
| **應用程式名稱** | 碳排放追蹤系統                               | AI 客服系統                |
| **主題色**       | 綠色系 (#8BC34A)                             | 紫色系 (#667eea)           |
| **伺服器地址**   | https://carbon-tracking.onrender.com/carbon/ | http://192.168.1.102:5000/ |

---

## 🌐 連接的後端功能

### 碳排放追蹤 APP 連接功能

```
http://server/carbon/
├── 首頁
├── 儀表板
├── 新增訪視記錄
├── 編輯訪視記錄
├── 訪視記錄列表
└── 統計報表
```

**包含模組：**

- ✅ 碳排放追蹤系統

---

### AI 客服系統 APP 連接功能

```
http://192.168.1.102:5000/
├── 主頁面 (/)
├── 碳排放追蹤 (/carbon/)
├── 員工管理 (/staff/)
├── 認證系統 (/auth/)
├── 語音克隆 (/voice-clone/)
├── TTS 文字轉語音 (/tts/)
├── 語音對話 (/voice-chat/)
├── 情緒識別 (/emotion/)
├── ASR 語音識別 (/asr/)
└── 音訊處理 (/audio/)
```

**包含模組：**

- ✅ JWT 認證系統
- ✅ 主頁面
- ✅ 員工管理
- ✅ 音訊處理
- ✅ 認證系統
- ✅ 語音克隆
- ✅ TTS（文字轉語音）
- ✅ 語音對話
- ✅ 情緒識別
- ✅ ASR 語音識別
- ✅ 碳排放追蹤

---

## 🔐 權限差異

### 碳排放追蹤 APP

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### AI 客服系統 APP

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

**額外權限說明：**

- `RECORD_AUDIO` - 語音輸入功能
- `MODIFY_AUDIO_SETTINGS` - 調整音訊設定
- `WRITE/READ_EXTERNAL_STORAGE` - 快取音訊檔案

---

## 🎨 視覺設計差異

### 碳排放追蹤 APP

- **主色調：** 綠色環保風格
- **Splash 背景：** 淺綠色漸層
- **圖示：** 綠色葉子主題

### AI 客服系統 APP

- **主色調：** 紫色科技風格
- **Splash 背景：** 紫色漸層 (#667eea → #764ba2)
- **圖示：** 現代科技感

---

## 📱 使用場景

### 碳排放追蹤 APP

**目標使用者：** 社工人員

**使用流程：**

1. 開啟 APP
2. 記錄訪視行程
3. 選擇交通工具
4. 自動計算碳排放
5. 查看統計報表

**適用情境：**

- 外出訪視時記錄
- 月底統計碳排放
- 生成報表給主管

---

### AI 客服系統 APP

**目標使用者：** 客服人員、系統管理員

**使用流程：**

1. 開啟 APP
2. 登入系統
3. 使用各種 AI 功能：
   - 語音對話
   - 情緒識別
   - 語音克隆
   - 員工管理
   - 碳排放追蹤

**適用情境：**

- 客服中心使用
- 語音互動服務
- 多功能整合平台

---

## 🚀 部署方式

### 碳排放追蹤 APP

- **後端：** 已部署到 Render.com
- **地址：** https://carbon-tracking.onrender.com
- **狀態：** ✅ 可直接使用

### AI 客服系統 APP

- **後端：** 本地開發伺服器
- **地址：** http://192.168.1.102:5000
- **狀態：** 🔧 開發中
- **注意：** 需要在同一 WiFi 網路

---

## 📦 建置方式

兩個 APP 的建置方式相同：

### 使用 Android Studio

1. 開啟對應的專案目錄
2. 等待 Gradle 同步
3. Build → Build APK

### 使用命令列

```bash
# 碳排放追蹤 APP
cd android_app
gradlew assembleDebug

# AI客服系統 APP
cd android_app_aicares
gradlew assembleDebug
```

---

## 🔄 可以同時安裝嗎？

**✅ 可以！**

因為兩個 APP 使用不同的套件名稱：

- `com.carbontracking.app`
- `com.aicares.app`

所以可以同時安裝在同一支手機上，互不衝突。

---

## 💡 選擇建議

### 只需要碳排放追蹤功能？

→ 使用 **碳排放追蹤 APP** (`android_app/`)

- 更輕量
- 功能專注
- 已部署雲端

### 需要完整的 AI 功能？

→ 使用 **AI 客服系統 APP** (`android_app_aicares/`)

- 功能完整
- 包含所有模組
- 適合開發測試

### 兩個都需要？

→ 兩個都安裝！

- 互不衝突
- 各司其職
- 靈活使用

---

## 📝 維護說明

### 碳排放追蹤 APP

- 專注於碳排放功能
- 保持簡潔穩定
- 適合長期使用

### AI 客服系統 APP

- 持續開發新功能
- 整合更多 AI 能力
- 適合實驗測試

---

## 🎯 總結

| 項目         | 碳排放追蹤 APP | AI 客服系統 APP |
| ------------ | -------------- | --------------- |
| **定位**     | 專業工具       | 整合平台        |
| **複雜度**   | 簡單           | 複雜            |
| **功能數**   | 1 個核心功能   | 10+ 個功能模組  |
| **部署狀態** | 已上線         | 開發中          |
| **推薦場景** | 日常使用       | 開發測試        |

兩個 APP 各有特色，根據需求選擇使用！ 🎉
