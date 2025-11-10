# 🚀 最簡單 3 步驟建置 APK

## 📱 超級簡單版本

### Step 1: 開始建置（1 分鐘）

**在 Android Studio 中：**

1. 點擊頂部選單 **"Build"**
2. 選擇 **"Generate Signed Bundle / APK"**
3. 選擇 **"APK"**（不是 Bundle）
4. 點擊 **"Next"**

### Step 2: 建立金鑰（3 分鐘，第一次需要）

#### 🆕 如果是第一次建置：

**點擊 "Create new..."**

**填寫以下資訊：**

```
Key store path（金鑰位置）：
D:\python\Flask-AICares\android_app\carbon-tracking.keystore

Password（密碼）：
carbon123
（或你自己設定的密碼，記住它！）

Confirm（確認密碼）：
carbon123
（再輸入一次）

---

Alias（別名）：
carbon

Password（金鑰密碼）：
carbon123
（可以跟上面一樣）

Confirm（確認）：
carbon123

Validity (years)（有效期）：
25

---

Certificate（證書資訊）：

First and Last Name（姓名）：
[你的名字]

Organizational Unit（部門）：
IT

Organization（組織）：
Carbon Tracking

City or Locality（城市）：
台灣

State or Province（省份）：
Taiwan

Country Code (XX)（國家代碼）：
TW
```

**點擊 "OK"**

**點擊 "Next"**

#### ✅ 如果已經有金鑰：

```
1. 點擊 "Choose existing..."
2. 選擇：carbon-tracking.keystore
3. 輸入密碼
4. 選擇 Alias: carbon
5. 輸入金鑰密碼
6. 點擊 "Next"
```

### Step 3: 完成建置（2-5 分鐘）

```
1. 選擇 "release"
2. 勾選 ☑ "V1 (Jar Signature)"
3. 勾選 ☑ "V2 (Full APK Signature)"
4. 點擊 "Finish"
5. 等待建置完成（底部會顯示進度）
```

## 🎉 完成！

建置完成後，Android Studio 會顯示通知。

### 📦 APK 在哪裡？

```
位置：
D:\python\Flask-AICares\android_app\app\release\app-release.apk
```

或點擊通知中的 **"locate"** 連結。

## 📱 安裝到手機

### 方法 A：使用 ADB（如果手機已連接）

```bash
cd D:\python\Flask-AICares\android_app
adb install app\release\app-release.apk
```

### 方法 B：直接傳輸（最簡單）

```
1. 把 app-release.apk 複製到手機
   （可以用 USB、藍牙、雲端等）

2. 在手機上找到 APK 檔案

3. 點擊安裝

4. 如果提示「不允許安裝未知來源」：
   - 點擊「設定」
   - 允許安裝
   - 返回繼續安裝

5. 完成！
```

## ⚠️ 超重要提醒

### 1. 備份金鑰檔案！

```
檔案名稱：carbon-tracking.keystore
位置：D:\python\Flask-AICares\android_app\

⚠️ 這個檔案非常重要！
- 遺失後無法更新 App
- 需要重新上架新的 App
- 建議立即備份到：
  ✓ 雲端硬碟（Google Drive、OneDrive）
  ✓ USB 隨身碟
  ✓ 另一台電腦
```

### 2. 記住密碼！

```
你設定的密碼：carbon123（或你自己設定的）

⚠️ 密碼忘記無法找回！
建議寫在：
✓ 密碼管理器
✓ 安全的筆記本
✓ 加密的文件
```

## 🧪 測試 APK

安裝後測試：

```
✓ App 成功啟動
✓ 顯示綠色 Splash Screen
✓ 首頁載入成功
✓ 新增訪視記錄
✓ 查看統計資料
✓ 匯出 Excel
✓ 所有功能正常
```

## 🔧 如果建置失敗

### 方法 1：Clean 後重試

```
1. Build > Clean Project
2. 等待完成
3. 重新執行 Step 1-3
```

### 方法 2：重啟 Android Studio

```
1. File > Invalidate Caches / Restart
2. 選擇 "Invalidate and Restart"
3. 重新開啟專案
4. 重新執行 Step 1-3
```

### 方法 3：問我

```
如果還是失敗：
1. 截圖錯誤訊息
2. 告訴我發生什麼
3. 我會立即協助你
```

## ⏱️ 建置時間

```
Step 1: 開始建置        1 分鐘
Step 2: 建立金鑰        3 分鐘（第一次）
Step 3: 完成建置        2-5 分鐘
---
首次總計：             6-9 分鐘
後續建置：             3-6 分鐘
```

## 🎯 建置成功後

### 1. 測試 APK

```
在手機上完整測試所有功能
```

### 2. 準備上架（如果要上架）

```
- Feature Graphic (1024x500)
- Screenshots (2-8 張)
- App 描述
- 隱私權政策
```

### 3. 建置 AAB（上架 Google Play 需要）

```
重複 Step 1-3，但在 Step 1 選擇 "Android App Bundle"
```

## 💡 小技巧

### 快速找到 APK

```
在 Android Studio 左側：
1. 切換到 "Project" 視圖
2. 展開 app > release
3. 找到 app-release.apk
4. 右鍵 > Show in Explorer
```

### 快速安裝

```
如果手機已連接：
1. 在 Android Studio 底部點擊 "Terminal"
2. 輸入：adb install app\release\app-release.apk
3. 按 Enter
```

## 🎉 恭喜！

你已經成功建置 APK 了！

**下一步：**

1. ✅ 在手機測試
2. ✅ 分享給朋友測試
3. ✅ 準備上架 Google Play

**你做得很好！** 💪

---

## 📞 需要協助？

如果遇到任何問題：

- 建置失敗
- 找不到檔案
- 安裝問題
- 任何疑問

**隨時問我！** 🤝

---

**準備好了嗎？開始建置吧！** 🚀

只需要 3 個步驟，6-9 分鐘就完成了！
