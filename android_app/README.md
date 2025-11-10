# 📱 碳排放追蹤系統 - Android App

## 專案說明

這是碳排放追蹤系統的 Android App 版本，使用 WebView 技術包裝 PWA。

## 專案結構

```
android_app/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/carbontracking/app/
│   │       │   └── MainActivity.kt
│   │       ├── res/
│   │       │   ├── layout/
│   │       │   │   └── activity_main.xml
│   │       │   ├── values/
│   │       │   │   ├── strings.xml
│   │       │   │   ├── colors.xml
│   │       │   │   └── themes.xml
│   │       │   └── mipmap-*/
│   │       │       └── ic_launcher.png
│   │       └── AndroidManifest.xml
│   └── build.gradle
├── gradle/
├── build.gradle
├── settings.gradle
└── README.md
```

## 開發環境需求

- Android Studio Arctic Fox 或更新版本
- JDK 11 或更新版本
- Android SDK API 24+ (Android 7.0+)
- Kotlin 1.5+

## 快速開始

### 1. 安裝 Android Studio

```
下載：https://developer.android.com/studio
安裝並設定 Android SDK
```

### 2. 開啟專案

```
1. 啟動 Android Studio
2. File > Open
3. 選擇 android_app 資料夾
4. 等待 Gradle 同步完成
```

### 3. 設定後端網址

```kotlin
// 編輯 MainActivity.kt
private val SERVER_URL = "http://10.0.2.2:5000/carbon/"  // 模擬器
// 或
private val SERVER_URL = "http://your-ip:5000/carbon/"   // 實體手機
```

### 4. 執行 App

```
1. 連接 Android 裝置或啟動模擬器
2. 點擊 Run (綠色播放按鈕)
3. 選擇目標裝置
4. 等待安裝完成
```

## 功能特色

- ✅ WebView 包裝 PWA
- ✅ 支援 JavaScript
- ✅ 本地儲存
- ✅ 返回鍵支援
- ✅ 全螢幕顯示
- ✅ 自訂啟動畫面
- ✅ 離線快取

## 版本資訊

- Version: 1.0.0
- Min SDK: 24 (Android 7.0)
- Target SDK: 34 (Android 14)
- Package: com.carbontracking.app

## 建置 APK

### Debug 版本

```bash
./gradlew assembleDebug
# 輸出：app/build/outputs/apk/debug/app-debug.apk
```

### Release 版本

```bash
# 1. 建立簽署金鑰
keytool -genkey -v -keystore carbon-tracking.keystore -alias carbon -keyalg RSA -keysize 2048 -validity 10000

# 2. 建置 Release APK
./gradlew assembleRelease

# 3. 簽署 APK
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore carbon-tracking.keystore app/build/outputs/apk/release/app-release-unsigned.apk carbon

# 4. 對齊 APK
zipalign -v 4 app/build/outputs/apk/release/app-release-unsigned.apk app/build/outputs/apk/release/app-release.apk
```

## 測試

### 模擬器測試

```
1. 啟動 Flask 後端：python app.py
2. 使用網址：http://10.0.2.2:5000/carbon/
3. 在模擬器中測試所有功能
```

### 實體手機測試

```
1. 確保手機和電腦在同一網路
2. 查詢電腦 IP：ipconfig (Windows) 或 ifconfig (Mac/Linux)
3. 使用網址：http://your-ip:5000/carbon/
4. 在手機中測試所有功能
```

## 常見問題

### Q: 無法連接後端？

A:

- 模擬器使用 10.0.2.2 代替 localhost
- 實體手機使用電腦的 IP 位址
- 確認防火牆允許連線

### Q: 白屏或載入失敗？

A:

- 檢查後端是否運行
- 檢查網址是否正確
- 查看 Logcat 錯誤訊息

### Q: JavaScript 不執行？

A:

- 確認 WebSettings 已啟用 JavaScript
- 檢查 Console 錯誤

## 下一步

1. 測試所有功能
2. 部署後端到 HTTPS
3. 轉換為 TWA（Trusted Web Activity）
4. 上架 Google Play

## 技術支援

如有問題，請參考：

- `build_android_app.md` - 完整建置指南
- Android 官方文件：https://developer.android.com/
