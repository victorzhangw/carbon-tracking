# 📱 超簡單 APK 建置指南

## 🎯 5 步驟建置 APK

### Step 1: Clean Project（30 秒）

**在 Android Studio 中：**

```
1. 點擊頂部選單 "Build"
2. 選擇 "Clean Project"
3. 等待完成（底部狀態列會顯示 "BUILD SUCCESSFUL"）
```

### Step 2: Rebuild Project（1-2 分鐘）

```
1. 點擊頂部選單 "Build"
2. 選擇 "Rebuild Project"
3. 等待完成
4. 確認沒有紅色錯誤訊息
```

### Step 3: 開始建置 APK（點擊這裡）

```
1. 點擊頂部選單 "Build"
2. 選擇 "Generate Signed Bundle / APK"
3. 選擇 "APK"（不是 Bundle）
4. 點擊 "Next"
```

### Step 4: 建立簽署金鑰（第一次需要）

#### 如果是第一次建置：

```
1. 點擊 "Create new..."

2. 填寫以下資訊：

   Key store path（金鑰檔案位置）：
   D:\python\Flask-AICares\android_app\carbon-tracking.keystore

   Password（密碼）：
   [設定一個密碼，例如：carbon123]

   Confirm（確認密碼）：
   [再輸入一次相同密碼]

   Alias（別名）：
   carbon

   Password（金鑰密碼）：
   [設定密碼，可以跟上面一樣]

   Confirm（確認）：
   [再輸入一次]

   Validity (years)（有效期）：
   25

3. Certificate（證書資訊）：

   First and Last Name（姓名）：
   [你的名字]

   Organizational Unit（部門）：
   [你的部門，例如：IT]

   Organization（組織）：
   [你的組織，例如：Carbon Tracking]

   City or Locality（城市）：
   台灣

   State or Province（省份）：
   Taiwan

   Country Code (XX)（國家代碼）：
   TW

4. 點擊 "OK"

5. 點擊 "Next"
```

#### 如果已經有金鑰：

```
1. 點擊 "Choose existing..."
2. 選擇：D:\python\Flask-AICares\android_app\carbon-tracking.keystore
3. 輸入密碼
4. 選擇 Alias: carbon
5. 輸入金鑰密碼
6. 點擊 "Next"
```

### Step 5: 完成建置（2-5 分鐘）

```
1. 選擇 "release"
2. 勾選 "V1 (Jar Signature)"
3. 勾選 "V2 (Full APK Signature)"
4. 點擊 "Finish"
5. 等待建置完成
```

## 📦 找到你的 APK

建置完成後，Android Studio 會顯示通知。

**APK 位置：**

```
D:\python\Flask-AICares\android_app\app\release\app-release.apk
```

或者點擊通知中的 "locate" 連結直接開啟資料夾。

## 📱 安裝到手機測試

### 方法 A：使用 ADB（如果手機已連接）

```bash
# 在命令列執行
cd D:\python\Flask-AICares\android_app
adb install app\release\app-release.apk
```

### 方法 B：直接傳輸

```
1. 把 app-release.apk 複製到手機
2. 在手機上點擊 APK 檔案
3. 允許安裝未知來源（如果需要）
4. 點擊安裝
5. 完成！
```

## ⚠️ 重要提醒

### 1. 備份金鑰檔案！

```
檔案：carbon-tracking.keystore
位置：D:\python\Flask-AICares\android_app\

⚠️ 非常重要！
- 這個檔案遺失後無法更新 App
- 建議複製到雲端硬碟備份
- 建議複製到 USB 隨身碟備份
```

### 2. 記住密碼！

```
需要記住：
- Keystore 密碼
- Key 密碼
- Alias 名稱（carbon）

建議寫在安全的地方，例如：
- 密碼管理器
- 筆記本（鎖起來）
- 加密的文件
```

### 3. 第一次建置較慢

```
首次建置可能需要：
- Clean: 30 秒
- Rebuild: 1-2 分鐘
- 建立金鑰: 2-3 分鐘
- 建置 APK: 2-5 分鐘
---
總計：5-10 分鐘

後續建置會更快（2-3 分鐘）
```

## 🧪 測試 APK

安裝後，測試以下功能：

### 基本功能

- [ ] App 成功啟動
- [ ] 顯示 Splash Screen（綠色畫面）
- [ ] 首頁載入成功
- [ ] 可以導航

### 核心功能

- [ ] 新增訪視記錄
- [ ] 查看記錄列表
- [ ] 查看統計資料
- [ ] 匯出 Excel
- [ ] 編輯記錄
- [ ] 刪除記錄
- [ ] 搜尋功能

### 互動功能

- [ ] 下拉重新整理
- [ ] 返回鍵正常
- [ ] 旋轉螢幕正常

## 🔧 常見問題

### Q: 建置失敗怎麼辦？

**A: 按照以下步驟：**

```
1. Build > Clean Project
2. File > Invalidate Caches / Restart
3. 選擇 "Invalidate and Restart"
4. 重新開啟專案
5. 再次嘗試建置
```

### Q: 找不到 APK 檔案？

**A: 檢查以下位置：**

```
D:\python\Flask-AICares\android_app\app\release\app-release.apk

或在 Android Studio 中：
1. 左側 Project 視圖
2. 切換到 "Project" 模式
3. 展開 app > release
4. 找到 app-release.apk
```

### Q: 手機無法安裝？

**A: 啟用未知來源：**

```
1. 設定 > 安全性
2. 允許安裝未知來源的應用程式
3. 或在安裝時點擊 "設定" 允許
```

### Q: 金鑰密碼忘記了？

**A: 無法找回，需要：**

```
1. 建立新的金鑰
2. 重新建置 APK
3. 如果已上架，需要上架新的 App
```

## 🎯 建置成功後

### 1. 測試 APK

```
在多台手機測試
確認所有功能正常
記錄任何問題
```

### 2. 準備上架素材

```
- Feature Graphic (1024x500)
- Screenshots (2-8 張)
- App 描述文案
- 隱私權政策
```

### 3. 建置 AAB（上架用）

```
1. Build > Generate Signed Bundle / APK
2. 選擇 "Android App Bundle"
3. 使用相同的 keystore
4. 建置 release
```

### 4. 上架 Google Play

```
1. 註冊開發者帳號（$25）
2. 建立應用程式
3. 上傳 AAB
4. 填寫資訊
5. 提交審核
```

## 📊 建置時間參考

```
Clean Project:        30 秒
Rebuild Project:      1-2 分鐘
建立金鑰:            2-3 分鐘（第一次）
建置 APK:            2-5 分鐘
---
首次總計:            5-10 分鐘
後續建置:            2-3 分鐘
```

## 🎉 完成！

建置成功後，你就有了一個可以安裝的 APK 檔案！

**下一步：**

1. 在手機測試
2. 準備上架素材
3. 上架 Google Play

**恭喜你完成 APK 建置！** 🎉

---

## 📞 需要協助？

如果遇到任何問題：

- 建置錯誤
- 找不到檔案
- 安裝問題
- 任何疑問

**隨時問我！** 🤝

---

**準備好了嗎？開始建置吧！** 🚀
