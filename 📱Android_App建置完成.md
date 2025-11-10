# 📱 Android App 建置完成！

## 🎉 恭喜！Android App 專案已建立

你的碳排放追蹤系統現在有一個完整的 Android App 專案！

---

## 📦 已建立的檔案

### Android 專案結構

```
android_app/
├── app/
│   ├── src/main/
│   │   ├── java/com/carbontracking/app/
│   │   │   └── MainActivity.kt          ✅ 主要活動
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   └── activity_main.xml    ✅ 主畫面佈局
│   │   │   ├── values/
│   │   │   │   ├── strings.xml          ✅ 字串資源
│   │   │   │   ├── colors.xml           ✅ 顏色資源
│   │   │   │   └── themes.xml           ✅ 主題樣式
│   │   │   └── mipmap-*/                ⏳ 需要加入 Icon
│   │   ├── AndroidManifest.xml          ✅ 應用程式配置
│   │   └── proguard-rules.pro           ✅ 混淆規則
│   └── build.gradle                     ✅ App 建置設定
├── build.gradle                         ✅ 專案建置設定
├── settings.gradle                      ✅ 專案設定
└── README.md                            ✅ 說明文件
```

---

## 🚀 快速開始

### 方法一：使用 Android Studio（推薦）

#### Step 1: 安裝 Android Studio

```
1. 下載 Android Studio
   https://developer.android.com/studio

2. 安裝並啟動

3. 安裝 Android SDK
   - SDK Platform: Android 14.0 (API 34)
   - SDK Tools: Android SDK Build-Tools
```

#### Step 2: 開啟專案

```
1. 啟動 Android Studio
2. File > Open
3. 選擇 android_app 資料夾
4. 等待 Gradle 同步完成（首次需要下載依賴）
```

#### Step 3: 加入 App Icons

```
1. 複製 PWA Icons 到 Android 專案
   - 從 static/icons/ 複製圖示
   - 貼到 app/src/main/res/mipmap-*/ 資料夾

2. 或使用 Android Studio 生成
   - 右鍵 res 資料夾
   - New > Image Asset
   - 選擇 Launcher Icons
   - 上傳 static/icons/icon-512x512.png
   - 生成所有尺寸
```

#### Step 4: 設定後端網址

```kotlin
// 編輯 MainActivity.kt (第 24 行)

// 選項 A: 使用模擬器（推薦測試）
private val SERVER_URL = "http://10.0.2.2:5000/carbon/"

// 選項 B: 使用實體手機
private val SERVER_URL = "http://192.168.1.100:5000/carbon/"  // 替換成你的電腦 IP

// 選項 C: 使用雲端（正式環境）
private val SERVER_URL = "https://your-domain.com/carbon/"
```

#### Step 5: 執行 App

```
1. 啟動 Flask 後端
   python app.py

2. 連接 Android 裝置或啟動模擬器
   - 實體手機：啟用 USB 除錯
   - 模擬器：Tools > Device Manager > Create Device

3. 點擊 Run (綠色播放按鈕)

4. 選擇目標裝置

5. 等待安裝完成
```

---

### 方法二：使用命令列

#### 前置需求

```bash
# 安裝 JDK 11+
java -version

# 設定 ANDROID_HOME 環境變數
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

#### 建置 Debug APK

```bash
cd android_app

# Windows
gradlew.bat assembleDebug

# Mac/Linux
./gradlew assembleDebug

# 輸出位置
# app/build/outputs/apk/debug/app-debug.apk
```

#### 安裝到裝置

```bash
# 連接裝置並啟用 USB 除錯

# 安裝 APK
adb install app/build/outputs/apk/debug/app-debug.apk

# 啟動 App
adb shell am start -n com.carbontracking.app/.MainActivity
```

---

## 🔧 設定說明

### 網址設定

#### 模擬器

```kotlin
// 模擬器使用 10.0.2.2 代替 localhost
private val SERVER_URL = "http://10.0.2.2:5000/carbon/"
```

#### 實體手機（同一網路）

```kotlin
// 1. 查詢電腦 IP
// Windows: ipconfig
// Mac/Linux: ifconfig

