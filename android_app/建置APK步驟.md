# 📱 建置 APK 完整步驟

## ✅ 你已完成

- [x] 後端部署到 Render：https://carbon-tracking.onrender.com
- [x] MainActivity.kt 已更新為雲端網址

## 🎯 現在要做：建置 APK

### 方法 1：使用 Android Studio（推薦）

#### Step 1: 開啟專案

1. 啟動 Android Studio
2. File > Open
3. 選擇 `android_app` 資料夾
4. 等待 Gradle 同步完成

#### Step 2: 建立簽署金鑰

1. Build > Generate Signed Bundle / APK
2. 選擇 APK
3. 點擊 "Create new..."
4. 填寫資訊：

   ```
   Key store path: D:\python\Flask-AICares\android_app\carbon-tracking.keystore
   Password: 設定一個安全密碼（記住它！）
   Alias: carbon
   Validity: 25 years

   Certificate:
   First and Last Name: 你的名字
   Organizational Unit: 你的組織
   Organization: 你的組織名稱
   City: 台灣
   State: Taiwan
   Country Code: TW
   ```

5. 點擊 OK

#### Step 3: 建置 Release APK

1. 選擇剛建立的 keystore
2. 輸入密碼
3. 選擇 release
4. 勾選 V1 和 V2 簽名
5. 點擊 Finish
6. 等待建置完成（約 2-5 分鐘）

#### Step 4: 找到 APK

建置完成後，APK 位於：

```
android_app/app/release/app-release.apk
```

### 方法 2：使用命令列（需要先設定）

如果你已經有 Gradle Wrapper，可以使用：

```bash
cd android_app

# 建立簽署金鑰（只需一次）
keytool -genkey -v -keystore carbon-tracking.keystore -alias carbon -keyalg RSA -keysize 2048 -validity 10000

# 建置 Debug APK（測試用）
gradlew.bat assembleDebug

# 建置 Release APK（需要簽署設定）
gradlew.bat assembleRelease
```

## 📱 測試 APK

### 在模擬器測試

```bash
# 啟動模擬器後
adb install app/release/app-release.apk
```

### 在實體手機測試

1. 啟用 USB 除錯：

   - 設定 > 關於手機 > 連點版本號 7 次
   - 開發人員選項 > USB 除錯

2. 連接手機到電腦

3. 安裝 APK：

```bash
adb devices  # 確認手機已連接
adb install app/release/app-release.apk
```

4. 測試所有功能：
   - ✅ App 啟動
   - ✅ 載入首頁
   - ✅ 新增訪視記錄
   - ✅ 查看統計資料
   - ✅ 匯出 Excel
   - ✅ 編輯/刪除記錄

## 🚀 準備上架 Google Play

### 建置 AAB（Android App Bundle）

AAB 是 Google Play 要求的格式：

#### 使用 Android Studio：

1. Build > Generate Signed Bundle / APK
2. 選擇 **Android App Bundle**
3. 選擇你的 keystore
4. 選擇 release
5. 點擊 Finish

AAB 位於：

```
android_app/app/release/app-release.aab
```

#### 使用命令列：

```bash
cd android_app
gradlew.bat bundleRelease
```

## 📋 上架前檢查清單

- [ ] APK 建置成功
- [ ] 在實體手機測試所有功能
- [ ] 準備 App 圖示（已有）
- [ ] 準備 Feature Graphic (1024x500)
- [ ] 截取 Screenshots（至少 2 張）
- [ ] 準備 App 描述文案
- [ ] 隱私權政策網址：https://carbon-tracking.onrender.com/privacy
- [ ] 註冊 Google Play 開發者帳號（$25）

## 💡 重要提醒

### 備份簽署金鑰！

```
檔案：carbon-tracking.keystore
位置：android_app/carbon-tracking.keystore

⚠️ 這個檔案非常重要！
- 遺失後無法更新 App
- 需要重新上架新的 App
- 建議備份到多個地方
```

### 記住密碼！

- Keystore 密碼
- Key 密碼
- Alias 名稱

建議寫在安全的地方。

## 🆘 常見問題

### Q: 沒有 gradlew.bat？

A: 使用 Android Studio 開啟專案，它會自動生成。

### Q: 建置失敗？

A:

1. 檢查 JDK 版本（需要 JDK 11+）
2. 清理專案：Build > Clean Project
3. 重新建置：Build > Rebuild Project

### Q: 簽署失敗？

A: 確認密碼正確，檢查 keystore 檔案路徑。

### Q: APK 太大？

A:

- 使用 AAB 格式（Google Play 會自動優化）
- 啟用 ProGuard 混淆

## 🎯 下一步

建置完成後：

1. ✅ 測試 APK
2. 📸 準備上架素材
3. 🚀 上架 Google Play

需要協助嗎？隨時問我！
