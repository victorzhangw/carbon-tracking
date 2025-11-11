# AI 語音克隆系統部署指南

## 📋 系統要求

### 硬體要求

- **CPU**: Intel i5 或 AMD Ryzen 5 以上
- **記憶體**: 8GB RAM 以上 (推薦 16GB)
- **顯卡**: NVIDIA GTX 1060 以上 (可選，用於加速)
- **硬碟**: 至少 10GB 可用空間

### 軟體要求

- **作業系統**: Windows 10/11
- **Python**: 3.9 - 3.11
- **Git**: 用於下載代碼

## 🚀 安裝步驟

### 1. 準備 GPT-SoVITS v4

確保你已經有 `GPT-SoVITS-v4-20250422fix` 目錄，並且包含以下文件：

```
GPT-SoVITS-v4-20250422fix/
├── api_v2.py
├── webui.py
├── GPT_SoVITS/
│   ├── configs/
│   │   └── tts_infer.yaml
│   └── pretrained_models/
│       ├── s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt
│       ├── s2G488k.pth
│       └── s2D488k.pth
└── requirements.txt
```

### 2. 安裝 Python 依賴

```bash
# 安裝 GPT-SoVITS 依賴
cd GPT-SoVITS-v4-20250422fix
pip install -r requirements.txt

# 回到主目錄
cd ..

# 安裝語音克隆服務依賴
pip install flask flask-cors librosa soundfile numpy requests pathlib
```

### 3. 下載預訓練模型

如果 `GPT_SoVITS/pretrained_models/` 目錄為空，請下載以下模型：

1. 訪問 [GPT-SoVITS Models](https://huggingface.co/lj1995/GPT-SoVITS)
2. 下載以下文件到 `GPT-SoVITS-v4-20250422fix/GPT_SoVITS/pretrained_models/`:
   - `s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt`
   - `s2G488k.pth`
   - `s2D488k.pth`

### 4. 啟動服務

#### 方法 1: 使用批次檔 (推薦)

```bash
# 啟動語音克隆服務
start-voice-clone-service.bat
```

#### 方法 2: 手動啟動

```bash
# 1. 啟動 GPT-SoVITS API (新開一個終端)
cd GPT-SoVITS-v4-20250422fix
python api_v2.py -a 127.0.0.1 -p 9880

# 2. 啟動語音克隆服務 (新開另一個終端)
python voice_clone_service.py
```

### 5. 測試服務

```bash
# 運行測試腳本
python test-voice-clone.py
```

## 🎯 使用方法

### 1. 訪問前端界面

- 啟動你的 AI 客服系統前端
- 登入後點擊「語音克隆」選單

### 2. 語音克隆流程

#### 步驟 1: 上傳參考語音

- 點擊上傳區域或拖拽音頻文件
- 支持格式: WAV, MP3, FLAC, M4A
- 建議時長: 5-30 秒
- 建議質量: 清晰、無雜音

#### 步驟 2: 查看分析結果

- 系統會自動分析音頻質量
- 顯示時長、採樣率、質量評分等信息
- 根據建議調整音頻文件

#### 步驟 3: 輸入目標文字

- **參考文字**: 輸入參考音頻中說的話 (可選)
- **目標文字**: 輸入要合成的新文字
- **語言選擇**: 選擇對應的語言

#### 步驟 4: 生成語音

- 點擊「開始生成語音」
- 等待處理完成 (通常 10-30 秒)
- 播放或下載生成的語音

## 🔧 API 接口

### 上傳音頻文件

```http
POST /api/voice/upload
Content-Type: multipart/form-data

{
  "audio": <音頻文件>
}
```

### 語音克隆

```http
POST /api/voice/clone
Content-Type: application/json

{
  "reference_audio_path": "音頻文件路徑",
  "target_text": "要合成的文字",
  "prompt_text": "參考文字 (可選)",
  "language": "zh"
}
```

### 獲取服務狀態

```http
GET /api/voice/status
```

## 🛠 故障排除

### 常見問題

#### 1. GPT-SoVITS API 啟動失敗

**症狀**: 語音克隆服務顯示 "GPT-SoVITS API 異常"
**解決方法**:

- 檢查 `GPT-SoVITS-v4-20250422fix` 目錄是否存在
- 確認預訓練模型已下載
- 手動啟動 GPT-SoVITS API: `python api_v2.py`

#### 2. 音頻上傳失敗

**症狀**: 上傳時顯示錯誤
**解決方法**:

- 檢查音頻文件格式是否支持
- 確認文件大小不超過 50MB
- 檢查 `audio_uploads` 目錄權限

#### 3. 語音生成失敗

**症狀**: 點擊生成後報錯
**解決方法**:

- 確認參考音頻質量足夠好
- 檢查目標文字是否過長
- 查看服務日誌獲取詳細錯誤信息

#### 4. 生成速度慢

**症狀**: 語音生成需要很長時間
**解決方法**:

- 使用 GPU 加速 (如果有 NVIDIA 顯卡)
- 減少目標文字長度
- 關閉其他占用資源的程序

### 日誌查看

- 語音克隆服務日誌: 終端輸出
- GPT-SoVITS 日誌: `GPT-SoVITS-v4-20250422fix/logs/`

## 📈 性能優化

### 1. GPU 加速

如果有 NVIDIA 顯卡，安裝 CUDA 版本的 PyTorch:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. 記憶體優化

- 關閉不必要的程序
- 增加虛擬記憶體
- 使用 SSD 硬碟

### 3. 網路優化

- 使用有線網路連接
- 確保網路穩定

## 🔒 安全注意事項

1. **文件安全**: 定期清理上傳的音頻文件
2. **訪問控制**: 確保只有授權用戶可以使用
3. **資料隱私**: 不要上傳包含敏感信息的音頻
4. **備份**: 定期備份重要的語音模型和配置

## 📞 技術支援

如果遇到問題，請提供以下信息：

1. 錯誤信息截圖
2. 系統配置 (CPU, 記憶體, 顯卡)
3. Python 版本
4. 使用的音頻文件格式和大小
5. 服務日誌

## 🔄 更新說明

### v1.0.0 (當前版本)

- ✅ 基本語音克隆功能
- ✅ 音頻質量分析
- ✅ 多語言支持
- ✅ Web 界面整合

### 計劃功能

- 🔄 批量語音克隆
- 🔄 語音情感控制
- 🔄 更多音頻格式支持
- 🔄 雲端部署支持
