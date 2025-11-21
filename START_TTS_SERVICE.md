# 🎤 GPT-SoVITS TTS 服務啟動指南

## 方法一：自動啟動（推薦）

如果 GPT-SoVITS 已安裝在正確位置，執行：

```batch
bStart.bat
```

系統會自動啟動 Flask 和 GPT-SoVITS。

---

## 方法二：手動啟動 GPT-SoVITS

### 步驟 1：進入 GPT-SoVITS 目錄

```batch
cd ..\GPT-SoVITS
```

### 步驟 2：激活 conda 環境

```batch
conda activate GPTSoVits
```

### 步驟 3：啟動 API 服務

```batch
python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS\configs\tts_infer.yaml
```

### 步驟 4：驗證服務

在瀏覽器訪問：http://localhost:9880

應該會看到 API 文檔或狀態頁面。

### 步驟 5：啟動 Flask

回到專案目錄並啟動 Flask：

```batch
cd ..\Flask-AICares
.\venv\Scripts\python.exe app.py
```

---

## 方法三：僅啟動 Flask（純文字模式）

如果暫時不需要語音功能：

```batch
.\venv\Scripts\python.exe app.py
```

系統會以純文字模式運行，所有功能正常，只是沒有語音播放。

---

## 🔧 故障排除

### 問題 1：找不到 GPT-SoVITS

**錯誤訊息：**

```
⚠️ 未找到 GPT-SoVITS，將以純文字模式運行
```

**解決方案：**

1. 確認 GPT-SoVITS 安裝位置：

   ```
   Flask-AICares/    ← 當前專案
   GPT-SoVITS/       ← 應該在這裡
   ```

2. 如果位置不同，修改 `bStart.bat` 中的路徑

---

### 問題 2：conda 環境不存在

**錯誤訊息：**

```
EnvironmentNameNotFound: Could not find conda environment: GPTSoVits
```

**解決方案：**

1. 創建 conda 環境：

   ```batch
   conda create -n GPTSoVits python=3.10
   ```

2. 安裝依賴：
   ```batch
   conda activate GPTSoVits
   cd GPT-SoVITS
   pip install -r requirements.txt
   ```

---

### 問題 3：端口被占用

**錯誤訊息：**

```
OSError: [WinError 10048] 通常每個通訊端位址只允許使用一次
```

**解決方案：**

1. 查找占用端口的進程：

   ```batch
   netstat -ano | findstr :9880
   ```

2. 終止進程：
   ```batch
   taskkill /F /PID [進程ID]
   ```

---

### 問題 4：TTS API 返回 500 錯誤

**錯誤訊息：**

```
POST http://localhost:5000/api/generate-tts 500 (INTERNAL SERVER ERROR)
```

**可能原因：**

- GPT-SoVITS 服務未啟動
- 參考音頻文件不存在
- API 配置錯誤

**解決方案：**

1. 確認 GPT-SoVITS 正在運行：

   ```
   訪問 http://localhost:9880
   ```

2. 檢查 Flask 控制台的詳細錯誤訊息

3. 確認 `mockvoice/vc.wav` 文件存在

---

## 📁 目錄結構

正確的目錄結構應該是：

```
專案根目錄/
├── Flask-AICares/          ← 當前專案
│   ├── bStart.bat
│   ├── app.py
│   ├── venv/
│   ├── mockvoice/
│   │   └── vc.wav         ← 參考音頻
│   └── ...
│
└── GPT-SoVITS/             ← TTS 服務
    ├── api_v2.py
    ├── GPT_SoVITS/
    │   └── configs/
    │       └── tts_infer.yaml
    └── ...
```

---

## 🎯 快速測試

### 測試 1：檢查 GPT-SoVITS 服務

```batch
curl http://localhost:9880
```

或在瀏覽器訪問：http://localhost:9880

### 測試 2：測試 TTS API

```batch
curl -X POST http://localhost:5000/api/generate-tts ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"測試語音\"}"
```

### 測試 3：檢查參考音頻

```batch
dir mockvoice\vc.wav
```

---

## 💡 建議

1. **首次使用**：建議先手動啟動 GPT-SoVITS，確認可以正常運行
2. **開發階段**：可以只啟動 Flask，使用純文字模式
3. **生產環境**：使用 `bStart.bat` 自動啟動所有服務

---

## 📞 需要幫助？

如果遇到問題，請提供：

1. Flask 控制台的錯誤訊息
2. GPT-SoVITS 窗口的輸出（如果有）
3. 瀏覽器控制台的錯誤訊息