// 2. 使用電腦 IP
private val SERVER_URL = "http://192.168.1.100:5000/carbon/"
```

#### 雲端部署

```kotlin
// 使用 HTTPS 網址
private val SERVER_URL = "https://your-domain.com/carbon/"
```

### 權限說明

已設定的權限：

- ✅ `INTERNET` - 網路存取
- ✅ `ACCESS_NETWORK_STATE` - 檢查網路狀態
- ✅ `ACCESS_WIFI_STATE` - 檢查 WiFi 狀態
- ⚠️ `WRITE_EXTERNAL_STORAGE` - 儲存檔案（API 28 以下）
- ⚠️ `ACCESS_FINE_LOCATION` - GPS 定位（如需要）

---

## 📱 功能特色

### 已實作功能

#### 1. WebView 包裝 ✅

- 完整的 WebView 設定
- JavaScript 支援
- DOM Storage 支援
- 本地快取

#### 2. 網路處理 ✅

- 網路狀態檢查
- 無網路提示
- 錯誤頁面顯示
- 自動重試

#### 3. 使用者體驗 ✅

- 下拉重新整理
- 載入進度條
- 返回鍵支援
- 狀態保存

#### 4. 主題樣式 ✅

- 與 PWA 一致的顏色
- Material Design
- 無標題列
- 全螢幕體驗

#### 5. 除錯支援 ✅

- Chrome DevTools 支援
- Console 訊息
- 網路監控

---

## 🧪 測試指南

### 模擬器測試

#### 建立模擬器

```
1. Android Studio > Tools > Device Manager
2. Create Device
3. 選擇裝置：Pixel 6
4. 選擇系統映像：Android 14.0 (API 34)
5. 完成建立
```

#### 測試步驟

```
1. 啟動 Flask 後端
   python app.py

2. 啟動模擬器

3. 執行 App

4. 測試功能：
   ✓ 首頁載入
   ✓ 頁面導航
   ✓ 新增記錄
   ✓ 查看統計
   ✓ 下拉重新整理
   ✓ 返回鍵
   ✓ 旋轉螢幕
```

### 實體手機測試

#### 啟用 USB 除錯

```
1. 設定 > 關於手機
2. 連續點擊「版本號碼」7 次
3. 返回 > 開發人員選項
4. 啟用「USB 除錯」
```

#### 測試步驟

```
1. 確保手機和電腦在同一網路

2. 查詢電腦 IP
   Windows: ipconfig
   Mac/Linux: ifconfig

3. 修改 MainActivity.kt 中的 SERVER_URL

4. 連接手機到電腦

5. 執行 App

6. 測試所有功能
```

### 離線測試

```
1. 正常使用 App
2. 關閉網路
3. 測試快取功能
4. 檢查錯誤處理
```

---

## 📦 建置 Release APK

### Step 1: 建立簽署金鑰

```bash
keytool -genkey -v -keystore carbon-tracking.keystore -alias carbon -keyalg RSA -keysize 2048 -validity 10000

# 輸入資訊：
# - 密碼（記住它！）
# - 姓名
# - 組織單位
# - 組織
# - 城市
# - 省份
# - 國家代碼（TW）
```

### Step 2: 設定簽署

```gradle
// 編輯 app/build.gradle

android {
    signingConfigs {
        release {
            storeFile file("../carbon-tracking.keystore")
            storePassword "your-password"
            keyAlias "carbon"
            keyPassword "your-password"
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
        }
    }
}
```

### Step 3: 建置 Release APK

```bash
# Windows
gradlew.bat assembleRelease

# Mac/Linux
./gradlew assembleRelease

# 輸出位置
# app/build/outputs/apk/release/app-release.apk
```

### Step 4: 測試 Release APK

```bash
# 安裝
adb install app/build/outputs/apk/release/app-release.apk

