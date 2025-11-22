# 即時語音互動系統 - URL 訪問指南

## 📍 正確的訪問地址

### 主頁面（選擇語言）

```
http://localhost:5000/voice_interaction_realtime/
```

或

```
http://localhost:5000/voice_interaction_realtime
```

（會自動重定向到帶斜線的版本）

**功能**：

- 顯示語言選擇頁面
- 可以選擇閩南語版或國語版
- 查看系統特色介紹

---

### 閩南語版本（Roy）

```
http://localhost:5000/voice_interaction_realtime/roy
```

**特色**：

- 🟠 橙色主題
- 🎤 Roy 語音角色（閩南語）
- 適合閩南語使用者

---

### 國語版本（Nofish）

```
http://localhost:5000/voice_interaction_realtime/nofish
```

**特色**：

- 🔵 藍色主題
- 🎤 Nofish 語音角色（國語）
- 適合國語使用者

---

## 🚀 快速訪問

### 方法 1：從主頁選擇（推薦）

1. 訪問 http://localhost:5000/voice_interaction_realtime/
2. 點擊「閩南語版」或「國語版」卡片
3. 開始使用

### 方法 2：直接訪問

直接訪問對應的語言版本 URL：

- 閩南語：http://localhost:5000/voice_interaction_realtime/roy
- 國語：http://localhost:5000/voice_interaction_realtime/nofish

---

## 📋 完整路由列表

| 路由                                        | 說明               | 狀態 |
| ------------------------------------------- | ------------------ | ---- |
| `/voice_interaction_realtime/`              | 主頁面（語言選擇） | ✅   |
| `/voice_interaction_realtime/roy`           | 閩南語版本         | ✅   |
| `/voice_interaction_realtime/nofish`        | 國語版本           | ✅   |
| `/voice_interaction_realtime/session/start` | 啟動會話 API       | ✅   |
| `/voice_interaction_realtime/session/stop`  | 結束會話 API       | ✅   |

---

## 🔧 故障排除

### 問題：訪問 404

**可能原因**：

1. 服務器未啟動
2. URL 拼寫錯誤
3. 路由未正確註冊

**解決方案**：

1. 確認服務器正在運行：

   ```cmd
   # 查看是否有 "即時語音互動" 模組載入的訊息
   ```

2. 檢查 URL 是否正確：

   - ✅ 正確：`http://localhost:5000/voice_interaction_realtime/`
   - ❌ 錯誤：`http://localhost:5000/voice_interaction_realtime`（無斜線可能重定向）

3. 重啟服務器：
   ```cmd
   # 停止服務器（Ctrl+C）
   # 重新啟動
   python app.py
   ```

### 問題：頁面空白

**解決方案**：

1. 檢查瀏覽器控制台（F12）
2. 確認模板文件存在
3. 查看服務器日誌

---

## 🌐 從其他設備訪問

如果要從同一網路的其他設備訪問：

1. 查看服務器 IP（服務器啟動時會顯示）：

   ```
   * Running on http://192.168.1.101:5000
   ```

2. 在其他設備上訪問：
   ```
   http://192.168.1.101:5000/voice_interaction_realtime/
   ```

---

## 📱 系統入口

如果從系統入口頁面訪問：

```
http://localhost:5000/portal
```

在入口頁面中應該會有「即時語音互動」的連結。

---

## ✅ 測試連接

使用以下命令測試連接：

```powershell
# 測試主頁
curl http://localhost:5000/voice_interaction_realtime/ -UseBasicParsing

# 測試閩南語版
curl http://localhost:5000/voice_interaction_realtime/roy -UseBasicParsing

# 測試國語版
curl http://localhost:5000/voice_interaction_realtime/nofish -UseBasicParsing
```

所有測試應該返回 `StatusCode: 200`

---

**記住**：訪問主頁時 URL 末尾要加斜線 `/`，或者讓瀏覽器自動重定向！
