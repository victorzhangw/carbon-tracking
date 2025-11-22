# ASR 測試工具使用說明

## 📋 概述

ASR（Automatic Speech Recognition）測試工具是一個語音識別測試系統，支援雙引擎（Whisper + FunASR）語音識別，並針對閩南語和長者語音進行了優化。

## 🎯 功能特點

- ✅ **雙引擎識別**: 支援 Whisper 和 FunASR 雙引擎
- ✅ **多語言支援**: 中文（普通話）、中文（台灣）、閩南語
- ✅ **即時錄音**: 支援瀏覽器即時錄音測試
- ✅ **文件上傳**: 支援 WAV, MP3, M4A 等音頻格式
- ✅ **閩南語優化**: 針對閩南語進行特殊優化
- ✅ **長者語音優化**: 針對高齡語音特徵進行優化

## 🚀 快速開始

### 1. 檢查系統狀態

運行測試腳本檢查 ASR 模組是否正常：

```bash
python test_asr_module.py
```

### 2. 啟動應用

確保 Flask 應用正在運行：

```bash
python app.py
```

或使用啟動腳本：

```bash
bStart.bat
```

### 3. 訪問測試頁面

在瀏覽器中訪問：

```
http://localhost:5000/api/asr/test
```

或從語音測試訓練模組入口進入：

```
http://localhost:5000/voice-testing
```

點擊「ASR 測試工具」卡片即可進入。

## 📝 使用方式

### 方式一：上傳音頻文件

1. 點擊上傳區域或拖曳音頻文件
2. 選擇語言提示（中文/台灣/閩南語）
3. 勾選需要的選項：
   - 返回詳細信息
   - 閩南語優化
4. 點擊「開始識別」按鈕
5. 查看識別結果

### 方式二：即時錄音

1. 點擊「開始錄音」按鈕
2. 允許瀏覽器訪問麥克風
3. 說話（錄音中按鈕會變綠色並閃爍）
4. 點擊「停止錄音」
5. 錄音會自動上傳並識別

## 🔧 API 端點

### 測試端點（無需認證）

```
POST /api/asr/recognize-test
```

**參數:**

- `file`: 音頻文件（multipart/form-data）
- `language_hint`: 語言提示（zh/zh-TW/minnan）
- `return_details`: 是否返回詳細信息（true/false）
- `enable_minnan_optimization`: 是否啟用閩南語優化（true/false）

**響應:**

```json
{
  "success": true,
  "text": "識別的文本",
  "confidence": 0.85,
  "language": "zh",
  "audio_duration": 5.2,
  "processing_time": 1.5
}
```

### 正式端點（需要認證）

```
POST /api/asr/recognize
```

需要 JWT Token 認證，參數與測試端點相同。

## 📦 依賴套件

必要套件：

- `openai-whisper`: OpenAI Whisper 語音識別引擎
- `torch`: PyTorch 深度學習框架
- `librosa`: 音頻處理庫
- `soundfile`: 音頻文件讀寫
- `numpy`: 數值計算

可選套件：

- `funasr`: FunASR 語音識別引擎（阿里達摩院）

安裝命令：

```bash
pip install openai-whisper torch librosa soundfile numpy
```

## 🐛 故障排除

### 問題 1: 404 錯誤

**原因**: ASR 路由未正確註冊

**解決方案**:

1. 檢查 `app.py` 中是否有 ASR 模組的導入
2. 確認 `routes/asr.py` 文件存在
3. 重啟 Flask 應用

### 問題 2: 模組導入失敗

**原因**: 缺少依賴套件

**解決方案**:

```bash
python test_asr_module.py  # 檢查缺少哪些套件
pip install [缺少的套件名稱]
```

### 問題 3: 識別速度慢

**原因**: 使用 CPU 運算或模型過大

**解決方案**:

1. 如果有 NVIDIA GPU，安裝 CUDA 版本的 PyTorch
2. 在 `routes/asr.py` 中調整模型大小（tiny/base/small）
3. 確保音頻文件不要太大（建議 < 10MB）

### 問題 4: 麥克風無法訪問

**原因**: 瀏覽器權限或 HTTPS 問題

**解決方案**:

1. 確保瀏覽器允許麥克風訪問
2. 在 Chrome 中，localhost 可以使用麥克風
3. 如果是遠程訪問，需要使用 HTTPS

## 📊 識別結果說明

- **識別文本**: 語音轉換的文字內容
- **信心度**: 識別結果的可信度（0-100%）
- **語言**: 檢測到的語言類型
- **音頻時長**: 音頻文件的長度（秒）
- **處理時間**: 識別所花費的時間（秒）

## 🔗 相關文件

- `routes/asr.py`: ASR 路由定義
- `services/asr/coordinator.py`: ASR 協調器
- `services/asr/whisper_engine.py`: Whisper 引擎
- `services/asr/funasr_engine.py`: FunASR 引擎
- `templates/asr_test.html`: 測試頁面

## 💡 提示

1. 首次使用時，Whisper 會自動下載模型（約 150MB），請耐心等待
2. 建議使用清晰的音頻文件，避免背景噪音
3. 閩南語識別需要啟用「閩南語優化」選項
4. 對於長音頻（>1 分鐘），處理時間會較長

## 📞 技術支援

如有問題，請查看：

1. 運行 `test_asr_module.py` 檢查系統狀態
2. 查看 Flask 應用的控制台輸出
3. 檢查瀏覽器的開發者工具（F12）中的錯誤信息