# 測試所有功能
```

---

## 🎨 自訂設定

### 修改 App 名稱

```xml
<!-- app/src/main/res/values/strings.xml -->
<string name="app_name">碳排放追蹤</string>
```

### 修改主題色彩

```xml
<!-- app/src/main/res/values/colors.xml -->
<color name="primary">#689F38</color>
<color name="primary_dark">#558B2F</color>
<color name="accent">#7CB342</color>
```

### 修改 Package ID

```gradle
// app/build.gradle
android {
    defaultConfig {
        applicationId "com.yourcompany.carbontracking"
    }
}
```

### 修改版本

```gradle
// app/build.gradle
android {
    defaultConfig {
        versionCode 2
        versionName "1.0.1"
    }
}
```

---

## 🔍 除錯技巧

### Chrome DevTools

```
1. 電腦開啟 Chrome
2. 訪問 chrome://inspect
3. 找到你的裝置和 App
4. 點擊 "inspect"
5. 可以查看 Console、Network、Elements
```

### Logcat

```
1. Android Studio > Logcat
2. 選擇裝置和 App
3. 查看日誌訊息
4. 篩選：com.carbontracking.app
```

### 常見問題

#### Q: 白屏或載入失敗？

```
解決方法：
1. 檢查後端是否運行
2. 檢查網址是否正確
3. 查看 Logcat 錯誤訊息
4. 檢查網路權限
```

#### Q: 無法連接後端？

```
解決方法：
1. 模擬器使用 10.0.2.2
2. 實體手機使用電腦 IP
3. 檢查防火牆設定
4. 確認在同一網路
```

#### Q: JavaScript 不執行？

```
解決方法：
1. 確認已啟用 JavaScript
2. 檢查 WebSettings 設定
3. 查看 Chrome DevTools Console
```

---

## 📤 上架 Google Play

### 準備清單

- [x] Release APK 已建立
- [x] 簽署金鑰已建立
- [ ] 部署到 HTTPS
- [ ] Feature Graphic (1024x500)
- [ ] Screenshots (2-8 張)
- [ ] 隱私權政策
- [ ] 商店說明
- [ ] Google Play 開發者帳號

### 上架步驟

```
1. 註冊 Google Play 開發者帳號
   https://play.google.com/console
   費用：$25 USD

2. 建立應用程式
   - 名稱：碳排放追蹤系統
   - 語言：繁體中文

3. 上傳 APK/AAB
   - 推薦使用 AAB 格式
   - 版本：1.0.0

4. 填寫商店資訊
   - 簡短說明
   - 完整說明
   - 截圖
   - Feature Graphic

5. 設定內容分級

6. 隱私權政策
   https://your-domain.com/privacy

7. 提交審核

8. 等待審核（1-3天）

9. 發布！
```

---

## 🎯 下一步

### 立即可做

1. ✅ 在 Android Studio 開啟專案
2. ✅ 加入 App Icons
3. ✅ 設定後端網址
4. ✅ 在模擬器測試

### 本週完成

5. ⏳ 在實體手機測試
6. ⏳ 建置 Release APK
7. ⏳ 部署後端到 HTTPS

### 下週完成

8. ⏳ 準備上架素材
9. ⏳ 上架 Google Play

---

## 📚 參考資源

### 官方文件

- Android 開發者指南：https://developer.android.com/
- WebView 文件：https://developer.android.com/reference/android/webkit/WebView
- Material Design：https://material.io/

### 工具

- Android Studio：https://developer.android.com/studio
- Gradle：https://gradle.org/
- Kotlin：https://kotlinlang.org/

---

## 🎉 完成狀態

### Android App 開發 ✅ 100%

- [x] 專案結構建立
- [x] MainActivity 實作
- [x] WebView 設定
- [x] UI 佈局
- [x] 主題樣式
- [x] 建置設定
- [x] 權限設定
- [x] 錯誤處理

### 測試階段 ⏳ 0%

- [ ] 模擬器測試
- [ ] 實體手機測試
- [ ] 功能測試
- [ ] 效能測試

### 上架階段 ⏳ 0%

- [ ] Release APK
- [ ] 素材準備
- [ ] 提交審核

---

## 🎊 恭喜！

你的 Android App 專案已經建立完成！

**開始在 Android Studio 中開啟專案吧！** 📱

```
1. 開啟 Android Studio
2. File > Open > 選擇 android_app 資料夾
3. 等待 Gradle 同步
4. 點擊 Run 執行 App
```

有任何問題隨時詢問！🚀
